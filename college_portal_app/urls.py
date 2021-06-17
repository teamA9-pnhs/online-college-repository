
from django.urls import path, include
from . import views
from .import HodViews


urlpatterns = [
    path('', views.loginPage, name="login"),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('doLogin/', views.doLogin, name="doLogin"),
    path('get_user_details/', views.get_user_details, name="get_user_details"),
    path('logout_user/', views.logout_user, name="logout_user"),
    path('admin_home/', HodViews.admin_home, name="admin_home"),
    path('add_teacher/', HodViews.add_teacher, name="add_teacher"),
    path('add_teacher_save/', HodViews.add_teacher_save, name="add_teacher_save"),
    path('manage_teacher/', HodViews.manage_teacher, name="manage_teacher"),
    path('edit_teacher/<teacher_id>/', HodViews.edit_teacher, name="edit_teacher"),
    path('edit_teacher_save/', HodViews.edit_teacher_save, name="edit_teacher_save"),
    path('delete_teacher/<teacher_id>/', HodViews.delete_teacher, name="delete_teacher"),
    path('add_semister/', HodViews.add_semister, name="add_semister"),
    path('add_subject/',HodViews.add_subject, name="add_subject"),
    path('add_semister_save/', HodViews.add_semister_save, name="add_semister_save"),
    path('manage_semister/', HodViews.manage_semister, name="manage_semister"),
   path('manage_subject/', HodViews.manage_subject, name="manage_subject"),
    path('edit_semister/<semister_id>/', HodViews.edit_semister, name="edit_semister"),
    path('edit_semister_save/', HodViews.edit_semister_save, name="edit_semister_save"),
    path('delete_semister/<semister_id>/', HodViews.delete_semister, name="delete_semister"),
    path('add_student/', HodViews.add_student, name="add_student"),
    path('add_student_save/', HodViews.add_student_save, name="add_student_save"),
    path('manage_student/', HodViews.manage_student, name="manage_student"),
    path('check_email/', views.go_here, name ="go_here"),
    path('checked_email/', views.reset_password , name="reset_password"),
    path('send_otp/' , views.sending_email , name="sending_email"),
    path('successful/', views.verify_otp , name="verify_otp"),
    path('change_password/',views.change_password, name='change_password'),
    # path('attendance/', views.attendanceReport, name='attendance')
    # path('edit_student/<student_id>', HodViews.edit_student, name="edit_student"),
    # path('edit_student_save/', HodViews.edit_student_save, name="edit_student_save"),
    # path('delete_student/<student_id>/', HodViews.delete_student, name="delete_student"),
]
