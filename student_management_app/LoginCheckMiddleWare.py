from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.urls import reverse

class LoginCheckMiddleWare(MiddlewareMixin):
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        user = request.user

        # List of allowed paths without login
        allowed_paths = [
            reverse("password_reset"),
            reverse("password_reset_done"),
            reverse("password_reset_complete"),
        ]

        # Allow dynamic reset confirm URL
        if 'reset' in request.path and 'password_reset_confirm' in request.resolver_match.url_name:
            allowed_paths.append(request.path)

        # Check whether the user is logged in or not
        if user.is_authenticated:
            if user.user_type == "1":
                if modulename == "student_management_app.HodViews":
                    pass
                elif modulename == "student_management_app.views" or modulename == "django.views.static":
                    pass
                else:
                    return redirect("admin_home")
            
            elif user.user_type == "2":
                if modulename == "student_management_app.StaffViews":
                    pass
                elif modulename == "student_management_app.views" or modulename == "django.views.static":
                    pass
                else:
                    return redirect("staff_home")
            
            elif user.user_type == "3":
                if modulename == "student_management_app.StudentViews":
                    pass
                elif modulename == "student_management_app.views" or modulename == "django.views.static":
                    pass
                else:
                    return redirect("student_home")

            else:
                return redirect("login")

        else:
            # Allow password reset views without login
            if request.path in allowed_paths or 'reset' in request.path:
                pass
            elif request.path == reverse("login") or request.path == reverse("doLogin"):
                pass
            else:
                return redirect("login")