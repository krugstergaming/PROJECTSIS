from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model  # Add this import

from student_management_app.EmailBackEnd import EmailBackEnd


def home(request):
    return render(request, 'index.html')


def loginPage(request):
    return render(request, 'login.html')


def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        # Pass 'email' as 'username' and 'password' from POST to the custom backend
        user = EmailBackEnd().authenticate(username=request.POST.get('email'), password=request.POST.get('password'))

        if user:
            # Check if the account is deactivated
            if not user.is_active:
                messages.error(request, "Your account has been deactivated due to multiple failed login attempts. Please contact the admin to reactivate it.")
                return redirect('login')

            # Reset failed login attempts on successful login
            user.failed_login_attempts = 0
            user.save()

            login(request, user)
            user_type = user.user_type

            # Redirect user based on their type
            if user_type == '1':  # HOD
                return redirect('admin_home')
            elif user_type == '2':  # Staff
                return redirect('staff_home')
            elif user_type == '3':  # Student
                return redirect('student_home')
            else:
                messages.error(request, "Invalid Login!")
                return redirect('login')

        else:
            # Authentication failed, check if user exists
            user = get_user_model().objects.filter(email=request.POST.get('email')).first()

            if user:
                # Increment failed login attempts
                user.failed_login_attempts += 1
                if user.failed_login_attempts >= 3:
                    user.is_active = False  # Deactivate account after 3 failed attempts
                    user.save()
                    messages.error(request, "Your account has been deactivated due to multiple failed login attempts. Please contact the admin to reactivate it.")
                    return redirect('login')  # Prevent further login attempts

                user.save()

            messages.error(request, "Invalid Login Credentials!")
            return redirect('login')


def get_user_details(request):
    if request.user is not None:
        return HttpResponse(f"User: {request.user.email} User Type: {request.user.user_type}")
    else:
        return HttpResponse("Please Login First")


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')
