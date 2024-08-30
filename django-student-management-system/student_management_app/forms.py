from django import forms 
from django.forms import Form
from student_management_app.models import Courses, SessionYearModel, Subjects, Staffs


class DateInput(forms.DateInput):
    input_type = "date"


class AddStudentForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    password = forms.CharField(label="Password", max_length=50, widget=forms.PasswordInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    gender_list = (
        ('Male','Male'),
        ('Female','Female')
    )
    gender = forms.ChoiceField(label="Gender", choices=gender_list, widget=forms.Select(attrs={"class":"form-control"}))
    
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))

    #For Displaying Courses
    try:
        courses = Courses.objects.all()
        course_list = [(course.id, course.course_name) for course in courses]
    except Exception as e:
        print("Error fetching courses:", e)
        course_list = []
    
    #For Displaying Session Years
    try:
        session_years = SessionYearModel.objects.all()
        session_year_list = [(session_year.id, f"{session_year.session_start_year} to {session_year.session_end_year}") for session_year in session_years]
    except Exception as e:
        print("Error fetching session years:", e)
        session_year_list = []

    course_id = forms.ChoiceField(label="Course", choices=course_list, widget=forms.Select(attrs={"class":"form-control"}), error_messages={'required': 'Please select a valid course.'})
    session_year_id = forms.ChoiceField(label="Session Year", choices=session_year_list, widget=forms.Select(attrs={"class":"form-control"}))

    def __init__(self, *args, **kwargs):
        super(AddStudentForm, self).__init__(*args, **kwargs)
        
        # Add a placeholder choice at the beginning
        self.fields['course_id'].choices = [('', 'Select a Course')] + [(course.id, course.course_name) for course in Courses.objects.all()]
        self.fields['session_year_id'].choices = [('', 'Select a Session Year')] + [(session_year.id, f"{session_year.session_start_year} to {session_year.session_end_year}") for session_year in SessionYearModel.objects.all()]

    
    # session_start_year = forms.DateField(label="Session Start", widget=DateInput(attrs={"class":"form-control"}))
    # session_end_year = forms.DateField(label="Session End", widget=DateInput(attrs={"class":"form-control"}))
    profile_pic = forms.FileField(label="Profile Pic", required=False, widget=forms.FileInput(attrs={"class":"form-control"}))



class EditStudentForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))

    #For Displaying Courses
    try:
        courses = Courses.objects.all()
        course_list = []
        for course in courses:
            single_course = (course.id, course.course_name)
            course_list.append(single_course)
    except:
        course_list = []

    #For Displaying Session Years
    try:
        session_years = SessionYearModel.objects.all()
        session_year_list = []
        for session_year in session_years:
            single_session_year = (session_year.id, str(session_year.session_start_year)+" to "+str(session_year.session_end_year))
            session_year_list.append(single_session_year)
            
    except:
        session_year_list = []

    
    gender_list = (
        ('Male','Male'),
        ('Female','Female')
    )
    
    course_id = forms.ChoiceField(label="Course", choices=course_list, widget=forms.Select(attrs={"class":"form-control"}))
    gender = forms.ChoiceField(label="Gender", choices=gender_list, widget=forms.Select(attrs={"class":"form-control"}))
    session_year_id = forms.ChoiceField(label="Session Year", choices=session_year_list, widget=forms.Select(attrs={"class":"form-control"}))
    # session_start_year = forms.DateField(label="Session Start", widget=DateInput(attrs={"class":"form-control"}))
    # session_end_year = forms.DateField(label="Session End", widget=DateInput(attrs={"class":"form-control"}))
    profile_pic = forms.FileField(label="Profile Pic", required=False, widget=forms.FileInput(attrs={"class":"form-control"}))


class AddScheduleForm(forms.Form):
    # Select the Course
    try:
        courses = Courses.objects.all()
        course_list = [(course.id, course.course_name) for course in courses]
    except Exception as e:
        print("Error fetching courses:", e)
        course_list = []
    
    course_id = forms.ChoiceField(
        label="Course", 
        choices=course_list, 
        widget=forms.Select(attrs={"class": "form-control"})
    )

    # Select the Subject
    try:
        subjects = Subjects.objects.all()
        subject_list = [(subject.id, subject.subject_name) for subject in subjects]
    except Exception as e:
        print("Error fetching subjects:", e)
        subject_list = []

    subject_id = forms.ChoiceField(
        label="Subject", 
        choices=subject_list, 
        widget=forms.Select(attrs={"class": "form-control"})
    )

    # Select the Staff Member
    try:
        staff_members = Staffs.objects.all()
        staff_list = [(staff.id, f"{staff.admin.first_name} {staff.admin.last_name}") for staff in staff_members]
    except Exception as e:
        print("Error fetching staff members:", e)
        staff_list = []

    staff_id = forms.ChoiceField(
        label="Staff Member", 
        choices=staff_list, 
        widget=forms.Select(attrs={"class": "form-control"})
    )

    # Select the Session Year
    try:
        session_years = SessionYearModel.objects.all()
        session_year_list = [(session_year.id, f"{session_year.session_start_year} to {session_year.session_end_year}") for session_year in session_years]
    except Exception as e:
        print("Error fetching session years:", e)
        session_year_list = []

    session_year_id = forms.ChoiceField(
        label="Session Year", 
        choices=session_year_list, 
        widget=forms.Select(attrs={"class": "form-control"})
    )

    # Day of the Week
    days_of_week = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday')
    ]
    day_of_week = forms.ChoiceField(
        label="Day of Week", 
        choices=days_of_week, 
        widget=forms.Select(attrs={"class": "form-control"})
    )

    # Start Time and End Time
    start_time = forms.TimeField(
        label="Start Time", 
        widget=forms.TimeInput(attrs={"class": "form-control", "type": "time"})
    )
    end_time = forms.TimeField(
        label="End Time", 
        widget=forms.TimeInput(attrs={"class": "form-control", "type": "time"})
    )

    def __init__(self, *args, **kwargs):
        super(AddScheduleForm, self).__init__(*args, **kwargs)
        # Placeholder choices
        self.fields['course_id'].choices = [('', 'Select a Course')] + [(course.id, course.course_name) for course in Courses.objects.all()]
        self.fields['subject_id'].choices = [('', 'Select a Subject')] + [(subject.id, subject.subject_name) for subject in Subjects.objects.all()]
        self.fields['staff_id'].choices = [('', 'Select a Staff Member')] + [(staff.id, f"{staff.admin.first_name} {staff.admin.last_name}") for staff in Staffs.objects.all()]
        self.fields['session_year_id'].choices = [('', 'Select a Session Year')] + [(session_year.id, f"{session_year.session_start_year} to {session_year.session_end_year}") for session_year in SessionYearModel.objects.all()]


class EditScheduleForm(forms.Form):
    # For Displaying Courses
    try:
        courses = Courses.objects.all()
        course_list = [(course.id, course.course_name) for course in courses]
    except:
        course_list = []

    # For Displaying Subjects
    try:
        subjects = Subjects.objects.all()
        subject_list = [(subject.id, subject.subject_name) for subject in subjects]
    except:
        subject_list = []

    # For Displaying Staff
    try:
        staffs = Staffs.objects.all()
        staff_list = [(staff.admin.id, f"{staff.admin.first_name} {staff.admin.last_name}") for staff in staffs]
    except:
        staff_list = []

    # For Displaying Session Years
    try:
        session_years = SessionYearModel.objects.all()
        session_year_list = [(session_year.id, f"{session_year.session_start_year} to {session_year.session_end_year}") for session_year in session_years]
    except:
        session_year_list = []

    # Day of the Week Choices
    day_of_week_choices = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]

    # Form Fields
    course_id = forms.ChoiceField(label="Course", choices=course_list, widget=forms.Select(attrs={"class": "form-control"}))
    subject_id = forms.ChoiceField(label="Subject", choices=subject_list, widget=forms.Select(attrs={"class": "form-control"}))
    staff_id = forms.ChoiceField(label="Staff", choices=staff_list, widget=forms.Select(attrs={"class": "form-control"}))
    session_year_id = forms.ChoiceField(label="Session Year", choices=session_year_list, widget=forms.Select(attrs={"class": "form-control"}))
    day_of_week = forms.ChoiceField(label="Day of Week", choices=day_of_week_choices, widget=forms.Select(attrs={"class": "form-control"}))
    start_time = forms.TimeField(label="Start Time", widget=forms.TimeInput(attrs={"class": "form-control", "type": "time"}))
    end_time = forms.TimeField(label="End Time", widget=forms.TimeInput(attrs={"class": "form-control", "type": "time"}))
