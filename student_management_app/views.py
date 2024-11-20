from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_control
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.urls import reverse


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from student_management_app.EmailBackEnd import EmailBackEnd
from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def loginPage(request):
    if request.user.is_authenticated:
        if request.user.user_type == '1':
            return redirect('admin_home')
        elif request.user.user_type == '2':
            return redirect('staff_home')
        elif request.user.user_type == '3':
            return redirect('student_home')
        else:
            return redirect('login')
    
    return render(request, 'login.html')


class LoginAPIView(APIView):
    permission_classes = [AllowAny]  # Disable permissions for login view

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Pass email as username to authenticate
        user = authenticate(request, username=email, password=password)
        if not user:
            raise AuthenticationFailed("Invalid login credentials")

        if user.last_login_session_key:
            # Check for active session
            try:
                active_session = Session.objects.get(session_key=user.last_login_session_key)
                if active_session.expire_date > timezone.now():
                    return Response({"error": "Account already logged in on another device"}, status=403)
            except Session.DoesNotExist:
                pass

        login(request, user)
        refresh = RefreshToken.for_user(user)

        # Determine redirection URL based on user_type
        if user.user_type == "1":
            redirect_url = reverse('admin_home')
        elif user.user_type == "2":
            redirect_url = reverse('staff_home')
        elif user.user_type == "3":
            redirect_url = reverse('student_home')
        else:
            redirect_url = reverse('login')

        return Response({
            "message": "Login successful",
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            "redirect_url": redirect_url,
        })

def get_user_details(request):
    """Fetch details of the logged-in user."""
    if request.user:
        return JsonResponse({
            "email": request.user.email,
            "user_type": request.user.user_type,
        })
    else:
        return HttpResponse("Please Login First")

@csrf_exempt
def logout_user(request):
    try:
        # Invalidate JWT tokens (optional, if using token blacklist)
        refresh_token = request.POST.get("refresh", None)
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception as e:
                return JsonResponse({"message": "Failed to blacklist the token", "error": str(e)}, status=400)
        
        logout(request)
        # Redirect to the login page
        return redirect('login')

    except Exception as e:
        return JsonResponse({"message": "Logout failed", "error": str(e)}, status=500)


@receiver(user_logged_in)
def update_session_key(sender, user, request, **kwargs):
    """Ensure a single active session per user."""
    current_session_key = request.session.session_key
    if user.last_login_session_key:
        try:
            old_session = Session.objects.get(session_key=user.last_login_session_key)
            old_session.delete()
        except Session.DoesNotExist:
            pass

    user.last_login_session_key = current_session_key
    user.save()


@receiver(user_logged_out)
def clear_session_key(sender, request, user, **kwargs):
    """Clear session key on logout."""
    if user:
        user.last_login_session_key = None
        user.save()
