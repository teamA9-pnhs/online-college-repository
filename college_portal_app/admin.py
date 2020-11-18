from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, AdminHOD, Teachers, Semisters, Subjects, Students, Attendance, AttendanceReport, LeaveReportStudent, LeaveReportTeacher, FeedBackStudent, FeedBackTeachers, NotificationStudent, NotificationTeachers

# Register your models here.
class UserModel(UserAdmin):
    pass


admin.site.register(CustomUser, UserModel)

admin.site.register(AdminHOD)
admin.site.register(Teachers)
admin.site.register(Semisters)
admin.site.register(Subjects)
admin.site.register(Students)
admin.site.register(Attendance)
admin.site.register(AttendanceReport)
admin.site.register(LeaveReportStudent)
admin.site.register(LeaveReportTeacher)
admin.site.register(FeedBackStudent)
admin.site.register(FeedBackTeachers)
admin.site.register(NotificationStudent)
admin.site.register(NotificationTeachers)
