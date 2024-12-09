# student_management_app/middleware/ClearStaleSessionMiddleware.py
from django.contrib.sessions.models import Session
from django.utils.timezone import now
from student_management_app.models import CustomUser

class ClearStaleSessionMiddleware:
    """
    Middleware to check and clear stale session keys from users
    if their session has expired.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            try:
                # Check if the session is expired
                session = Session.objects.get(session_key=request.user.last_login_session_key)
                if session.expire_date < now():
                    # Session expired, clear user fields
                    request.user.last_login_session_key = None
                    request.user.session_expiry = None
                    request.user.save()
            except Session.DoesNotExist:
                # Session no longer exists
                request.user.last_login_session_key = None
                request.user.session_expiry = None
                request.user.save()

        response = self.get_response(request)
        return response
