# from channels.auth import login, logout
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model

from college_portal_app.EmailBackEnd import EmailBackEnd


def home(request):
    return render(request, 'index.html')


def loginPage(request):
    return render(request, 'login.html')

def go_here(request):
    if request.method == 'GET':
       return render(request , 'reset.html',{'message':"Enter your Email here to check if the User exists"})

def reset_password(request):
    if not 'email' in request.POST is None:
        email = request.POST.get('email')
    else:
        return redirect('reset.html', {'message':"Please Enter a Valid Email"})
    if not get_user_model().objects.filter(email= email):
        return render(request, 'reset.html', {'exists':False ,'message':"Please register your name with your faculty",'email':email} )
    return render(request, 'reset.html' , {'exists':True,'message' : "Verified", 'email':email})
  

def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
        
    else:
        user = EmailBackEnd.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
        if user != None:
            login(request, user)
            user_type = user.user_type
            #return HttpResponse("Email: "+request.POST.get('email')+ " Password: "+request.POST.get('password'))
            if user_type == '1':
                return redirect('admin_home')
                
            elif user_type == '2':
                return HttpResponse("Teacher Login"+str(user.user_type))
                # return redirect('teacher_home')
                
            elif user_type == '3':
                # return HttpResponse("Student Login")
                return redirect('student_home')
            else:
                messages.error(request, "Invalid Login!")
                return redirect('login')
        else:
            messages.error(request, "Invalid Login Credentials!")
            #return HttpResponseRedirect("/")
            return redirect('login')



def get_user_details(request):
    if request.user != None:
        return HttpResponse("User: "+request.user.email+" User Type: "+request.user.user_type)
    else:
        return HttpResponse("Please Login First")



def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


