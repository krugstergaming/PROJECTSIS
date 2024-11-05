# from channels.auth import login, logout
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from student_management_app.EmailBackEnd import EmailBackEnd

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def loginPage(request):
    session_exists = request.session.session_key is not None
    context = {
        'session_exists': session_exists,
    }

    if request.user.is_authenticated:
        if request.user.user_type == '1':
            return redirect('admin_home')
        elif request.user.user_type == '2':
            return redirect('staff_home')
        elif request.user.user_type == '3':
            return redirect('student_home')
        else:
            return redirect('login')
    
    return render(request, 'login.html', context)

 
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
                # return HttpResponse("Staff Login")
                return redirect('staff_home')
                
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

@csrf_exempt
def logout_on_close(request):
    # Logs out the user if they are authenticated, called by JavaScript when the tab is closed
    if request.user.is_authenticated:
        logout(request)
    return HttpResponse(status=200)

@login_required
def check_login_status(request):
    return JsonResponse({'is_logged_in': True})

def check_login_status_unauthenticated(request):
    return JsonResponse({'is_logged_in': False})


