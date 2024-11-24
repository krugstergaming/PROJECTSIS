from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class SessionYearModel(models.Model):
    id = models.AutoField(primary_key=True)
    session_start_year = models.DateField(blank=True, null=True)
    session_end_year = models.DateField(blank=True, null=True)
    session_limit = models.IntegerField(blank=True, null=True)
    session_status = models.CharField(max_length=255)
    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

# Overriding the Default Django Auth User and adding One More Field (user_type)
class CustomUser(AbstractUser):
    user_type_data = ((1, "HOD"), (2, "Staff"), (3, "Student"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)
    last_login_session_key = models.CharField(max_length=40, blank=True, null=True)


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
    suffix = models.CharField(max_length=20, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)  # Assuming Date of Birth is a date
    age = models.CharField(max_length=15, blank=True, null=True)
    pob = models.CharField(max_length=255)
    sex = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    civil_status = models.CharField(max_length=20, choices=[('single', 'Single'), ('married', 'Married'), ('other', 'Other')])
    citizenship = models.CharField(max_length=20, default='Filipino', blank=True, null=True)
    dual_country = models.CharField(max_length=255, blank=True, null=True)  # For specifying the country if dual citizenship
    max_load = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class staff_contact_info(models.Model):
    staffs_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    region = models.CharField(max_length=255, blank=True, null=True)
    province = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    barangay = models.CharField(max_length=255, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    telephone_no = models.CharField(max_length=20, blank=True, null=True)
    cellphone_no = models.CharField(max_length=20, blank=True, null=True)
    emergency_contact = models.CharField(max_length=20, blank=True, null=True)
    emergency_relationship = models.CharField(max_length=255, blank=True, null=True)
    medical_condition = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class staff_employment_info(models.Model):
    staffs_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    employee_number = models.CharField(max_length=12, unique=True, editable=False, blank=True, null=True)
    employee_type = models.CharField(max_length=255, blank=True, null=True)
    position = models.CharField(max_length=255, blank=True, null=True)
    employment_status = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class staff_physical_info(models.Model):
    staffs_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    blood_type = models.CharField(max_length=10, blank=True, null=True)
    height = models.CharField(max_length=10, blank=True, null=True)  # For height in meters
    weight = models.CharField(max_length=10, blank=True, null=True)  # For weight in kilograms
    eye_color = models.CharField(max_length=255, blank=True, null=True)
    hair_color = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class staff_government_ID_info(models.Model):
    staffs_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    gsis_id = models.CharField(max_length=50, blank=True, null=True, default='N/A')
    pagibig_id = models.CharField(max_length=50, blank=True, null=True, default='N/A')
    philhealth_id = models.CharField(max_length=50, blank=True, null=True, default='N/A')
    sss_id = models.CharField(max_length=50, blank=True, null=True, default='N/A')
    tin_id = models.CharField(max_length=50, blank=True, null=True, default='N/A')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Staffs_Educ_Background(models.Model):
    staffs_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    HEA = models.CharField(max_length=255, blank=True, null=True) # Highest Educational Attainment
    Cert_License = models.CharField(max_length=255, blank=True, null=True)
    teaching_exp = models.CharField(max_length=255, blank=True, null=True)
    skills_competencies = models.CharField(max_length=255, blank=True, null=True)
    language_spoken = models.CharField(max_length=255, blank=True, null=True)
    preferred_subject = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Curriculums(models.Model):
    id = models.AutoField(primary_key=True)
    curriculum_name = models.CharField(max_length=255)
    curriculum_description = models.TextField(max_length=255)
    curriculum_status = models.CharField(max_length=255)
    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Classroom(models.Model):
    id = models.AutoField(primary_key=True)
    classroom_name = models.CharField(max_length=255)
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

class Students(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    student_number = models.CharField(max_length=12, unique=True, editable=False, blank=True, null=True)
    GradeLevel_id = models.ForeignKey(GradeLevel, on_delete=models.CASCADE, default=1)
    session_year_id = models.ForeignKey(SessionYearModel, on_delete=models.CASCADE)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    suffix = models.CharField(max_length=20, blank=True, null=True)
    nickname = models.CharField(max_length=50, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    pob = models.CharField(max_length=100, blank=True, null=True)
    sex = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    address = models.TextField()
    nationality = models.CharField(max_length=50, blank=True, null=True)
    religion = models.CharField(max_length=50, blank=True, null=True)
    rank_in_family = models.IntegerField(blank=True, null=True)
    telephone_nos = models.CharField(max_length=20, blank=True, null=True)
    mobile_phone_nos = models.CharField(max_length=20, blank=True, null=True)
    is_covid_vaccinated = models.BooleanField(default=False)
    date_of_vaccination = models.DateField(blank=True, null=True)
    student_status = models.CharField(max_length=255, blank=True, null=True)
    profile_pic = models.FileField(upload_to='profile_pics/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Enrollment_voucher(models.Model):
    id = models.AutoField(primary_key=True)
    GradeLevel_id = models.ForeignKey(GradeLevel, on_delete=models.CASCADE, default=1)
    registration_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    misc_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tuition_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Enrollment(models.Model):
    id = models.AutoField(primary_key=True)

    GradeLevel_id = models.ForeignKey(GradeLevel, on_delete=models.CASCADE, default=1)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)

    registration_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    misc_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tuition_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    downpayment = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True, null=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True, null=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True, null=True)
    installment_option = models.CharField(max_length=50, default='Monthly', blank=True, null=True)
    installment_payment = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True, null=True)
    assessed_by = models.CharField(max_length=100, blank=True, null=True)
    assessed_date = models.DateField(blank=True, null=True)
    payment_received_by = models.CharField(max_length=100, blank=True, null=True)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_date = models.DateField(blank=True, null=True)
    enrollment_status = models.CharField(max_length=20, default='Pending')
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Attachment(models.Model):
    enrollment = models.ForeignKey('Enrollment', on_delete=models.CASCADE, related_name='attachments')
    id_picture_file = models.FileField(upload_to='attachments/', blank=True, null=True)
    psa_file = models.FileField(upload_to='attachments/', blank=True, null=True)
    form_138_file = models.FileField(upload_to='attachments/', blank=True, null=True)
    attachment_remarks = models.CharField(max_length=255, blank=True, null=True)  
    uploaded_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class BalancePayment(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='payments')
    payment_balance_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_balance_date = models.DateField(blank=True, null=True)
    past_balance = models.DecimalField(max_digits=10, decimal_places=2)
    payment_balance_remarks = models.TextField(blank=True, null=True)

class StudentPromotionHistory(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    previous_grade = models.ForeignKey(GradeLevel, related_name='previous_grade', on_delete=models.SET_NULL, null=True)
    new_grade = models.ForeignKey(GradeLevel, related_name='new_grade', on_delete=models.SET_NULL, null=True)
    promotion_date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student} promoted from {self.previous_grade} to {self.new_grade} on {self.promotion_date}"
    objects = models.Manager()

class Section(models.Model):
    id = models.AutoField(primary_key=True)
    GradeLevel_id = models.ForeignKey(GradeLevel, on_delete=models.CASCADE, default=1)
    section_name = models.CharField(max_length=255)
    section_soft_limit = models.IntegerField(blank=True, null= True)
    section_limit = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Subjects(models.Model):
    id = models.AutoField(primary_key=True)

    curriculum_id = models.ForeignKey(Curriculums, on_delete=models.CASCADE)
    GradeLevel_id = models.ForeignKey(GradeLevel, on_delete=models.CASCADE, default=1)
    subject_name = models.CharField(max_length=255, blank=True, null=True)
    subject_description = models.CharField(max_length=255, blank=True, null=True)
    subject_code = models.CharField(max_length=255, blank=True, null=True)
    subject_hours = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class AssignSection(models.Model):
    id = models.AutoField(primary_key=True)
    GradeLevel_id = models.ForeignKey(GradeLevel, on_delete=models.CASCADE, default=1)
    section_id = models.ForeignKey(Section, on_delete=models.CASCADE)
    Student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Load(models.Model):
    id = models.AutoField(primary_key=True)
    session_year_id = models.ForeignKey(SessionYearModel, on_delete=models.CASCADE)
    curriculum_id = models.ForeignKey(Curriculums, on_delete=models.CASCADE)
    AssignSection_id = models.ForeignKey(AssignSection, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    staff_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_advisory = models.BooleanField(default=False)  # BooleanField with True/False for Yes/No
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Schedule(models.Model):
    id = models.AutoField(primary_key=True)
    load_id = models.ForeignKey(Load, on_delete=models.CASCADE)  
    classroom_id = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=10)                       
    start_time = models.TimeField()                                     
    end_time = models.TimeField()                                       
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return f"{self.load_id.subject_id.subject_name} - {self.load_id.GradeLevel_id.GradeLevel_name} - {self.day_of_week} ({self.start_time} to {self.end_time})"
    
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
    previous_school_name = models.CharField(max_length=100, blank=True, null=True)
    previous_school_address = models.CharField(max_length=255, blank=True, null=True)
    previous_grade_level = models.CharField(max_length=20, blank=True, null=True)
    previous_school_year_attended = models.CharField(max_length=255, blank=True, null=True)
    previous_teacher_name = models.CharField(max_length=100, blank=True, null=True)
    objects = models.Manager()

class EmergencyContact(models.Model):
    students_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_relationship = models.CharField(max_length=50, blank=True, null=True)
    emergency_contact_address = models.CharField(max_length=255, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True, null=True)
    emergency_enrolling_teacher = models.CharField(max_length=100, blank=True, null=True)
    emergency_referred_by = models.CharField(max_length=100, blank=True, null=True)
    emergency_date = models.DateField(blank=True, null=True)
    objects = models.Manager()

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
    load_id = models.ForeignKey(Load, on_delete=models.CASCADE)
    
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
            Students.objects.create(admin=instance, GradeLevel_id=GradeLevel.objects.get(id=1), session_year_id=SessionYearModel.objects.get(id=1), address="", profile_pic="", sex="")
    

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhod.save()
    if instance.user_type == 2:
        instance.staffs.save()
    if instance.user_type == 3:
        instance.students.save()
    

