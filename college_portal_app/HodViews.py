from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json

from college_portal_app.models import CustomUser, Teachers,Semisters,Students,Subjects



def admin_home(request):
    return render(request, "hod_template/home_content.html")


def add_teacher(request):
    return render(request, "hod_template/add_teacher_template.html")


def add_teacher_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect('add_teacher')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')

        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=2)
            user.teachers.address = address
            user.save()
            messages.success(request, "Teacher Added Successfully!")
            return redirect('add_teacher')
        except:
            messages.error(request, "Failed to Add Teacher!")
            return redirect('add_teacher')



def manage_teacher(request):
    teachers = Teachers.objects.all()
    context = {
        "teachers": teachers
    }
    return render(request, "hod_template/manage_teacher_template.html", context)


def edit_teacher(request, teacher_id):
    teacher = Teachers.objects.get(admin=teacher_id)

    context = {
        "teacher": teacher,
        "id": teacher_id
    }
    return render(request, "hod_template/edit_teacher_template.html", context)


def edit_teacher_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        teacher_id = request.POST.get('teacher_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')

        try:
            # INSERTING into Customuser Model
            user = CustomUser.objects.get(id=teacher_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()
            
            # INSERTING into Teacher Model
            teacher_model = Teachers.objects.get(admin=teacher_id)
            teacher_model.address = address
            teacher_model.save()

            messages.success(request, "Teacher Updated Successfully.")
            return redirect('/edit_teacher/'+teacher_id)

        except:
            messages.error(request, "Failed to Update Teacher.")
            return redirect('/edit_teacher/'+teacher_id)



def delete_teacher(request, teacher_id):
    teacher = Teachers.objects.get(admin=teacher_id)
    try:
        teacher.delete()
        messages.success(request, "Teacher Deleted Successfully.")
        return redirect('manage_teacher')
    except:
        messages.error(request, "Failed to Delete Teacher.")
        return redirect('manage_teacher')





def add_semister(request):
    return render(request,"hod_template/add_semister.html")

def add_semister_save(request):
    if request.method!="POST":
        return HttpResponseRedirect("Method Not Allowed")
    else:
        semister=request.POST.get("semister")
        try:
            semister_model=Semisters(semister_name=semister)
            semister_model.save()
            messages.success(request, "Semister Deleted Successfully.")
            return redirect('/add_semister')
        except:
            messages.error(request, "Failed to add Semister.")
            return redirect('/add_semister')
        

def manage_semister(request):
    semisters = Semisters.objects.all()
    context = {
        "semisters": semisters
    }
    return render(request, "hod_template/manage_semister.html", context)


def edit_semister(request, semister_id):
    semister = Semisters.objects.get(id=semister_id)
    context = {
        "semister": semister,
        "id": semister_id
    }
    return render(request, 'hod_template/edit_semister.html', context)


def edit_semister_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        semister_id = request.POST.get('semister_id')
        semister_name = request.POST.get('semister')

        try:
            semister = Semisters.objects.get(id=semister_id)
            semister.semister_name = semister_name
            semister.save()

            messages.success(request, "Semister Updated Successfully.")
            return redirect('/edit_semister/'+semister_id)

        except:
            messages.error(request, "Failed to Update Semister.")
            return redirect('/edit_semister/'+semister_id)

def delete_semister(request, semister_id):
    semister = Semisters.objects.get(id=semister_id)
    try:
        semister.delete()
        messages.success(request, "Semister Deleted Successfully.")
        return redirect('manage_semister')
    except:
        messages.error(request, "Failed to Delete Semister.")
        return redirect('manage_semister')


def add_student(request):
    semisters=Semisters.objects.all()
    return render(request,'hod_template/add_student.html',{"semisters":semisters})

def add_student_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect('add_student')
        
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        session_start=request.POST.get('session_start')
        session_end=request.POST.get('session_end')
        semister_id=request.POST.get('semister')
        sex=request.POST.get("sex")

        try:

            user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=3)
            user.students.address = address
            semister_obj=Semisters.objects.get(id=semister_id)
            user.students.semister_id=semister_obj
            user.students.session_start_year=session_start
            user.students.session_end_year=session_end
            user.students.gender=sex
            user.students.profile_pics=""
            user.save()
            messages.success(request, "Student Added Successfully!")
            return redirect('add_student')
        except:
            messages.error(request, "Failed to Add Student!")
            return redirect('add_student')


def manage_student(request):
    students = Students.objects.all()
    context = {
        "students": students
    }
    return render(request, 'hod_template/manage_student.html', context)
#student module author neetya date 20-6-21
def add_student(request):
    semisters=Semisters.objects.all()
    return render(request,'hod_template/add_student.html',{"semisters":semisters})

def add_student_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect('add_student')
        
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        session_start=request.POST.get('session_start')
        session_end=request.POST.get('session_end')
        semister_id=request.POST.get('semister')
        sex=request.POST.get("sex")

        try:

            user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=3)
            user.students.address = address
            semister_obj=Semisters.objects.get(id=semister_id)
            user.students.semister_id=semister_obj
            user.students.session_start_year=session_start
            user.students.session_end_year=session_end
            user.students.gender=sex
            user.students.profile_pics=""
            user.save()
            messages.success(request, "Student Added Successfully!")
            return redirect('add_student')
        except:
            messages.error(request, "Failed to Add Student!")
            return redirect('add_student')


def manage_student(request):
    students = Students.objects.all()
    context = {
        "students": students
    }
    return render(request, 'hod_template/manage_student.html', context)

def edit_student(request, student_id):
    student = Students.objects.get(admin=student_id)

    context = {
        "student": student,
        "id": student_id
    }
    return render(request, "hod_template/edit_student.html", context)


def edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        student_id = request.POST.get('student_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')

        try:
            # INSERTING into Customuser Model
            user = CustomUser.objects.get(id=student_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()
            
            # INSERTING into Teacher Model
            student_model = Students.objects.get(admin=student_id)
            student_model.address = address
            student_model.save()

            messages.success(request, "Student Updated Successfully.")
            return redirect('/edit_student/'+student_id)

        except:
            messages.error(request, "Failed to Update Student.")
            return redirect('/edit_student/'+student_id)

def delete_student(request,student_id):
    student = Students.objects.get(admin=student_id)
    try:
        student.delete()
        messages.success(request, "Student Deleted Successfully.")
        return redirect('manage_student')
    except:
        messages.error(request, "Failed to Delete student.")
        return redirect('manage_student')

def manage_session(request):
    return render(request,"hod_template/manage_session_template.html")

#def add_session_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("manage_session"))
    else:
        session_start_year=request.POST.get("session_start")
        session_end_year=request.POST.get("session_end")

        try:
            sessionyear=SessionYearModel(session_start_year=session_start_year,session_end_year=session_end_year)
            sessionyear.save()
            messages.success(request, "Successfully Added Session")
            return HttpResponseRedirect(reverse("manage_session"))
        except:
            messages.error(request, "Failed to Add Session")
            return HttpResponseRedirect(reverse("manage_session"))
#code by Neetya Dated: 19-06-21
#these u add and try
#see there is some mistake either of these four files
def add_subject_template(request):
    semisters=Semisters.objects.all()
    teachers=CustomUser.objects.filter(user_type=2)
    return render(request,"hod_template/add_subject_template.html", {"semisters":semisters,"teachers":teachers})

def add_subject_template_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_name=request.POST.get("subject_name")
        semister_id=request.POST.get("semester")
        teacher_id=request.POST.get("staff")
        

        try:
            subject=Subjects(subject_name=subject_name)
            semister_obj=Semisters.objects.get(id=semister_id)
            subject.semister_id=semister_obj
            teachers_obj=CustomUser.objects.get(id=teacher_id)
            subject.teacher_id=teachers_obj 
            subject.save()

            messages.success(request,"Successfully Added Subject")
            return redirect('add_subject_template')
        except:
            messages.error(request,"Failed to Add Subject")
            return redirect('add_subject_template')

def manage_subject(request):
    subjects=Subjects.objects.all()
    return render(request,"hod_template/manage_subject.html",{"subjects":subjects})



def manage_session(request):
    return render(request,"hod_template/manage_session_template.html")

#def add_session_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("manage_session"))
    else:
        session_start_year=request.POST.get("session_start")
        session_end_year=request.POST.get("session_end")

        try:
            sessionyear=SessionYearModel(session_start_year=session_start_year,session_end_year=session_end_year)
            sessionyear.save()
            messages.success(request, "Successfully Added Session")
            return HttpResponseRedirect(reverse("manage_session"))
        except:
            messages.error(request, "Failed to Add Session")
            return HttpResponseRedirect(reverse("manage_session"))
#code by Neetya Dated: 19-06-21
#these u add and try
#see there is some mistake either of these four files
def add_subject_template(request):
    semister=Semisters.objects.all()
    teachers=CustomUser.objects.filter(user_type=2)
    return render(request,"hod_template/add_subject_template.html", {"teachers":teachers,"semister":semister})

def add_subject_template_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_name=request.POST.get("subject_name")
        semisters_id=request.POST.get("semester")
        semisters=Semisters.objects.get(id=semisters_id)
        teachers_id=request.POST.get("staff")
        teachers=CustomUser.objects.get(id=teachers_id)

        try:
            subject=Subjects(subject_name=subject_name,semister_id=semisters,teacher_id=teachers)
            subject.save()
            messages.success(request,"Successfully Added Subject")
            return HttpResponseRedirect(reverse("add_subject"))
        except:
            messages.error(request,"Failed to Add Subject")
            return HttpResponseRedirect(reverse("add_subject"))

def manage_subject(request):
    subjects=Subjects.objects.all()
    return render(request,"hod_template/manage_subject.html",{"subjects":subjects})

