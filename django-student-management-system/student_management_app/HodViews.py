from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json

from student_management_app.models import CustomUser, Staffs, Curriculums, GradeLevel, Subjects, Section, Students, SessionYearModel, FeedBackStudent, FeedBackStaffs, LeaveReportStudent, LeaveReportStaff, Attendance, AttendanceReport, Schedule, GradingConfiguration, ParentGuardian, PreviousSchool, EmergencyContact
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
        subject_list.append(subject.subject_one)
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
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        middle_name = request.POST.get('middle_name')
        dob = request.POST.get('dob')
        age = request.POST.get('age')
        pob = request.POST.get('pob')
        sex = request.POST.get('sex')
        civil_status = request.POST.get('civil_status')
        height = request.POST.get('height')
        weight = request.POST.get('weight')
        blood_type = request.POST.get('blood_type')
        gsis_id = request.POST.get('gsis_id', 'N/A')
        pagibig_id = request.POST.get('pagibig_id', 'N/A')
        philhealth_id = request.POST.get('philhealth_id', 'N/A')
        sss_id = request.POST.get('sss_id', 'N/A')
        tin_id = request.POST.get('tin_id', 'N/A')
        citizenship = request.POST.get('citizenship')
        dual_country = request.POST.get('dual_country')
        permanent_address = request.POST.get('permanent_address')
        telephone_no = request.POST.get('telephone_no')
        cellphone_no = request.POST.get('cellphone_no')
        email_address = request.POST.get('email_address')

        try:
            user = CustomUser.objects.create_user(username=username, 
                                                  password=password, 
                                                  email=email, 
                                                  first_name=first_name, 
                                                  last_name=last_name, 
                                                  user_type=2)
            
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
            user.staffs.email_address = email_address
            
            user.save()
            messages.success(request, "Staff Added Successfully!")
            return redirect('add_staff')
        except:
            messages.error(request, "Failed to Add Staff!")
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
        try:
            curriculum = Curriculums(
                curriculum_name=curriculum_name,
                )
            curriculum.save()
            messages.success(request, "Curriculum Added Successfully!")
            return redirect('add_curriculum')
        except:
            messages.error(request, "Failed to Add Curriculum!")
            return redirect('add_curriculum')
        

def manage_curriculum(request):
    curriculums = Curriculums.objects.all()
    context = {
        "curriculums": curriculums
    }
    return render(request, 'hod_template/manage_curriculum_template.html', context)

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

        try:
            sessionyear = SessionYearModel(
                session_start_year = session_start_year, 
                session_end_year = session_end_year,
                session_limit = session_limit)
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
    context = {
        "gradelevels": gradelevels,
        "sessions": sessions
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
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        session_year_id = request.POST.get('session_year_id')
        GradeLevel_id = request.POST.get('GradeLevel_id')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        date_of_birth = request.POST.get('date_of_birth')
        place_of_birth = request.POST.get('place_of_birth')
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
            username=username, password=password, email=email,
            first_name=first_name, last_name=last_name, user_type=3
        )
        user.students.address = address

        # Assign GradeLevel and Session Year
        gradelevel_obj = GradeLevel.objects.get(id=GradeLevel_id)
        session_year_obj = SessionYearModel.objects.get(id=session_year_id)
        user.students.GradeLevel_id = gradelevel_obj
        user.students.session_year_id = session_year_obj

        # Additional Student Details
        user.students.gender = gender
        user.students.profile_pic = profile_pic_url
        user.students.age = age
        user.students.date_of_birth = date_of_birth
        user.students.place_of_birth = place_of_birth
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
            school_name=request.POST.get('school_name'),
            school_address=request.POST.get('school_address'),
            grade_level=request.POST.get('grade_level'),
            school_year_attended=request.POST.get('school_year_attended'),
            teacher_name=request.POST.get('teacher_name')
        )

        # Save Emergency Contact Information
        EmergencyContact.objects.create(
            students_id=user.students,
            name=request.POST.get('contact_name'),
            relation=request.POST.get('contact_relation'),
            address=request.POST.get('contact_address'),
            telephone_nos=request.POST.get('contact_telephone'),
            enrolling_teacher=request.POST.get('contact_referred_by'),
            referred_by=request.POST.get('referred_by')
        )

        messages.success(request, "Student Added Successfully!")
        return redirect('add_student')

    except Exception as e:
        messages.error(request, f"Failed to Add Student! Error: {str(e)}")
        return redirect('add_student')


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
    form.fields['gender'].initial = student.gender
    form.fields['session_year_id'].initial = student.session_year_id.id

    context = {
        "id": student_id,
        "username": student.admin.username,
        "form": form
    }
    return render(request, "hod_template/edit_student_template.html", context)


def edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("Invalid Method!")
    else:
        student_id = request.session.get('student_id')
        if student_id == None:
            return redirect('/manage_student')

        form = EditStudentForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            address = form.cleaned_data['address']
            GradeLevel_id = form.cleaned_data['GradeLevel_id']
            gender = form.cleaned_data['gender']
            session_year_id = form.cleaned_data['session_year_id']

            # Getting Profile Pic first
            # First Check whether the file is selected or not
            # Upload only if file is selected
            if len(request.FILES) != 0:
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None

            try:
                # First Update into Custom User Model
                user = CustomUser.objects.get(id=student_id)
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.username = username
                user.save()

                # Then Update Students Table
                student_model = Students.objects.get(admin=student_id)
                student_model.address = address

                gradelevel = GradeLevel.objects.get(id=GradeLevel_id)
                student_model.GradeLevel_id = gradelevel

                session_year_obj = SessionYearModel.objects.get(id=session_year_id)
                student_model.session_year_id = session_year_obj

                student_model.gender = gender
                if profile_pic_url != None:
                    student_model.profile_pic = profile_pic_url
                student_model.save()
                # Delete student_id SESSION after the data is updated
                del request.session['student_id']

                messages.success(request, "Student Updated Successfully!")
                return redirect('/edit_student/'+student_id)
            except:
                messages.success(request, "Failed to Uupdate Student.")
                return redirect('/edit_student/'+student_id)
        else:
            return redirect('/edit_student/'+student_id)


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
    gradelevels = GradeLevel.objects.all()
    curriculums = Curriculums.objects.all()
    context = {
        "gradelevels": gradelevels,
        "curriculums": curriculums
    }
    return render(request, 'hod_template/add_subject_template.html', context)



def add_subject_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_subject')
    else:
        subject_one = request.POST.get('subject_one')
        subject_two = request.POST.get('subject_two')
        subject_three = request.POST.get('subject_three')
        subject_four = request.POST.get('subject_four')
        subject_five = request.POST.get('subject_five')
        subject_six = request.POST.get('subject_six')
        subject_seven = request.POST.get('subject_seven')
        subject_eight = request.POST.get('subject_eight')
        subject_nine = request.POST.get('subject_nine')
        subject_ten = request.POST.get('subject_ten')

        curriculum_id = request.POST.get('curriculum_id')
        curriculum_id = Curriculums.objects.get(id=curriculum_id)

        GradeLevel_id = request.POST.get('GradeLevel_id')
        GradeLevel_id = GradeLevel.objects.get(id=GradeLevel_id)
        
        try:
            subject = Subjects(subject_one=subject_one,
                               subject_two=subject_two,
                               subject_three=subject_three,
                               subject_four=subject_four,
                               subject_five=subject_five,
                               subject_six=subject_six,
                               subject_seven=subject_seven,
                               subject_eight=subject_eight,
                               subject_nine=subject_nine,
                               subject_ten=subject_ten, 
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




def add_schedule(request):
    form = AddScheduleForm()
    context = {
        "form": form
    }
    return render(request, 'hod_template/add_schedule_template.html', context)


def add_schedule_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_schedule')
    else:
        form = AddScheduleForm(request.POST)

        if form.is_valid():
            GradeLevel_id = form.cleaned_data['GradeLevel_id']
            subject_id = form.cleaned_data['subject_id']
            staff_id = form.cleaned_data['staff_id']
            session_year_id = form.cleaned_data['session_year_id']
            day_of_week = form.cleaned_data['day_of_week']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']

            try:
                gradelevel_obj = GradeLevel.objects.get(id=GradeLevel_id)
                subject_obj = Subjects.objects.get(id=subject_id)
                staff_obj = Staffs.objects.get(id=staff_id)
                session_year_obj = SessionYearModel.objects.get(id=session_year_id)

                # Creating the schedule entry
                schedule = Schedule.objects.create(
                    GradeLevel_id=gradelevel_obj,
                    subject_id=subject_obj,
                    staff_id=staff_obj,
                    session_year_id=session_year_obj,
                    day_of_week=day_of_week,
                    start_time=start_time,
                    end_time=end_time
                )
                schedule.save()

                messages.success(request, "Schedule Added Successfully!")
                return redirect('add_schedule')
            except Exception as e:
                print(e)  # Print the exception for debugging purposes
                messages.error(request, "Failed to Add Schedule!")
                return redirect('add_schedule')
        else:
            messages.error(request, "Invalid Form Submission!")
            return redirect('add_schedule')

def manage_schedule(request):
    schedules = Schedule.objects.all()
    context = {
        "schedules": schedules
    }
    return render(request, 'hod_template/manage_schedule_template.html', context)

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


