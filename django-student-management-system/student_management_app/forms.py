from django import forms 
from django.forms import Form
from student_management_app.models import YearLevel, SessionYearModel


class DateInput(forms.DateInput):
    input_type = "date"


class AddStudentForm(forms.Form):
    lrn = forms.IntegerField(label="LRN", widget=forms.NumberInput(attrs={"class":"form-control"}))
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    password = forms.CharField(label="Password", max_length=50, widget=forms.PasswordInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    nickname = forms.CharField(label="Nickname", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    
    street = forms.CharField(label="Street", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    barangay = forms.CharField(label="Barangay", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    city = forms.CharField(label="City", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    region = forms.CharField(label="Region", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    
    nationality = forms.CharField(label="Nationality", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    religion = forms.CharField(label="Religion", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))

    
    #For Displaying yearlevels
    try:
        yearlevel = YearLevel.objects.all()
        yearlevel_list = []
        for yearlevel in yearlevel:
            single_yearlevel = (yearlevel.id, yearlevel.yearlevel_name)
            yearlevel_list.append(single_yearlevel)
    except:
        yearlevel_list = []
    
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

    enrollment_status = (
    (True, 'Enrolled'),
    (False, 'Not Enrolled')
    )

    yearlevel_id = forms.ChoiceField(label="Yearlevel", choices=yearlevel_list, widget=forms.Select(attrs={"class":"form-control"}))
    gender = forms.ChoiceField(label="Gender", choices=gender_list, widget=forms.Select(attrs={"class":"form-control"}))
    session_year_id = forms.ChoiceField(label="Session Year", choices=session_year_list, widget=forms.Select(attrs={"class":"form-control"}))
    is_enrolled = forms.ChoiceField(label="Enrollment Status", choices=enrollment_status, widget=forms.Select(attrs={"class":"form-control"}))
    # session_start_year = forms.DateField(label="Session Start", widget=DateInput(attrs={"class":"form-control"}))
    # session_end_year = forms.DateField(label="Session End", widget=DateInput(attrs={"class":"form-control"}))
    profile_pic = forms.FileField(label="Profile Pic", required=False, widget=forms.FileInput(attrs={"class":"form-control"}))
        
    def clean(self):
        cleaned_data = super().clean()
        street = cleaned_data.get("street")
        barangay = cleaned_data.get("barangay")
        city = cleaned_data.get("city")
        region = cleaned_data.get("region")

        # Concatenate the address parts into one field
        address = f"{street}, {barangay}, {city}, {region}"
        
        # Add the concatenated address back into the cleaned_data dictionary
        cleaned_data["address"] = address
        
        return cleaned_data




class EditStudentForm(forms.Form):
    lrn = forms.IntegerField(label="LRN", widget=forms.NumberInput(attrs={"class":"form-control"}))
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    
    street = forms.CharField(label="Street", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    barangay = forms.CharField(label="Barangay", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    city = forms.CharField(label="City", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    region = forms.CharField(label="Region", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    
    nationality = forms.CharField(label="Nationality", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    religion = forms.CharField(label="Religion", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    # For Displaying yearlevels
    try:
        yearlevels = YearLevel.objects.all()
        yearlevel_list = []
        for yearlevel in yearlevels:
            single_yearlevel = (yearlevel.id, yearlevel.yearlevel_name)
            yearlevel_list.append(single_yearlevel)
    except:
        yearlevel_list = []

    # For Displaying Session Years
    try:
        session_years = SessionYearModel.objects.all()
        session_year_list = []
        for session_year in session_years:
            single_session_year = (session_year.id, str(session_year.session_start_year) + " to " + str(session_year.session_end_year))
            session_year_list.append(single_session_year)
    except:
        session_year_list = []

    gender_list = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    yearlevel_id = forms.ChoiceField(label="Yearlevel", choices=yearlevel_list, widget=forms.Select(attrs={"class":"form-control"}))
    gender = forms.ChoiceField(label="Gender", choices=gender_list, widget=forms.Select(attrs={"class":"form-control"}))
    session_year_id = forms.ChoiceField(label="Session Year", choices=session_year_list, widget=forms.Select(attrs={"class":"form-control"}))
    profile_pic = forms.FileField(label="Profile Pic", required=False, widget=forms.FileInput(attrs={"class":"form-control"}))
    
    def clean(self):
        cleaned_data = super().clean()
        street = cleaned_data.get("street")
        barangay = cleaned_data.get("barangay")
        city = cleaned_data.get("city")
        region = cleaned_data.get("region")

        # Concatenate the address parts into one field
        address = f"{street}, {barangay}, {city}, {region}"
        
        # Add the concatenated address back into the cleaned_data dictionary
        cleaned_data["address"] = address
        
        return cleaned_data


class AddStaffForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="Password", max_length=50, widget=forms.PasswordInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))

    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    
    employee_no = forms.IntegerField(label="Employee Number", widget=forms.NumberInput(attrs={"class": "form-control"}))
    registration_no = forms.IntegerField(label="Registration Number", widget=forms.NumberInput(attrs={"class": "form-control"}))
    registration_date = forms.DateField(label="Registration Date", widget=forms.DateInput(attrs={"class":"form-control", "type":"date"}))

    street = forms.CharField(label="Street", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    barangay = forms.CharField(label="Barangay", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    city = forms.CharField(label="City", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    region = forms.CharField(label="Region", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))

    profile_pic = forms.FileField(label="Profile Pic", required=False, widget=forms.FileInput(attrs={"class":"form-control"}))
    teacher_license = forms.FileField(label="Teacher License", required=False, widget=forms.FileInput(attrs={"class":"form-control"}))
    signature = forms.FileField(label="Signature", required=False, widget=forms.FileInput(attrs={"class":"form-control"}))

    def clean(self):
        cleaned_data = super().clean()
        street = cleaned_data.get("street")
        barangay = cleaned_data.get("barangay")
        city = cleaned_data.get("city")
        region = cleaned_data.get("region")

        # Concatenate the address parts into one field
        address = f"{street}, {barangay}, {city}, {region}"
        
        # Add the concatenated address back into the cleaned_data dictionary
        cleaned_data["address"] = address
        
        return cleaned_data