from django import forms 
from django.forms import Form
from student_management_app.models import GradeLevel, SessionYearModel, Subjects, Staffs


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
    age = forms.IntegerField(label="Age", widget=forms.NumberInput(attrs={"class": "form-control"}))
    date_of_birth = forms.DateField(label="Date of Birth", widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}))
    place_of_birth = forms.CharField(label="Place of Birth", max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
    nationality = forms.CharField(label="Nationality", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    religion = forms.CharField(label="Religion", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    rank_in_family = forms.IntegerField(label="Rank in the Family", required=False, widget=forms.NumberInput(attrs={"class": "form-control"}))
    telephone_nos = forms.CharField(label="Telephone Nos", max_length=20, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    mobile_phone_nos = forms.CharField(label="Mobile Phone Nos", max_length=20, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    is_covid_vaccinated = forms.ChoiceField(label="Is COVID Vaccinated?", choices=[(True, 'Yes'), (False, 'No')], widget=forms.Select(attrs={"class": "form-control"}))
    date_of_vaccination = forms.DateField(label="Date of Vaccination", required=False, widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}))

    #For Displaying GradeLevel
    try:
        gradelevels = GradeLevel.objects.all()
        course_list = [(gradelevel.id, gradelevel.GradeLevel_name) for gradelevel in gradelevels]
    except Exception as e:
        print("Error fetching gradelevels:", e)
        course_list = []
    
    #For Displaying Session Years
    try:
        session_years = SessionYearModel.objects.all()
        session_year_list = [(session_year.id, f"{session_year.session_start_year} to {session_year.session_end_year}") for session_year in session_years]
    except Exception as e:
        print("Error fetching session years:", e)
        session_year_list = []

    GradeLevel_id = forms.ChoiceField(label="GradeLevel", choices=course_list, widget=forms.Select(attrs={"class":"form-control"}), error_messages={'required': 'Please select a valid gradelevel.'})
    session_year_id = forms.ChoiceField(label="School Year", choices=session_year_list, widget=forms.Select(attrs={"class":"form-control"}))

    def __init__(self, *args, **kwargs):
        super(AddStudentForm, self).__init__(*args, **kwargs)
        
        # Add a placeholder choice at the beginning
        self.fields['GradeLevel_id'].choices = [('', 'Select a GradeLevel')] + [(gradelevel.id, gradelevel.GradeLevel_name) for gradelevel in GradeLevel.objects.all()]
        self.fields['session_year_id'].choices = [('', 'Select a School Year')] + [(session_year.id, f"{session_year.session_start_year} to {session_year.session_end_year}") for session_year in SessionYearModel.objects.all()]

    
    # session_start_year = forms.DateField(label="Session Start", widget=DateInput(attrs={"class":"form-control"}))
    # session_end_year = forms.DateField(label="Session End", widget=DateInput(attrs={"class":"form-control"}))
    profile_pic = forms.FileField(label="Profile Pic", required=False, widget=forms.FileInput(attrs={"class":"form-control"}))


class ParentGuardianForm(forms.Form):
    father_name = forms.CharField(label="Father's Name", max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
    father_occupation = forms.CharField(label="Father's Occupation", max_length=100, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    mother_name = forms.CharField(label="Mother's Name", max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
    mother_occupation = forms.CharField(label="Mother's Occupation", max_length=100, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    guardian_name = forms.CharField(label="Guardian's Name", max_length=100, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    guardian_occupation = forms.CharField(label="Guardian's Occupation", max_length=100, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))


class PreviousSchoolForm(forms.Form):
    school_name = forms.CharField(label="School Name", max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
    school_address = forms.CharField(label="School Address", max_length=255, widget=forms.TextInput(attrs={"class": "form-control"}))
    grade_level = forms.CharField(label="Grade/Level", max_length=20, widget=forms.TextInput(attrs={"class": "form-control"}))
    sy_attended = forms.CharField(label="School Year Attended", max_length=20, widget=forms.TextInput(attrs={"class": "form-control"}))
    teacher_name = forms.CharField(label="Teacher's Name", max_length=100, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))


class EmergencyContactForm(forms.Form):
    contact_name = forms.CharField(label="Name", max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
    contact_relation = forms.CharField(label="Relation", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    contact_address = forms.CharField(label="Address", max_length=255, widget=forms.TextInput(attrs={"class": "form-control"}))
    contact_telephone = forms.CharField(label="Telephone Nos", max_length=20, widget=forms.TextInput(attrs={"class": "form-control"}))
    contact_referred_by = forms.CharField(label="Referred By", max_length=100, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))


class EditStudentForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    
    gender_list = (
        ('Male','Male'),
        ('Female','Female')
    )
    gender = forms.ChoiceField(label="Gender", choices=gender_list, widget=forms.Select(attrs={"class":"form-control"}))
    
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    age = forms.IntegerField(label="Age", widget=forms.NumberInput(attrs={"class": "form-control"}))
    date_of_birth = forms.DateField(label="Date of Birth", widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}))
    place_of_birth = forms.CharField(label="Place of Birth", max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
    nationality = forms.CharField(label="Nationality", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    religion = forms.CharField(label="Religion", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    rank_in_family = forms.IntegerField(label="Rank in the Family", required=False, widget=forms.NumberInput(attrs={"class": "form-control"}))
    telephone_nos = forms.CharField(label="Telephone Nos", max_length=20, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    mobile_phone_nos = forms.CharField(label="Mobile Phone Nos", max_length=20, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    is_covid_vaccinated = forms.ChoiceField(label="Is COVID Vaccinated?", choices=[(True, 'Yes'), (False, 'No')], widget=forms.Select(attrs={"class": "form-control"}))
    date_of_vaccination = forms.DateField(label="Date of Vaccination", required=False, widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}))


    #For Displaying GradeLevel
    try:
        gradelevels = GradeLevel.objects.all()
        course_list = []
        for gradelevel in gradelevels:
            single_course = (gradelevel.id, gradelevel.GradeLevel_name)
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
    
    GradeLevel_id = forms.ChoiceField(label="GradeLevel", choices=course_list, widget=forms.Select(attrs={"class":"form-control"}))
    
    session_year_id = forms.ChoiceField(label="Session Year", choices=session_year_list, widget=forms.Select(attrs={"class":"form-control"}))
    # session_start_year = forms.DateField(label="Session Start", widget=DateInput(attrs={"class":"form-control"}))
    # session_end_year = forms.DateField(label="Session End", widget=DateInput(attrs={"class":"form-control"}))
    profile_pic = forms.FileField(label="Profile Pic", required=False, widget=forms.FileInput(attrs={"class":"form-control"}))


class AddScheduleForm(forms.Form):
    # Select the GradeLevel
    try:
        gradelevels = GradeLevel.objects.all()
        course_list = [(gradelevel.id, gradelevel.GradeLevel_name) for gradelevel in gradelevels]
    except Exception as e:
        print("Error fetching gradelevels:", e)
        course_list = []
    
    GradeLevel_id = forms.ChoiceField(
        label="GradeLevel", 
        choices=course_list, 
        widget=forms.Select(attrs={"class": "form-control"})
    )

    # Select the Subject
    try:
        subjects = Subjects.objects.all()
        subject_list = [(subject.id, subject.subject_one) for subject in subjects]
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
        label="School Year", 
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
        self.fields['GradeLevel_id'].choices = [('', 'Select a GradeLevel')] + [(gradelevel.id, gradelevel.GradeLevel_name) for gradelevel in GradeLevel.objects.all()]
        self.fields['subject_id'].choices = [('', 'Select a Subject')] + [(subject.id, subject.subject_one) for subject in Subjects.objects.all()]
        self.fields['staff_id'].choices = [('', 'Select a Staff Member')] + [(staff.id, f"{staff.admin.first_name} {staff.admin.last_name}") for staff in Staffs.objects.all()]
        self.fields['session_year_id'].choices = [('', 'Select a School Year')] + [(session_year.id, f"{session_year.session_start_year} to {session_year.session_end_year}") for session_year in SessionYearModel.objects.all()]


class EditScheduleForm(forms.Form):
    # For Displaying GradeLevel
    try:
        gradelevels = GradeLevel.objects.all()
        course_list = [(gradelevel.id, gradelevel.GradeLevel_name) for gradelevel in gradelevels]
    except:
        course_list = []

    # For Displaying Subjects
    try:
        subjects = Subjects.objects.all()
        subject_list = [(subject.id, subject.subject_one) for subject in subjects]
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
    GradeLevel_id = forms.ChoiceField(label="GradeLevel", choices=course_list, widget=forms.Select(attrs={"class": "form-control"}))
    subject_id = forms.ChoiceField(label="Subject", choices=subject_list, widget=forms.Select(attrs={"class": "form-control"}))
    staff_id = forms.ChoiceField(label="Staff", choices=staff_list, widget=forms.Select(attrs={"class": "form-control"}))
    session_year_id = forms.ChoiceField(label="School Year", choices=session_year_list, widget=forms.Select(attrs={"class": "form-control"}))
    day_of_week = forms.ChoiceField(label="Day of Week", choices=day_of_week_choices, widget=forms.Select(attrs={"class": "form-control"}))
    start_time = forms.TimeField(label="Start Time", widget=forms.TimeInput(attrs={"class": "form-control", "type": "time"}))
    end_time = forms.TimeField(label="End Time", widget=forms.TimeInput(attrs={"class": "form-control", "type": "time"}))
