from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date
from django.urls import reverse


class SessionYearModel(models.Model):
    id = models.AutoField(primary_key=True)
    session_start_year = models.DateField()
    session_end_year = models.DateField()
    objects = models.Manager()



# Overriding the Default Django Auth User and adding One More Field (user_type)
class CustomUser(AbstractUser):
    user_type_data = ((1, "HOD"), (2, "Teacher"), (3, "Student"))
    random_key = models.CharField(default=000000, max_length=6)
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)

# class CustomUser(AbstractBaseUser):
#     class Meta:
#         unique_together = (('id'),('email'))
#     id = models.AutoField(primary_key=True);
#     email= models.EmailField(unique=True);
#     password=models.CharField(max_length=50);
#     user_type_data=((1,"HOD"),(2,"Teacher"),(3,"Student"));
#     random_key = models.CharField(default=000000, max_length=6)
#     user_type = models.CharField(default=1, choices=user_type_data, max_length=10)
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS= []



class AdminHOD(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Teachers(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Semisters(models.Model):
    id = models.AutoField(primary_key=True)
    semister_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    # def __str__(self):
	#     return self.semister_name



class Subjects(models.Model):
    id =models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=255)
    semister_id = models.ForeignKey(Semisters, on_delete=models.CASCADE, default=1) #need to give defauult semister
    teacher_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()



class Students(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    gender = models.CharField(max_length=50)
    profile_pic = models.FileField()
    address = models.TextField()
    semister_id = models.ForeignKey(Semisters, on_delete=models.DO_NOTHING, default=1)
    session_start_year=models.DateField()
    session_end_year=models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class AttendanceReport(models.Model):
    # Individual Student Attendance
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.DO_NOTHING)
    # attendance_id = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    # attendance_date = models.DateField()
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Attendance(models.Model):
    # Subject Attendance
    # id = models.AutoField(primary_key=True)
    # subject_id = models.ForeignKey(Subjects, on_delete=models.DO_NOTHING)
    # attendance_date = models.DateField()
    # session_year_id = models.ForeignKey(SessionYearModel, on_delete=models.CASCADE)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    # objects = models.Manager()
    id = models.AutoField(primary_key=True)
    teacher_id = models.ForeignKey(Teachers, on_delete=models.CASCADE)
    # attendance_id = models.ForeignKey(AttendanceReport, on_delete=models.CASCADE)
    # attendance_date = models.DateField()
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class LeaveReportStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class LeaveReportTeacher(models.Model):
    id = models.AutoField(primary_key=True)
    teacher_id = models.ForeignKey(Teachers, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class LeaveReportStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class FeedBackStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class FeedBackTeachers(models.Model):
    id = models.AutoField(primary_key=True)
    teacher_id = models.ForeignKey(Teachers, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()



class NotificationStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class NotificationTeachers(models.Model):
    id = models.AutoField(primary_key=True)
    teacherf_id = models.ForeignKey(Teachers, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class StudentResult(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    subject_exam_marks = models.FloatField(default=0)
    subject_assignment_marks = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

# Name: Harshat 
# Functionality : Calendar database for users
# view : 
# html :
# url :
# last modified : 19/06/2020

class Calendar(models.Model):
    customuser = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    start_time = models.TimeField(auto_now=False,auto_now_add=False,editable=True)
    end_time = models.TimeField(auto_now=False,auto_now_add=False,editable=True)
    created_date = models.DateField(auto_now=False , editable=True)  
    objects=models.Manager()
    

#Creating Django Signals

# It's like trigger in database. It will run only when Data is Added in CustomUser model

@receiver(post_save, sender=CustomUser)
# Now Creating a Function which will automatically insert data in HOD, Teacher or Student
def create_user_profile(sender, instance, created, **kwargs):
    # if Created is true (Means Data Inserted)
    if created:
        # Check the user_type and insert the data in respective tables
        if instance.user_type == 1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type == 2:
            Teachers.objects.create(admin=instance)
        if instance.user_type == 3:
            Students.objects.create(admin=instance, semister_id=Semisters.objects.get(id=1),session_start_year="2020-01-01",session_end_year="2021-01-01", address="", profile_pic="", gender="")
    

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhod.save()
    if instance.user_type == 2:
        instance.teachers.save()
    if instance.user_type == 3:
        instance.students.save()
    


