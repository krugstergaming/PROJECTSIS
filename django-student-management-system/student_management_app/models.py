from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver



class SessionYearModel(models.Model):
    id = models.AutoField(primary_key=True)
    session_start_year = models.DateField()
    session_end_year = models.DateField()
    session_limit = models.IntegerField(blank=True, null=True)
    objects = models.Manager()



# Overriding the Default Django Auth User and adding One More Field (user_type)
class CustomUser(AbstractUser):
    user_type_data = ((1, "HOD"), (2, "Staff"), (3, "Student"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)



class AdminHOD(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Staffs(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    dob = models.DateField()  # Assuming Date of Birth is a date
    age = models.CharField(max_length=15, blank=True, null=True)
    pob = models.CharField(max_length=255)
    sex = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    civil_status = models.CharField(max_length=20, choices=[('single', 'Single'), ('married', 'Married'), ('other', 'Other')])
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # For height in meters
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # For weight in kilograms
    blood_type = models.CharField(max_length=10, blank=True, null=True)
    gsis_id = models.CharField(max_length=50, blank=True, null=True, default='N/A')
    pagibig_id = models.CharField(max_length=50, blank=True, null=True, default='N/A')
    philhealth_id = models.CharField(max_length=50, blank=True, null=True, default='N/A')
    sss_id = models.CharField(max_length=50, blank=True, null=True, default='N/A')
    tin_id = models.CharField(max_length=50, blank=True, null=True, default='N/A')
    citizenship = models.CharField(max_length=20, choices=[('filipino', 'Filipino'), ('dual', 'Dual Citizenship')])
    dual_country = models.CharField(max_length=255, blank=True, null=True)  # For specifying the country if dual citizenship
    
    # permanent_address
    permanent_address = models.TextField(blank=True, null=True)
    
    # Residential address

    telephone_no = models.CharField(max_length=20, blank=True, null=True)
    cellphone_no = models.CharField(max_length=20, blank=True, null=True)
    email_address = models.EmailField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


    # def __str__(self):
	#     return self.GradeLevel_name


class Curriculums(models.Model):
    id = models.AutoField(primary_key=True)
    curriculum_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class GradeLevel(models.Model):
    id = models.AutoField(primary_key=True)
    GradeLevel_name = models.CharField(max_length=255)
    curriculum_id = models.ForeignKey(Curriculums, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Subjects(models.Model):
    id = models.AutoField(primary_key=True)
    subject_one = models.CharField(max_length=255, blank=True, null=True)
    subject_two = models.CharField(max_length=255, blank=True, null=True)
    subject_three = models.CharField(max_length=255, blank=True, null=True)
    subject_four = models.CharField(max_length=255, blank=True, null=True)
    subject_five = models.CharField(max_length=255, blank=True, null=True)
    subject_six = models.CharField(max_length=255, blank=True, null=True)
    subject_seven = models.CharField(max_length=255, blank=True, null=True)
    subject_eight = models.CharField(max_length=255, blank=True, null=True)
    subject_nine = models.CharField(max_length=255, blank=True, null=True)
    subject_ten = models.CharField(max_length=255, blank=True, null=True)

    GradeLevel_id = models.ForeignKey(GradeLevel, on_delete=models.CASCADE, default=1)

    curriculum_id = models.ForeignKey(Curriculums, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Section(models.Model):
    id = models.AutoField(primary_key=True)
    section_name = models.CharField(max_length=255)
    section_limit = models.IntegerField(blank=True, null=True)
    GradeLevel_id = models.ForeignKey(GradeLevel, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Load(models.Model):
    id = models.AutoField(primary_key=True)
    curriculum_id = models.ForeignKey(Curriculums, on_delete=models.CASCADE)
    GradeLevel_id = models.ForeignKey(GradeLevel, on_delete=models.CASCADE, default=1)
    subject_id = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    staff_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    section_id = models.ForeignKey(Section, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Students(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    suffix = models.CharField(max_length=20, blank=True, null=True)
    student_number = models.CharField(max_length=8, unique=True, editable=False, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    profile_pic = models.FileField(upload_to='profile_pics/', blank=True, null=True)
    address = models.TextField()

    GradeLevel_id = models.ForeignKey(GradeLevel, on_delete=models.DO_NOTHING, default=1)
    
    session_year_id = models.ForeignKey(SessionYearModel, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    grade_level = models.CharField(max_length=20, blank=True, null=True)
    nickname = models.CharField(max_length=50, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    place_of_birth = models.CharField(max_length=100, blank=True, null=True)
    nationality = models.CharField(max_length=50, blank=True, null=True)
    religion = models.CharField(max_length=50, blank=True, null=True)
    rank_in_family = models.IntegerField(blank=True, null=True)
    telephone_nos = models.CharField(max_length=20, blank=True, null=True)
    mobile_phone_nos = models.CharField(max_length=20, blank=True, null=True)
    is_covid_vaccinated = models.BooleanField(default=False)
    date_of_vaccination = models.DateField(blank=True, null=True)
    Enrollment_status = models.CharField(max_length=255, blank=True, null=True)
    objects = models.Manager()


class ParentGuardian(models.Model):
    students_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    father_name = models.CharField(max_length=100, blank=True, null=True)
    father_occupation = models.CharField(max_length=100, blank=True, null=True)
    mother_name = models.CharField(max_length=100, blank=True, null=True)
    mother_occupation = models.CharField(max_length=100, blank=True, null=True)
    guardian_name = models.CharField(max_length=100, blank=True, null=True)
    guardian_occupation = models.CharField(max_length=100, blank=True, null=True)
    objects = models.Manager()


class PreviousSchool(models.Model):
    students_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    school_name = models.CharField(max_length=100, blank=True, null=True)
    school_address = models.CharField(max_length=255, blank=True, null=True)
    grade_level = models.CharField(max_length=20, blank=True, null=True)
    school_year_attended = models.CharField(max_length=20, blank=True, null=True)
    teacher_name = models.CharField(max_length=100, blank=True, null=True)
    objects = models.Manager()

class EmergencyContact(models.Model):
    students_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    relation = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    telephone_nos = models.CharField(max_length=20, blank=True, null=True)
    enrolling_teacher = models.CharField(max_length=100, blank=True, null=True)
    referred_by = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    objects = models.Manager()

class Schedule(models.Model):
    id = models.AutoField(primary_key=True)
    subject_id = models.ForeignKey(Subjects, on_delete=models.CASCADE)  # The subject being scheduled
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)      # The staff assigned to the subject
    GradeLevel_id = models.ForeignKey(GradeLevel, on_delete=models.CASCADE)    # The gradelevel the subject belongs to
    session_year_id = models.ForeignKey(SessionYearModel, on_delete=models.CASCADE)  # The session year
    day_of_week = models.CharField(max_length=10)                       # The day of the week (e.g., "Monday")
    start_time = models.TimeField()                                     # The start time of the class
    end_time = models.TimeField()                                       # The end time of the class
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return f"{self.subject_id.subject_name} - {self.GradeLevel_id.GradeLevel_name} - {self.day_of_week} ({self.start_time} to {self.end_time})"


class Attendance(models.Model):
    # Subject Attendance
    id = models.AutoField(primary_key=True)
    subject_id = models.ForeignKey(Subjects, on_delete=models.DO_NOTHING)
    attendance_date = models.DateField()
    session_year_id = models.ForeignKey(SessionYearModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class AttendanceReport(models.Model):
    # Individual Student Attendance
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.DO_NOTHING)
    attendance_id = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class LeaveReportStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class LeaveReportStaff(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class FeedBackStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class FeedBackStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()



class NotificationStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class NotificationStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    stafff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class StudentResult(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    
    subject_first_quarter = models.FloatField(default=0)
    subject_second_quarter = models.FloatField(default=0)
    subject_third_quarter = models.FloatField(default=0)
    subject_fourth_quarter = models.FloatField(default=0)
    subject_final_grade = models.FloatField(default=0)

    subject_exam_marks = models.FloatField(default=0)
    subject_assignment_marks = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class GradingConfiguration(models.Model):
    is_grading_active = models.BooleanField(default=True)

    def __str__(self):
        return "Grading is Active" if self.is_grading_active else "Grading is Inactive"


#Creating Django Signals

# It's like trigger in database. It will run only when Data is Added in CustomUser model

@receiver(post_save, sender=CustomUser)
# Now Creating a Function which will automatically insert data in HOD, Staff or Student
def create_user_profile(sender, instance, created, **kwargs):
    # if Created is true (Means Data Inserted)
    if created:
        # Check the user_type and insert the data in respective tables
        if instance.user_type == 1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type == 2:
            Staffs.objects.create(admin=instance)
        if instance.user_type == 3:
            Students.objects.create(admin=instance, GradeLevel_id=GradeLevel.objects.get(id=1), session_year_id=SessionYearModel.objects.get(id=1), address="", profile_pic="", gender="")
    

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhod.save()
    if instance.user_type == 2:
        instance.staffs.save()
    if instance.user_type == 3:
        instance.students.save()
    

