from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

class RedirectAuthenticatedUserMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        super().__init__(get_response)

    def process_request(self, request):
        # Check if the request is for the login page and the user is authenticated
        if request.path == '' and request.user.is_authenticated:
            # Redirect to the appropriate home page based on user type
            if request.user.user_type == '1':
                return redirect('admin_home')
            elif request.user.user_type == '2':
                return redirect('staff_home')
            elif request.user.user_type == '3':
                return redirect('student_home')
            else:
                return redirect('')  # Fallback if user_type is not recognized

    def __call__(self, request):
        response = super().__call__(request)  # Call the parent __call__ method
        return response
