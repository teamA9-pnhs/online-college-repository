from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, redirect
from django.urls import reverse
import re
from django.conf import settings


if hasattr(settings, 'LOGIN_EXEMPT_URLS' ):
    EXEMPT_URLS =[re.compile(url) for url in settings.LOGIN_EXEMPT_URLS]
print(EXEMPT_URLS)

class LoginCheckMiddleWare(MiddlewareMixin):
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        # print(modulename)
        user = request.user

        #Check whether the user is logged in or not
        if user.is_authenticated:
            if user.user_type == "1":
                if modulename == "college_portal_app.HodViews":
                    pass
                elif modulename == "college_portal_app.views" or modulename == "django.views.static":
                    pass
                else:
                    return redirect("admin_home")
            
            elif user.user_type == "2":
                if modulename == "college_portal_app.TeacherViews":
                    pass
                elif modulename == "college_portal_app.views" or modulename == "django.views.static":
                    pass
                else:
                   return render(request, "staff_Templates/base_template.html")
            
            elif user.user_type == "3":
                if modulename == "college_portal_app.StudentViews":
                    pass
                elif modulename == "college_portal_app.views" or modulename == "django.views.static":
                    pass
                else:
                    return render(request, "student_Templates/base_template.html")

            else:
                return redirect("login")

        else:
            path = request.path_info
            if(path=='/'):
                return None;
            if not any(url.match(path) for url in EXEMPT_URLS):
                return redirect("login")
