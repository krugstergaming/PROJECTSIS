from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
from django.utils.timezone import now
from django.contrib.auth.hashers import make_password

from student_management_app.models import CustomUser, Staffs, StudentPromotionHistory, Curriculums, GradeLevel, Subjects, Section, AssignSection, Load, Schedule, Students, SessionYearModel, FeedBackStudent, FeedBackStaffs, LeaveReportStudent, LeaveReportStaff, Attendance, AttendanceReport, GradingConfiguration, ParentGuardian, PreviousSchool, EmergencyContact
from .forms import EditStudentForm, AddScheduleForm, EditScheduleForm


def admin_home(request):
    all_student_count = Students.objects.all().count()
    subject_count = Subjects.objects.all().count()
    gradelevel_count = GradeLevel.objects.all().count()
    staff_count = Staffs.objects.all().count()

    # Total Subjects and students in Each GradeLevel
    gradelevel_all = GradeLevel.objects.all()
    GradeLevel_name_list = []
    subject_count_list = []
    student_count_list_in_gradelevel = []

    for gradelevel in gradelevel_all:
        subjects = Subjects.objects.filter(GradeLevel_id=gradelevel.id).count()
        students = Students.objects.filter(GradeLevel_id=gradelevel.id).count()
        GradeLevel_name_list.append(gradelevel.GradeLevel_name)
        subject_count_list.append(subjects)
        student_count_list_in_gradelevel.append(students)
    
    subject_all = Subjects.objects.all()
    subject_list = []
    student_count_list_in_subject = []
    for subject in subject_all:
        gradelevel = GradeLevel.objects.get(id=subject.GradeLevel_id.id)
        student_count = Students.objects.filter(GradeLevel_id=gradelevel.id).count()
        subject_list.append(subject.subject_name)
        student_count_list_in_subject.append(student_count)
    
    # For Saffs
    staff_attendance_present_list=[]
    staff_attendance_leave_list=[]
    staff_name_list=[]

    staffs = Staffs.objects.all()
    for staff in staffs:
        # subject_ids = Subjects.objects.filter(staff_id=staff.admin.id)
        # attendance = Attendance.objects.filter(subject_id__in=subject_ids).count()
        leaves = LeaveReportStaff.objects.filter(staff_id=staff.id, leave_status=1).count()
        # staff_attendance_present_list.append(attendance)
        staff_attendance_leave_list.append(leaves)
        staff_name_list.append(staff.admin.first_name)

    # For Students
    student_attendance_present_list=[]
    student_attendance_leave_list=[]
    student_name_list=[]

    students = Students.objects.all()
    for student in students:
        attendance = AttendanceReport.objects.filter(student_id=student.id, status=True).count()
        absent = AttendanceReport.objects.filter(student_id=student.id, status=False).count()
        leaves = LeaveReportStudent.objects.filter(student_id=student.id, leave_status=1).count()
        student_attendance_present_list.append(attendance)
        student_attendance_leave_list.append(leaves+absent)
        student_name_list.append(student.admin.first_name)


    context={
        "all_student_count": all_student_count,
        "subject_count": subject_count,
        "gradelevel_count": gradelevel_count,
        "staff_count": staff_count,
        "GradeLevel_name_list": GradeLevel_name_list,
        "subject_count_list": subject_count_list,
        "student_count_list_in_gradelevel": student_count_list_in_gradelevel,
        "subject_list": subject_list,
        "student_count_list_in_subject": student_count_list_in_subject,
        "staff_attendance_present_list": staff_attendance_present_list,
        "staff_attendance_leave_list": staff_attendance_leave_list,
        "staff_name_list": staff_name_list,
        "student_attendance_present_list": student_attendance_present_list,
        "student_attendance_leave_list": student_attendance_leave_list,
        "student_name_list": student_name_list,
    }
    return render(request, "hod_template/home_content.html", context)


def add_staff(request):
    return render(request, "hod_template/add_staff_template.html")

def add_staff_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect('add_staff')
    else:
        try:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            email = request.POST.get('email')
            max_laod = request.poST.get('max_load')
            middle_name = request.POST.get('middle_name')
            dob = request.POST.get('dob')
            age = request.POST.get('age')
            pob = request.POST.get('pob')
            sex = request.POST.get('sex')
            civil_status = request.POST.get('civil_status')
            height = request.POST.get('height')
            weight = request.POST.get('weight')
            blood_type = request.POST.get('blood_type')
            gsis_id = request.POST.get('gsis_id')
            pagibig_id = request.POST.get('pagibig_id')
            philhealth_id = request.POST.get('philhealth_id')
            sss_id = request.POST.get('sss_id')
            tin_id = request.POST.get('tin_id')
            citizenship = request.POST.get('citizenship')
            dual_country = request.POST.get('dual_country')
            permanent_address = request.POST.get('permanent_address')
            telephone_no = request.POST.get('telephone_no')
            cellphone_no = request.POST.get('cellphone_no')

            # Generate a predefined password based on staff details
            current_year = now().year
            predefined_password = f"{first_name.lower()}.{last_name.lower()}.{current_year}"

            # Create Staff User
            user = CustomUser.objects.create_user(
                username=username,
                password=make_password(predefined_password),  # Use hashed password
                email=email,
                first_name=first_name,
                last_name=last_name,
                user_type=2
            )
            user.staffs.max_laod = max_laod
            user.staffs.middle_name = middle_name
            user.staffs.dob = dob
            user.staffs.age = age
            user.staffs.pob = pob
            user.staffs.sex = sex
            user.staffs.civil_status = civil_status
            user.staffs.height = height
            user.staffs.weight = weight
            user.staffs.blood_type = blood_type
            user.staffs.gsis_id = gsis_id
            user.staffs.pagibig_id = pagibig_id
            user.staffs.philhealth_id = philhealth_id
            user.staffs.sss_id = sss_id
            user.staffs.tin_id = tin_id
            user.staffs.citizenship = citizenship
            user.staffs.dual_country = dual_country
            user.staffs.permanent_address = permanent_address
            user.staffs.telephone_no = telephone_no
            user.staffs.cellphone_no = cellphone_no
            user.save()
            
            messages.success(request, "Faculty Added Successfully! Password: " + predefined_password)
            return redirect('add_staff')
        except Exception as e:
            messages.error(request, f"Failed to Add Staff: {str(e)}")
            return redirect('add_staff')

def toggle_grading_state(request):
    grading_config, created = GradingConfiguration.objects.get_or_create(id=1)
    # Toggle the grading state
    grading_config.is_grading_active = not grading_config.is_grading_active
    grading_config.save()
    
    # Redirect back to the manage_staff view
    return redirect('manage_staff')

def manage_staff(request):
    staffs = Staffs.objects.all()
    grading_config, created = GradingConfiguration.objects.get_or_create(id=1)
    context = {
        "staffs": staffs,
        "grading_config": grading_config,  # Pass the grading configuration to the template
    }
    return render(request, "hod_template/manage_staff_template.html", context)


def edit_staff(request, staff_id):
    staff = Staffs.objects.get(admin=staff_id)

    context = {
        "staff": staff,
        "id": staff_id
    }
    return render(request, "hod_template/edit_staff_template.html", context)


def edit_staff_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        staff_id = request.POST.get('staff_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')

        try:
            # INSERTING into Customuser Model
            user = CustomUser.objects.get(id=staff_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()
            
            # INSERTING into Staff Model
            staff_model = Staffs.objects.get(admin=staff_id)
            staff_model.address = address
            staff_model.save()

            messages.success(request, "Staff Updated Successfully.")
            return redirect('/edit_staff/'+staff_id)

        except:
            messages.error(request, "Failed to Update Staff.")
            return redirect('/edit_staff/'+staff_id)


def delete_staff(request, staff_id):
    staff = Staffs.objects.get(admin=staff_id)
    try:
        staff.delete()
        messages.success(request, "Staff Deleted Successfully.")
        return redirect('manage_staff')
    except:
        messages.error(request, "Failed to Delete Staff.")
        return redirect('manage_staff')


def add_curriculum(request):
    return render(request, "hod_template/add_curriculum_template.html")

def add_curriculum_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_curriculum')
    else:
        curriculum_name = request.POST.get('curriculum_name')
        curriculum_description = request.POST.get('curriculum_description')
        curriculum_status = request.POST.get('curriculum_status')
        try:
            curriculum = Curriculums(
                curriculum_name=curriculum_name,
                curriculum_description=curriculum_description,
                curriculum_status=curriculum_status
                )
            curriculum.save()
            messages.success(request, "Curriculum Added Successfully!")
            return redirect('add_curriculum')
        except:
            messages.error(request, "Failed to Add Curriculum!")
            return redirect('add_curriculum')

def manage_curriculum(request):
    curriculums = Curriculums.objects.filter(is_archived=False)
    context = {
        "curriculums": curriculums
    }
    return render(request, 'hod_template/manage_curriculum_template.html', context)

def edit_curriculum(request, curriculum_id):
    curriculum = Curriculums.objects.get(id=curriculum_id)
    context = {
        "curriculum": curriculum,
        "id": curriculum_id
    }
    return render(request, 'hod_template/edit_curriculum_template.html', context)

def edit_curriculum_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        curriculum_id = request.POST.get('curriculum_id')
        curriculum_name = request.POST.get('curriculum_name')
        curriculum_description = request.POST.get('curriculum_description')
        curriculum_status = request.POST.get('curriculum_status')

        try:
            curriculum = Curriculums.objects.get(id=curriculum_id)
            curriculum.curriculum_name = curriculum_name
            curriculum.curriculum_description = curriculum_description
            curriculum.curriculum_status = curriculum_status
            curriculum.save()

            messages.success(request, "Curriculum Updated Successfully.")
            return redirect('/manage_curriculum/')

        except:
            messages.error(request, "Failed to Update GradeLevel.")
            return redirect('/manage_curriculum/')

def archived_curriculums(request):
    # Filter curriculums with status 'Archived'
    curriculums = Curriculums.objects.filter(is_archived=True)
    context = {
        "curriculums": curriculums
    }
    return render(request, 'hod_template/archived_curriculum_template.html', context)

def archive_curriculum(request, curriculum_id):
    curriculum = get_object_or_404(Curriculums, id=curriculum_id)
    curriculum.is_archived = True
    curriculum.curriculum_status = "Inactive"
    curriculum.save()
    messages.success(request, "Curriculum archived successfully!")
    return redirect('/manage_curriculum/')  

def unarchive_curriculum(request, curriculum_id):
    curriculum = get_object_or_404(Curriculums, id=curriculum_id)
    curriculum.is_archived = False
    curriculum.curriculum_status = "Active"
    curriculum.save()
    messages.success(request, "Curriculum unarchived successfully!")
    return redirect('/manage_curriculum/')  

def add_gradelevel(request):
    curriculums = Curriculums.objects.all()
    context = {
        "curriculums": curriculums
    }
    return render(request, "hod_template/add_gradelevel_template.html", context)

def add_gradelevel_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_gradelevel')
    else:

        GradeLevel_name = request.POST.get('GradeLevel_name')

        curriculum_id = request.POST.get('curriculum_id')
        curriculums = Curriculums.objects.get(id=curriculum_id)

        try:
            gradelevel = GradeLevel(
                GradeLevel_name=GradeLevel_name,
                curriculum_id = curriculums
                )
            gradelevel.save()
            messages.success(request, "GradeLevel Added Successfully!")
            return redirect('add_gradelevel')
        except:
            messages.error(request, "Failed to Add GradeLevel!")
            return redirect('add_gradelevel')

def manage_gradelevel(request):
    gradelevels = GradeLevel.objects.all()
    context = {
        "gradelevels": gradelevels
    }
    return render(request, 'hod_template/manage_gradelevel_template.html', context)

def edit_gradelevel(request, GradeLevel_id):
    gradelevel = GradeLevel.objects.get(id=GradeLevel_id)
    context = {
        "gradelevel": gradelevel,
        "id": GradeLevel_id
    }
    return render(request, 'hod_template/edit_gradelevel_template.html', context)

def edit_gradelevel_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        GradeLevel_id = request.POST.get('GradeLevel_id')
        GradeLevel_name = request.POST.get('gradelevel')

        try:
            gradelevel = GradeLevel.objects.get(id=GradeLevel_id)
            gradelevel.GradeLevel_name = GradeLevel_name
            gradelevel.save()

            messages.success(request, "GradeLevel Updated Successfully.")
            return redirect('/edit_gradelevel/'+GradeLevel_id)

        except:
            messages.error(request, "Failed to Update GradeLevel.")
            return redirect('/edit_gradelevel/'+GradeLevel_id)


def delete_gradelevel(request, GradeLevel_id):
    gradelevel = GradeLevel.objects.get(id=GradeLevel_id)
    try:
        gradelevel.delete()
        messages.success(request, "GradeLevel Deleted Successfully.")
        return redirect('manage_gradelevel')
    except:
        messages.error(request, "Failed to Delete GradeLevel.")
        return redirect('manage_gradelevel')


def manage_session(request):
    session_years = SessionYearModel.objects.all()
    context = {
        "session_years": session_years
    }
    return render(request, "hod_template/manage_session_template.html", context)


def add_session(request):
    return render(request, "hod_template/add_session_template.html")


def add_session_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_session')
    else:
        session_start_year = request.POST.get('session_start_year')
        session_end_year = request.POST.get('session_end_year')
        session_limit = request.POST.get('session_limit')
        session_status = request.pOST.get('session_status')

        try:
            sessionyear = SessionYearModel(
                session_start_year = session_start_year, 
                session_end_year = session_end_year,
                session_limit = session_limit,
                session_status = session_status
                )
            sessionyear.save()
            messages.success(request, "Session Year added Successfully!")
            return redirect("add_session")
        except:
            messages.error(request, "Failed to Add Session Year")
            return redirect("add_session")


def edit_session(request, session_id):
    session_year = SessionYearModel.objects.get(id=session_id)
    context = {
        "session_year": session_year
    }
    return render(request, "hod_template/edit_session_template.html", context)


def manage_section(request):
    session_years = SessionYearModel.objects.all()
    context = {
        "session_years": session_years
    }
    return render(request, "hod_template/manage_session_template.html", context)


def add_session(request):
    return render(request, "hod_template/add_session_template.html")


def edit_session_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('manage_session')
    else:
        session_id = request.POST.get('session_id')
        session_start_year = request.POST.get('session_start_year')
        session_end_year = request.POST.get('session_end_year')
        session_limit = request.POST.get('session_limit')

        try:
            session_year = SessionYearModel.objects.get(id=session_id)
            session_year.session_start_year = session_start_year
            session_year.session_end_year = session_end_year
            session_limit = session_limit
            session_year.save()

            messages.success(request, "Session Year Updated Successfully.")
            return redirect('/edit_session/'+session_id)
        except:
            messages.error(request, "Failed to Update Session Year.")
            return redirect('/edit_session/'+session_id)


def delete_session(request, session_id):
    session = SessionYearModel.objects.get(id=session_id)
    try:
        session.delete()
        messages.success(request, "Session Deleted Successfully.")
        return redirect('manage_session')
    except:
        messages.error(request, "Failed to Delete Session.")
        return redirect('manage_session')


def add_student(request):
    gradelevels = GradeLevel.objects.all()
    sessions = SessionYearModel.objects.all()
    year = datetime.now().year

    # Debug print to check current year
    print(f"Current Year: {year}")

    # Fetch the last student number starting with the current year
    last_student = Students.objects.filter(student_number__startswith=f"{year}-").order_by('-student_number').first()

    if last_student:
        # Debug print to check the last student number fetched
        print(f"Last Student Number: {last_student.student_number}")
        
        # Extract the last four digits after the dash, convert to an integer, and increment by 1
        last_number = int(last_student.student_number.split('-')[1])
        new_number = f"{year}-{str(last_number + 1).zfill(4)}"
    else:
        # Start with 0001 if no student exists for the current year
        new_number = f"{year}-0001"

    # Debug print to check the new student number
    print(f"New Student Number: {new_number}")

    context = {
        "gradelevels": gradelevels,
        "sessions": sessions,
        "student_number": new_number
    }
    return render(request, 'hod_template/add_student2_template.html', context)

def add_student_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_student')

    try:
        # Extract data from request.POST
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        middlename = request.POST.get('middle_name')

        suffix = request.POST.get("suffix")
        nickname = request.POST.get("nickname")

        email = request.POST.get('email')
        address = request.POST.get('address')
        session_year_id = request.POST.get('session_year_id')
        GradeLevel_id = request.POST.get('GradeLevel_id')
        sex = request.POST.get('sex')
        age = request.POST.get('age')
        dob = request.POST.get('dob')
        pob = request.POST.get('pob')
        nationality = request.POST.get('nationality')
        religion = request.POST.get('religion')
        rank_in_family = request.POST.get('rank_in_family')
        telephone_nos = request.POST.get('telephone_nos')
        mobile_phone_nos = request.POST.get('mobile_phone_nos')
        is_covid_vaccinated = request.POST.get('is_covid_vaccinated')
        date_of_vaccination = request.POST.get('date_of_vaccination')

        # Handle file upload for profile picture
        profile_pic_url = None
        if 'profile_pic' in request.FILES:
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)

        # Generate a predefined password based on the student's details
        current_year = now().year
        predefined_password = f"{first_name.lower()}.{last_name.lower()}.{current_year}"

        # Generate student_number
        last_student = Students.objects.filter(student_number__startswith=str(current_year)).order_by('-id').first()
        if last_student:
            last_number = int(last_student.student_number.split('-')[1])
            new_number = last_number + 1
        else:
            new_number = 1
        student_number = f"{current_year}-{new_number:04d}"

        # Create Student User
        user = CustomUser.objects.create_user(
            username=username, 
            password=make_password(predefined_password),  # Use hashed password
            email=email,
            first_name=first_name, 
            last_name=last_name, 
            user_type=3
        )
        user.students.student_number = student_number  # Set student_number
        user.students.address = address

        # Assign GradeLevel and Session Year
        gradelevel_obj = GradeLevel.objects.get(id=GradeLevel_id)
        session_year_obj = SessionYearModel.objects.get(id=session_year_id)
        user.students.GradeLevel_id = gradelevel_obj
        user.students.session_year_id = session_year_obj

        # Additional Student Details
        user.students.middle_name = middlename
        user.students.suffix = suffix
        user.students.nickname = nickname
        user.students.sex = sex
        user.students.profile_pic = profile_pic_url
        user.students.age = age
        user.students.dob = dob
        user.students.pob = pob
        user.students.nationality = nationality
        user.students.religion = religion
        user.students.rank_in_family = rank_in_family
        user.students.telephone_nos = telephone_nos
        user.students.mobile_phone_nos = mobile_phone_nos
        user.students.is_covid_vaccinated = is_covid_vaccinated
        user.students.date_of_vaccination = date_of_vaccination
        user.save()

        # Save Parent/Guardian Information
        ParentGuardian.objects.create(
            students_id=user.students,
            father_name=request.POST.get('father_name'),
            father_occupation=request.POST.get('father_occupation'),
            mother_name=request.POST.get('mother_name'),
            mother_occupation=request.POST.get('mother_occupation'),
            guardian_name=request.POST.get('guardian_name'),
            guardian_occupation=request.POST.get('guardian_occupation')
        )

        # Save Previous School Information
        PreviousSchool.objects.create(
            students_id=user.students,
            previous_school_name=request.POST.get('previous_school_name'),
            previous_school_address=request.POST.get('previous_school_address'),
            previous_grade_level=request.POST.get('previous_grade_level'),
            previous_school_year_attended=request.POST.get('previous_school_year_attended'),
            previous_teacher_name=request.POST.get('previous_teacher_name')
        )

        # Save Emergency Contact Information
        EmergencyContact.objects.create(
            students_id=user.students,
            emergency_contact_name=request.POST.get('emergency_contact_name'),
            emergency_contact_relationship=request.POST.get('emergency_contact_relationship'),
            emergency_contact_address=request.POST.get('emergency_contact_address'),
            emergency_contact_phone=request.POST.get('emergency_contact_phone'),
            emergency_enrolling_teacher=request.POST.get('emergency_enrolling_teacher'),
            emergency_date=request.POST.get('emergency_date'),
            emergency_referred_by=request.POST.get('emergency_referred_by')
        )

        messages.success(request, "Student Added Successfully! Password: " + predefined_password)
        return redirect('add_student')

    except Exception as e:
        messages.error(request, f"Failed to Add Student! Error: {str(e)}")
        return redirect('add_student')


# def promote_students(request):
#     if request.method == "POST":
#         current_grade_id = request.POST.get('current_grade')
#         next_grade_id = request.POST.get('next_grade')
        
#         try:
#             current_grade = GradeLevel.objects.get(id=current_grade_id)
#             next_grade = GradeLevel.objects.get(id=next_grade_id)
            
#             # Get all students in the current grade
#             students_to_promote = Students.objects.filter(GradeLevel_id=current_grade)
            
#             # Create a promotion history for each student
#             for student in students_to_promote:
#                 StudentPromotionHistory.objects.create(
#                     student=student,
#                     previous_grade=current_grade,
#                     new_grade=next_grade,
#                     promotion_date=timezone.now()
#                 )

#             # Promote students to the next grade
#             students_to_promote.update(GradeLevel_id=next_grade)
            
#             messages.success(request, f"All students have been promoted from {current_grade.name} to {next_grade.name}.")
#         except Exception as e:
#             messages.error(request, f"Failed to promote students. Error: {e}")
        
#     return redirect('students_list')

# def view_promotion_history(request, student_id):
#     promotion_history = StudentPromotionHistory.objects.filter(student_id=student_id)
#     return render(request, 'view_promotion_history.html', {'promotion_history': promotion_history})


def manage_student(request):
    students = Students.objects.all()
    context = {
        "students": students
    }
    return render(request, 'hod_template/manage_student_template.html', context)


def edit_student(request, student_id):
    # Adding Student ID into Session Variable
    request.session['student_id'] = student_id

    student = Students.objects.get(admin=student_id)
    form = EditStudentForm()
    # Filling the form with Data from Database
    form.fields['email'].initial = student.admin.email
    form.fields['username'].initial = student.admin.username
    form.fields['first_name'].initial = student.admin.first_name
    form.fields['last_name'].initial = student.admin.last_name
    form.fields['address'].initial = student.address
    form.fields['GradeLevel_id'].initial = student.GradeLevel_id.id
    form.fields['sex'].initial = student.sex
    form.fields['session_year_id'].initial = student.session_year_id.id

    context = {
        "id": student_id,
        "username": student.admin.username,
        "form": form
    }
    return render(request, "hod_template/edit_student_template.html", context)


def edit_student_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('/manage_student')

    student_id = request.session.get('student_id')
    if student_id is None:
        messages.error(request, "Student ID Missing!")
        return redirect('/manage_student')

    try:
        # Extract data from request.POST
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        middlename = request.POST.get('middle_name')

        suffix = request.POST.get("suffix")
        nickname = request.POST.get("nickname")

        email = request.POST.get('email')
        address = request.POST.get('address')
        session_year_id = request.POST.get('session_year_id')
        GradeLevel_id = request.POST.get('GradeLevel_id')
        sex = request.POST.get('sex')
        age = request.POST.get('age')
        dob = request.POST.get('dob')
        pob = request.POST.get('pob')
        nationality = request.POST.get('nationality')
        religion = request.POST.get('religion')
        rank_in_family = request.POST.get('rank_in_family')
        telephone_nos = request.POST.get('telephone_nos')
        mobile_phone_nos = request.POST.get('mobile_phone_nos')
        is_covid_vaccinated = request.POST.get('is_covid_vaccinated')
        date_of_vaccination = request.POST.get('date_of_vaccination')

        # Handle file upload for profile picture
        profile_pic_url = None
        if 'profile_pic' in request.FILES:
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)

        # Create Student User
        user = CustomUser.objects.create_user(
            username=username, 
            password=password, 
            email=email,
            first_name=first_name, 
            last_name=last_name, 
            user_type=3
        )
        user.students.address = address

        # Assign GradeLevel and Session Year
        gradelevel_obj = GradeLevel.objects.get(id=GradeLevel_id)
        session_year_obj = SessionYearModel.objects.get(id=session_year_id)
        user.students.GradeLevel_id = gradelevel_obj
        user.students.session_year_id = session_year_obj

        # Additional Student Details
        user.students.middle_name = middlename
        user.students.suffix = suffix
        user.students.nickname = nickname
        user.students.sex = sex
        user.students.profile_pic = profile_pic_url
        user.students.age = age
        user.students.dob = dob
        user.students.pob = pob
        user.students.nationality = nationality
        user.students.religion = religion
        user.students.rank_in_family = rank_in_family
        user.students.telephone_nos = telephone_nos
        user.students.mobile_phone_nos = mobile_phone_nos
        user.students.is_covid_vaccinated = is_covid_vaccinated
        user.students.date_of_vaccination = date_of_vaccination
        user.save()

        # Update Parent/Guardian Information
        parent_guardian = ParentGuardian.objects.get(students_id=student)
        parent_guardian.father_name = request.POST.get('father_name')
        parent_guardian.father_occupation = request.POST.get('father_occupation')
        parent_guardian.mother_name = request.POST.get('mother_name')
        parent_guardian.mother_occupation = request.POST.get('mother_occupation')
        parent_guardian.guardian_name = request.POST.get('guardian_name')
        parent_guardian.guardian_occupation = request.POST.get('guardian_occupation')
        parent_guardian.save()

        # Update Previous School Information
        previous_school = PreviousSchool.objects.get(students_id=student)
        previous_school.previous_school_name = request.POST.get('previous_school_name')
        previous_school.previous_school_address = request.POST.get('previous_school_address')
        previous_school.previous_grade_level = request.POST.get('previous_grade_level')
        previous_school.previous_school_year_attended = request.POST.get('previous_school_year_attended')
        previous_school.previous_teacher_name = request.POST.get('previous_teacher_name')
        previous_school.save()

        # Update Emergency Contact Information
        emergency_contact = EmergencyContact.objects.get(students_id=student)
        emergency_contact.emergency_contact_name = request.POST.get('emergency_contact_name')
        emergency_contact.emergency_contact_relationship = request.POST.get('emergency_contact_relationship')
        emergency_contact.emergency_contact_address = request.POST.get('emergency_contact_address')
        emergency_contact.emergency_contact_phone = request.POST.get('emergency_contact_phone')
        emergency_contact.emergency_enrolling_teacher = request.POST.get('emergency_enrolling_teacher')
        emergency_contact.emergency_date = request.POST.get('emergency_date')
        emergency_contact.emergency_referred_by = request.POST.get('emergency_referred_by')
        emergency_contact.save()

        # Clear the student_id session after updating
        del request.session['student_id']

        messages.success(request, "Student Updated Successfully!")
        return redirect('/edit_student/' + student_id)

    except Exception as e:
        messages.error(request, f"Failed to Update Student! Error: {str(e)}")
        return redirect('/edit_student/' + student_id)


def delete_student(request, student_id):
    student = Students.objects.get(admin=student_id)
    try:
        student.delete()
        messages.success(request, "Student Deleted Successfully.")
        return redirect('manage_student')
    except:
        messages.error(request, "Failed to Delete Student.")
        return redirect('manage_student')


def add_section(request):
    gradelevels = GradeLevel.objects.all()
    context = {
        "gradelevels": gradelevels
    }
    return render(request, 'hod_template/add_section_template.html', context)


def add_section_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_section')
    else:
        section_name = request.POST.get('section_name')
        section_limit = request.POST.get('section_limit')

        GradeLevel_id = request.POST.get('gradelevel')
        gradelevel = GradeLevel.objects.get(id=GradeLevel_id)
        
        try:
            section = Section(
                section_name = section_name,
                section_limit = section_limit,
                GradeLevel_id=gradelevel)
            section.save()
            messages.success(request, "Section Added Successfully!")
            return redirect('add_section')
        except:
            messages.error(request, "Failed to Add Section!")
            return redirect('add_section')

def add_subject(request):
    curriculums = Curriculums.objects.all()
    gradelevels = GradeLevel.objects.all()
    context = {
        "curriculums": curriculums,
        "gradelevels": gradelevels
        
    }
    return render(request, 'hod_template/add_subject_template.html', context)

def add_subject_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_subject')
    else:
        subject_name = request.POST.get('subject_name')
        subject_description = request.POST.get('subject_description')
        subject_code = request.POST.get('subject_code')
        subject_hours = request.POST.get('subject_hours')

        curriculum_id = request.POST.get('curriculum_id')
        curriculum_id = Curriculums.objects.get(id=curriculum_id)

        GradeLevel_id = request.POST.get('GradeLevel_id')
        GradeLevel_id = GradeLevel.objects.get(id=GradeLevel_id)
        
        try:
            subject = Subjects(subject_name=subject_name,
                               subject_description=subject_description,
                               subject_code=subject_code,
                               subject_hours=subject_hours,
                               GradeLevel_id=GradeLevel_id, 
                               curriculum_id = curriculum_id)
            subject.save()
            messages.success(request, "Subject Added Successfully!")
            return redirect('add_subject')
        except:
            messages.error(request, "Failed to Add Subject!")
            return redirect('add_subject')

def manage_subject(request):
    subjects = Subjects.objects.all()
    context = {
        "subjects": subjects
    }
    return render(request, 'hod_template/manage_subject_template.html', context)

def edit_subject(request, subject_id):
    subject = Subjects.objects.get(id=subject_id)
    gradelevels = GradeLevel.objects.all()
    staffs = CustomUser.objects.filter(user_type='2')
    context = {
        "subject": subject,
        "gradelevels": gradelevels,
        "staffs": staffs,
        "id": subject_id
    }
    return render(request, 'hod_template/edit_subject_template.html', context)

def edit_subject_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        subject_id = request.POST.get('subject_id')
        subject_name = request.POST.get('subject')
        GradeLevel_id = request.POST.get('gradelevel')
        staff_id = request.POST.get('staff')

        try:
            subject = Subjects.objects.get(id=subject_id)
            subject.subject_name = subject_name

            gradelevel = GradeLevel.objects.get(id=GradeLevel_id)
            subject.GradeLevel_id = gradelevel

            staff = CustomUser.objects.get(id=staff_id)
            subject.staff_id = staff
            
            subject.save()

            messages.success(request, "Subject Updated Successfully.")
            # return redirect('/edit_subject/'+subject_id)
            return HttpResponseRedirect(reverse("edit_subject", kwargs={"subject_id":subject_id}))

        except:
            messages.error(request, "Failed to Update Subject.")
            return HttpResponseRedirect(reverse("edit_subject", kwargs={"subject_id":subject_id}))
            # return redirect('/edit_subject/'+subject_id)

def delete_subject(request, subject_id):
    subject = Subjects.objects.get(id=subject_id)
    try:
        subject.delete()
        messages.success(request, "Subject Deleted Successfully.")
        return redirect('manage_subject')
    except:
        messages.error(request, "Failed to Delete Subject.")
        return redirect('manage_subject')

def add_assignsection(request):
    gradelevels = GradeLevel.objects.filter(id__in=Students.objects.values_list('GradeLevel_id', flat=True))
    context = {
        "gradelevels": gradelevels,
    }
    return render(request, 'hod_template/add_assignsection_template.html', context)

def load_sections_and_students(request):
    gradelevel_id = request.GET.get('gradelevel_id')
    
    # Fetch sections by GradeLevel
    sections = Section.objects.filter(GradeLevel_id=gradelevel_id)

    # Get all students in the GradeLevel who are NOT already assigned to a section
    assigned_students = AssignSection.objects.filter(GradeLevel_id=gradelevel_id).values_list('Student_id', flat=True)
    students = Students.objects.filter(GradeLevel_id=gradelevel_id).exclude(id__in=assigned_students)

    # Prepare data for response
    section_list = [{"id": section.id, "name": section.section_name} for section in sections]
    student_list = [{"id": student.id, "name": f"{student.admin.first_name} {student.admin.last_name}"} for student in students]
    
    return JsonResponse({'sections': section_list, 'students': student_list})


def add_assignsection_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_assignsection')
    
    try:
        gradelevel_id = request.POST.get('GradeLevel_id')
        gradelevel = GradeLevel.objects.get(id=gradelevel_id)

        section_id = request.POST.get('section_id')
        section = Section.objects.get(id=section_id)

        student_ids = request.POST.getlist('student_ids')  # Get multiple student IDs

        # Check if student_ids is empty
        if not student_ids:
            messages.error(request, "No students selected! Please select students to assign to this section.")
            return redirect('add_assignsection')

        # Proceed to save the assignment for each student
        for student_id in student_ids:
            student = Students.objects.get(id=student_id)

            # Create and save an AssignSection entry for each student
            assignsection = AssignSection(   
                GradeLevel_id=gradelevel, 
                section_id=section,
                Student_id=student
            )
            assignsection.save()

        messages.success(request, "Assign Section Added Successfully!")
        return redirect('add_assignsection')

    except Exception as e:
        messages.error(request, f"Failed to Assign Section! Error: {e}")
        return redirect('add_assignsection')

def add_load(request):
    # Fetch all necessary data for the context
    curriculums = Curriculums.objects.all()
    assignsections = AssignSection.objects.select_related('GradeLevel_id', 'section_id').distinct('GradeLevel_id', 'section_id')
    gradelevels = GradeLevel.objects.all()
    sections = Section.objects.all()
    subjects = Subjects.objects.all()
    
    # Use select_related to fetch related data for loads
    loads = Load.objects.select_related('curriculum_id', 'AssignSection_id', 'subject_id', 'staff_id').all()
    
    staffs = CustomUser.objects.filter(user_type='2')

    context = {
        "curriculums": curriculums,
        "assignsections": assignsections,
        "gradelevels": gradelevels,
        "sections": sections,
        "subjects": subjects,
        "staffs": staffs,
        "loads": loads,
    }
    return render(request, 'hod_template/add_load_template.html', context)

def add_load_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_load')
    else:
        try:
            curriculum_id = request.POST.get('curriculum_id')
            curriculum = Curriculums.objects.get(id=curriculum_id)

            AssignSection_id = request.POST.get('AssignSection_id')
            assignsection = AssignSection.objects.get(id=AssignSection_id)

            subject_id = request.POST.get('subject_id')
            subject = Subjects.objects.get(id=subject_id)

            staff_id = request.POST.get('staff_id')
            staff_user = CustomUser.objects.get(id=staff_id)

            # Get the related Staff instance to check the max_load
            staff = Staffs.objects.get(admin=staff_user)
            current_load = Load.objects.filter(staff_id=staff_user).count()

            # Check if the current load exceeds or equals the staff's max_load
            if current_load >= staff.max_load:
                messages.error(request, f"{staff_user.first_name} {staff_user.last_name} has reached the maximum load limit of {staff.max_load}.")
                return redirect('add_load')

            # Saving the load
            load = Load(      
                        curriculum_id=curriculum,
                        AssignSection_id = assignsection,
                        subject_id=subject,
                        staff_id=staff_user
                        )
            load.save()

            messages.success(request, "Load Added Successfully!")
            return redirect('add_load')

        except Exception as e:
            messages.error(request, f"Failed to Add Load! Error: {e}")
            return redirect('add_load')

def add_schedule(request):
    session_years = SessionYearModel.objects.all()
    staffs = CustomUser.objects.filter(user_type='2')
    loads = Load.objects.all()  
    context = {
        "session_years": session_years,
        "staffs": staffs,
        "loads": loads,  
    }
    return render(request, 'hod_template/add_schedule_template.html', context)


def add_schedule_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_schedule')
    else:
        
        try:

            session_year_id = request.POST.get('session_year_id')
            session_id = SessionYearModel.objects.get(id=session_year_id)
            
            staff_id = request.POST.get('staff_id')
            staff_id = CustomUser.objects.get(id=staff_id)

            load_id = request.POST.get('load_id')
            load_id = Load.objects.get(id=load_id)

            day_of_week = request.POST.get('day_of_week')
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')
            
            # Saving the load
            schedule = Schedule(      
                        session_year_id=session_id,
                        staff_id=staff_id, 
                        load_id=load_id,
                        day_of_week=day_of_week,
                        start_time=start_time,
                        end_time=end_time
                        )
            schedule.save()

            messages.success(request, "Schedule Added Successfully!")
            return redirect('add_schedule')
        
        except Exception as e:
            print(e)  # Print the exception for debugging purposes
            messages.error(request, f"Failed to Add Schedule! Erro: {e}" )
            return redirect('add_schedule')

def manage_schedule(request):
    loads = Load.objects.all()
    assignsections = AssignSection.objects.all()
    schedules = Schedule.objects.all()
    context = {
        "loads": loads,
        "assignsections": assignsections,
        "schedules": schedules,
        
    }
    return render(request, 'hod_template/manage_schedule_template.html', context)


def class_search(request):
    search_query = request.GET.get('search', '')

    # Store search results
    assignsections = AssignSection.objects.all()
    loads = Load.objects.all()
    schedules = Schedule.objects.all()

    # If a search query is provided, filter the results
    if search_query:
        assignsections = AssignSection.objects.filter(
            Student_id__admin__first_name__icontains=search_query
        )
        loads = Load.objects.filter(
            subject_id__subject_name__icontains=search_query
        )
        schedules = Schedule.objects.filter(
            load_id__subject_id__subject_name__icontains=search_query
        )

        # Save the search query in the session to persist it across page loads
        request.session['search_query'] = search_query
    else:
        # Clear the search query from the session if no search is provided
        request.session.pop('search_query', None)

    # Check if there is a search query in the GET request and if a search has been made
    if 'search' in request.GET:
        # Don't redirect on the initial search
        return render(request, 'hod_template/manage_schedule_template.html', {
            'assignsections': assignsections,
            'loads': loads,
            'schedules': schedules,
            'search_query': search_query,  # Pass the search query to the template if needed
        })

    # Render the search results or the default page
    return render(request, 'hod_template/manage_schedule_template.html', {
        'assignsections': assignsections,
        'loads': loads,
        'schedules': schedules,
        'search_query': search_query,  # Pass the search query to the template if needed
    })


def edit_schedule(request, schedule_id):
    # Adding Schedule ID into Session Variable
    request.session['schedule_id'] = schedule_id

    try:
        # Retrieve the schedule object using the provided schedule_id
        schedule = Schedule.objects.get(id=schedule_id)
    except Schedule.DoesNotExist:
        messages.error(request, "Schedule does not exist.")
        return redirect('manage_schedule')  # Adjust this redirect based on your URL names

    # Initialize the form with data from the database
    form = EditScheduleForm()
    form.fields['GradeLevel_id'].initial = schedule.GradeLevel_id.id
    form.fields['subject_id'].initial = schedule.subject_id.id
    form.fields['staff_id'].initial = schedule.staff_id.admin.id
    form.fields['session_year_id'].initial = schedule.session_year_id.id
    form.fields['day_of_week'].initial = schedule.day_of_week
    form.fields['start_time'].initial = schedule.start_time
    form.fields['end_time'].initial = schedule.end_time

    context = {
        "id": schedule_id,
        "form": form
    }

    return render(request, "hod_template/edit_schedule_template.html", context)

def edit_schedule_save(request):
    if request.method != "POST":
        return HttpResponse("Invalid Method!")
    else:
        schedule_id = request.session.get('schedule_id')
        if schedule_id is None:
            return redirect('/manage_schedule')

        form = EditScheduleForm(request.POST, request.FILES)
        if form.is_valid():
            subject_id = form.cleaned_data['subject_id']
            GradeLevel_id = form.cleaned_data['GradeLevel_id']
            staff_id = form.cleaned_data['staff_id']
            session_year_id = form.cleaned_data['session_year_id']
            day_of_week = form.cleaned_data['day_of_week']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']

            try:
                # Update Schedule model
                schedule = Schedule.objects.get(id=schedule_id)
                
                # Update schedule fields
                schedule.subject_id = Subjects.objects.get(subject_id)
                schedule.GradeLevel_id = GradeLevel.objects.get(id=GradeLevel_id)
                schedule.staff_id = Staffs.objects.get(id=staff_id)
                schedule.session_year_id = SessionYearModel.objects.get(id=session_year_id)
                schedule.day_of_week = day_of_week
                schedule.start_time = start_time
                schedule.end_time = end_time
                schedule.save()
                
                # Clear the session variable
                del request.session['schedule_id']

                messages.success(request, "Schedule Updated Successfully!")
                return redirect(f'/edit_schedule/{schedule_id}')
            except Exception as e:
                messages.error(request, f"Failed to Update Schedule: {e}")
                return redirect(f'/edit_schedule/{schedule_id}')
        else:
            return redirect(f'/edit_schedule/{schedule_id}')




@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)



def student_feedback_message(request):
    feedbacks = FeedBackStudent.objects.all()
    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'hod_template/student_feedback_template.html', context)


@csrf_exempt
def student_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBackStudent.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")


def staff_feedback_message(request):
    feedbacks = FeedBackStaffs.objects.all()
    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'hod_template/staff_feedback_template.html', context)


@csrf_exempt
def staff_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBackStaffs.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")


def student_leave_view(request):
    leaves = LeaveReportStudent.objects.all()
    context = {
        "leaves": leaves
    }
    return render(request, 'hod_template/student_leave_view.html', context)

def student_leave_approve(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect('student_leave_view')


def student_leave_reject(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('student_leave_view')


def staff_leave_view(request):
    leaves = LeaveReportStaff.objects.all()
    context = {
        "leaves": leaves
    }
    return render(request, 'hod_template/staff_leave_view.html', context)


def staff_leave_approve(request, leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect('staff_leave_view')


def staff_leave_reject(request, leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('staff_leave_view')


def admin_view_attendance(request):
    subjects = Subjects.objects.all()
    session_years = SessionYearModel.objects.all()
    context = {
        "subjects": subjects,
        "session_years": session_years
    }
    return render(request, "hod_template/admin_view_attendance.html", context)


@csrf_exempt
def admin_get_attendance_dates(request):
    # Getting Values from Ajax POST 'Fetch Student'
    subject_id = request.POST.get("subject")
    session_year = request.POST.get("session_year_id")

    # Students enroll to GradeLevel, GradeLevel has Subjects
    # Getting all data from subject model based on subject_id
    subject_model = Subjects.objects.get(id=subject_id)

    session_model = SessionYearModel.objects.get(id=session_year)

    # students = Students.objects.filter(GradeLevel_id=subject_model.GradeLevel_id, session_year_id=session_model)
    attendance = Attendance.objects.filter(subject_id=subject_model, session_year_id=session_model)

    # Only Passing Student Id and Student Name Only
    list_data = []

    for attendance_single in attendance:
        data_small={"id":attendance_single.id, "attendance_date":str(attendance_single.attendance_date), "session_year_id":attendance_single.session_year_id.id}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def admin_get_attendance_student(request):
    # Getting Values from Ajax POST 'Fetch Student'
    attendance_date = request.POST.get('attendance_date')
    attendance = Attendance.objects.get(id=attendance_date)

    attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)
    # Only Passing Student Id and Student Name Only
    list_data = []

    for student in attendance_data:
        data_small={"id":student.student_id.admin.id, "name":student.student_id.admin.first_name+" "+student.student_id.admin.last_name, "status":student.status}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


def admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)

    context={
        "user": user
    }
    return render(request, 'hod_template/admin_profile.html', context)


def admin_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('admin_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect('admin_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('admin_profile')
    


def staff_profile(request):
    pass


def student_profile(requtest):
    pass



