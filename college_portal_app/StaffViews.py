#code written and modified
#date :19-06-21
#author:neetya

from college_portal_app.models import SessionYearModel, Subjects
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, request
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json

def staff_home(request):
    return render(request, "staff_templates/home_content.html")

def staff_attendance_template(request):
    subject=Subjects.objects.filter(subject_id=request.user.id)
    session_year=SessionYearModel.objects.all()
    return render(request,"staff_template/staff_attendance_template.html",{"subject":subject,"session_year":session_year})