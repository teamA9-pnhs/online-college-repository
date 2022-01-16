from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
from college_portal_app.forms import EventForm
from college_portal_app.models import CustomUser, Teachers,Semisters,Students,Calendar,LeaveReportTeacher,LeaveReportStudent,Attendance,AttendanceReport



def admin_home(request):
    return render(request, "hod_template/home_content.html")

def staff_home(request):
    return render(request, "staff_Templates/base_template.html")

def student_home(request):
    return render(request, "student_Templates/base_template.html")

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
    # print(context.admin)
    return render(request, 'hod_template/manage_student.html', context)


def leave_req(request):
    students = LeaveReportStudent.objects.all()
    context = {
        "students": students
    }
    # print(context.admin)
    return render(request, 'hod_template/leave_req.html', context)
    
def leave_req_faculty(request):
    Teachers = LeaveReportTeacher.objects.all()
    context = {
        "teachers": Teachers
    }
    # print(context.admin)
    return render(request, 'hod_template/leave_req_faculty.html', context)

def attendance_faculty(request):
    Teachers = Attendance.objects.all()
    context = {
        "teachers": Teachers
    }
    # print(context.admin)
    return render(request, 'hod_template/attendance_faculty.html', context)

def attendance_student(request):
    Students = AttendanceReport.objects.all()
    context = {
        "students": Students
    }
    # print(context.admin)
    return render(request, 'hod_template/attendance_student.html', context)



# Name: Harshat 
# Functionality : Calendar database for users
# model : models.py -> Calendar 
# html : sidebar.html, hod_templates/calendar.html
# url : urls.py
# last modified : 19/06/2020
from json import dumps
from django.core import serializers

def show_calendar(request):
    calendar_events = Calendar.objects.filter(customuser=request.user).values()
    calendar = {}
    # dataJson_1 = json.dumps(calendar_events,indent=0, sort_keys=True,default=str)
    i='a'
    for e in calendar_events:
        calendar[i] = e
        i=i+'a'
    # dataJson =json.dumps(calendar, indent=0, sort_keys=True, default=str);
    # x = dataJson.split("\n")
    # dataJson = serializers.serialize('json',calendar);
    # print(calendar['a'])
    # print(calendar_events.title)
    return render(request, 'hod_template/calendar.html',{'calendar_events':calendar_events})

def new_event(request):
    form = EventForm(request.POST or None)
    print(request.GET["this_day"] )
    if request.POST and form.is_valid():
        print("VOILA SUCCESSFUL MY FRIEND")
        title = form.cleaned_data['title']
        description = form.cleaned_data['description']
        start_time = form.cleaned_data['start_time']
        end_time = form.cleaned_data['end_time']
        Calendar.objects.get_or_create(
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time,
            customuser=request.user,
            created_date=request.GET["this_day"]
        )
        return HttpResponseRedirect(reverse('show_calendar'))
    return render(request, 'hod_template/event.html', {'form': form})

