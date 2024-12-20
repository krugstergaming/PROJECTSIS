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
from django.contrib.auth import get_user_model  # Add this import


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from student_management_app.EmailBackEnd import EmailBackEnd
from rest_framework_simplejwt.exceptions import TokenError
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
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = EmailBackEnd.authenticate(request, username=email, password=password)

        if user:
            if not user.is_active:
                return Response(
                    {"error": "Your account has been deactivated due to multiple failed login attempts. Please contact support."}, 
                    status=403
                )
            
            # Check user type and active session logic
            if user.user_type in ["1", "2", "3"]:
                if user.last_login_session_key:
                    try:
                        active_session = Session.objects.get(session_key=user.last_login_session_key)
                        if active_session.expire_date > timezone.now():
                            return Response({"error": "Account already logged in on another device"}, status=403)
                    except Session.DoesNotExist:
                        pass
            else:
                return Response({"error": "User type is invalid or missing."}, status=400)

            if user:
                user.failed_login_attempts = 0
                user.save()
            else:
                user_model = get_user_model()
                user = user_model.objects.filter(email=email).first()
                user.failed_login_attempts += 1
                if user.failed_login_attempts >= 3:
                    user.is_active = False  # Deactivate account after 3 failed attempts
                    user.save()
                    return Response(
                        {"error": "Your account has been deactivated due to multiple failed login attempts. Please contact support."}, 
                        status=403
                    )

                user.save()

            # Log the user in
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

            response_data = {
                "message": "Login successful",
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                "redirect_url": redirect_url,
            }
            return Response(response_data)
        else:
            return Response({"error": "Invalid login credentials"}, status=401)
        


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)

            if not refresh_token:
                return Response({"error": "Refresh token is required"}, status=400)

            token.blacklist()
            logout(request)

        except Exception as e:
            return Response({"error": f"Failed to blacklist token: {str(e)}"}, status=500)

        return Response({"message": "Logged out successfully"})

class DecodeRefreshTokenView(APIView):
    permission_classes = [AllowAny]  # Open endpoint, no authentication required

    def post(self, request):
        refresh_token = request.data["refresh_token"]
        if not refresh_token:
            return Response({"error": "Refresh token is required"}, status=400)

        try:
            token = RefreshToken(refresh_token)

            # Check if the token is blacklisted
            if token.check_blacklist():
                return Response({"error": "Token is blacklisted"}, status=403)

            # Decode and retrieve the user_id
            user_id = token.get("user_id")

            # Fetch the user from the database
            from student_management_app.models import CustomUser
            user = CustomUser.objects.get(id=user_id)

            return Response({
                "email": user.email,
                "user_type": user.get_user_type_display()
            })

        except TokenError as e:
            # Handle invalid or blacklisted token errors
            return Response({"error": f"Token error: {str(e)}"}, status=403)
        except CustomUser.DoesNotExist:
            # Handle case where the user doesn't exist
            return Response({"error": "User not found"}, status=404)
        except Exception as e:
            # Handle all other exceptions
            return Response({"error": str(e)}, status=400)
        
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
    user.session_expiry = request.session.get_expiry_date()  # Store session expiry
    user.save()


@receiver(user_logged_out)
def clear_session_key(sender, request, user, **kwargs):
    """Clear session key on logout."""
    if user:
        user.last_login_session_key = None
        user.session_expiry = None
        user.save()
