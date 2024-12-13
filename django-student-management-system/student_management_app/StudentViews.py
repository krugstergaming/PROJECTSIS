from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage 
from django.urls import reverse
import datetime 
import math
from student_management_app.models import CustomUser, Staffs, Enrollment, BalancePayment, GradeLevel, School_info, AssignSection, Schedule, Subjects, Students, Attendance, AttendanceReport, LeaveReportStudent, FeedBackStudent, StudentResult


def student_home(request):
    student_obj = Students.objects.get(admin=request.user.id)
    total_attendance = AttendanceReport.objects.filter(student_id=student_obj).count()
    attendance_present = AttendanceReport.objects.filter(student_id=student_obj, status=True).count()
    attendance_absent = AttendanceReport.objects.filter(student_id=student_obj, status=False).count()

    course_obj = GradeLevel.objects.get(id=student_obj.GradeLevel_id.id)
    total_subjects = Subjects.objects.filter(GradeLevel_id=course_obj).count()

    subject_name = []
    data_present = []
    data_absent = []
    subject_data = Subjects.objects.filter(GradeLevel_id=student_obj.GradeLevel_id)
    for subject in subject_data:
        attendance = Attendance.objects.filter(subject_id=subject.id)
        attendance_present_count = AttendanceReport.objects.filter(attendance_id__in=attendance, status=True, student_id=student_obj.id).count()
        attendance_absent_count = AttendanceReport.objects.filter(attendance_id__in=attendance, status=False, student_id=student_obj.id).count()
        subject_name.append(subject.subject_name)
        data_present.append(attendance_present_count)
        data_absent.append(attendance_absent_count)
    
    context={
        "total_attendance": total_attendance,
        "attendance_present": attendance_present,
        "attendance_absent": attendance_absent,
        "total_subjects": total_subjects,
        "subject_name": subject_name,
        "data_present": data_present,
        "data_absent": data_absent
    }
    return render(request, "student_template/student_home_template.html", context)


def student_view_attendance(request):
    student = Students.objects.get(admin=request.user.id) # Getting Logged in Student Data
    gradelevel = student.GradeLevel_id # Getting GradeLevel Enrolled of LoggedIn Student
    # gradelevel = GradeLevel.objects.get(id=student.GradeLevel_id.id) # Getting GradeLevel Enrolled of LoggedIn Student
    subjects = Subjects.objects.filter(GradeLevel_id=gradelevel) # Getting the Subjects of GradeLevel Enrolled
    context = {
        "subjects": subjects
    }
    return render(request, "student_template/student_view_attendance.html", context)


def student_view_attendance_post(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('student_view_attendance')
    else:
        # Getting all the Input Data
        subject_id = request.POST.get('subject')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Parsing the date data into Python object
        start_date_parse = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date_parse = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

        # Getting all the Subject Data based on Selected Subject
        subject_obj = Subjects.objects.get(id=subject_id)
        # Getting Logged In User Data
        user_obj = CustomUser.objects.get(id=request.user.id)
        # Getting Student Data Based on Logged in Data
        stud_obj = Students.objects.get(admin=user_obj)

        # Now Accessing Attendance Data based on the Range of Date Selected and Subject Selected
        attendance = Attendance.objects.filter(attendance_date__range=(start_date_parse, end_date_parse), subject_id=subject_obj)
        # Getting Attendance Report based on the attendance details obtained above
        attendance_reports = AttendanceReport.objects.filter(attendance_id__in=attendance, student_id=stud_obj)

        # for attendance_report in attendance_reports:
        #     print("Date: "+ str(attendance_report.attendance_id.attendance_date), "Status: "+ str(attendance_report.status))

        # messages.success(request, "Attendacne View Success")

        context = {
            "subject_obj": subject_obj,
            "attendance_reports": attendance_reports
        }

        return render(request, 'student_template/student_attendance_data.html', context)
       

def student_apply_leave(request):
    student_obj = Students.objects.get(admin=request.user.id)
    leave_data = LeaveReportStudent.objects.filter(student_id=student_obj)
    context = {
        "leave_data": leave_data
    }
    return render(request, 'student_template/student_apply_leave.html', context)


def student_apply_leave_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('student_apply_leave')
    else:
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')

        student_obj = Students.objects.get(admin=request.user.id)
        try:
            leave_report = LeaveReportStudent(student_id=student_obj, leave_date=leave_date, leave_message=leave_message, leave_status=0)
            leave_report.save()
            messages.success(request, "Applied for Leave.")
            return redirect('student_apply_leave')
        except:
            messages.error(request, "Failed to Apply Leave")
            return redirect('student_apply_leave')
 

def student_feedback(request):
    student_obj = Students.objects.get(admin=request.user.id)
    feedback_data = FeedBackStudent.objects.filter(student_id=student_obj)
    context = {
        "feedback_data": feedback_data
    }
    return render(request, 'student_template/student_feedback.html', context)


def student_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('student_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        student_obj = Students.objects.get(admin=request.user.id)

        try:
            add_feedback = FeedBackStudent(student_id=student_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('student_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('student_feedback')


def student_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    student = Students.objects.get(admin=user)

    context={
        "user": user,
        "student": student
    }
    return render(request, 'student_template/student_profile.html', context)


def student_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('student_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        address = request.POST.get('address')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()

            student = Students.objects.get(admin=customuser.id)
            student.address = address
            student.save()
            
            messages.success(request, "Profile Updated Successfully")
            return redirect('student_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('student_profile')


def student_view_result(request):
    student = Students.objects.get(admin=request.user.id)
    student_results = StudentResult.objects.filter(student_id=student.id)
    schools = School_info.objects.first()

    # Organize results by academic year
    results_by_year = {}
    for result in student_results:
        academic_year = result.load_id.session_year_id
        if academic_year not in results_by_year:
            results_by_year[academic_year] = {'results': [], 'general_averages': []}
        # Append results and general averages
        results_by_year[academic_year]['results'].append(result)
        results_by_year[academic_year]['general_averages'].append(result.general_average)

    # Calculate general averages and apply rounding
    for academic_year, data in results_by_year.items():
        # Round up each subject's final grade
        for result in data['results']:
            if result.subject_final_grade is not None:
                result.subject_final_grade = math.ceil(result.subject_final_grade)

        # Calculate general average and round up
        general_average = sum(data['general_averages']) / len(data['general_averages']) if data['general_averages'] else 0
        data['general_average'] = math.ceil(general_average)

    # Sort results_by_year by academic year in descending order
    sorted_results_by_year = dict(
        sorted(results_by_year.items(), key=lambda item: item[0].session_start_year, reverse=True)
    )

    # Get the student's status from the Students model
    student_status = student.student_status

    # Get the student's GradeLevel and Section from AssignSection model
    try:
        assign_section = AssignSection.objects.get(Student_id=student)
        grade_level = assign_section.GradeLevel_id.GradeLevel_name
        section = assign_section.section_id.section_name
    except AssignSection.DoesNotExist:
        grade_level = "N/A"
        section = "N/A"

    context = {
        "results_by_year": sorted_results_by_year,
        "student_status": student_status,
        "grade_level": grade_level,
        "section": section,
        "student": student,
        "schools": schools,
    }

    return render(request, "student_template/student_view_result.html", context)

def student_view_schedule(request):
    # Get the student object for the currently logged-in user
    student = Students.objects.get(admin=request.user.id)

    # Query the assigned section for the student
    assign_section = AssignSection.objects.filter(Student_id=student.id).first()

    if assign_section:
        # Get the section that the student is assigned to
        section = assign_section.section_id

        # Get the schedules where the student is assigned
        student_schedules = Schedule.objects.filter(
            load_id__AssignSection_id__section_id=section
        ).select_related(
            'load_id', 'load_id__session_year_id', 'load_id__AssignSection_id', 'load_id__subject_id'
        )

        # Organize schedules by academic year
        schedules_by_year = {}
        for schedule in student_schedules:
            academic_year = schedule.load_id.session_year_id
            if academic_year not in schedules_by_year:
                schedules_by_year[academic_year] = []
            schedules_by_year[academic_year].append(schedule)

        # Sort schedules_by_year by academic year in descending order
        sorted_schedules_by_year = dict(
            sorted(schedules_by_year.items(), key=lambda item: item[0].session_start_year, reverse=True)
        )

        # Add flags to avoid repeating data for Grade Level - Section, Subject Code, and Description
        for academic_year, schedules in sorted_schedules_by_year.items():
            last_grade_section = None
            last_subject_code = None
            last_description = None

            for schedule in schedules:
                # Get values
                grade_section = f"{schedule.load_id.AssignSection_id.GradeLevel_id.GradeLevel_name} - {schedule.load_id.AssignSection_id.section_id.section_name}"
                subject_code = schedule.load_id.subject_id.subject_code
                description = f"{schedule.load_id.subject_id.subject_name} - {schedule.load_id.subject_id.subject_description}"

                # Determine whether to show each field
                schedule.show_grade_section = grade_section != last_grade_section
                schedule.show_subject_code = subject_code != last_subject_code
                schedule.show_description = description != last_description

                # Update last seen values
                last_grade_section = grade_section
                last_subject_code = subject_code
                last_description = description

        # Track visible rows for numbering
        for academic_year, schedules in sorted_schedules_by_year.items():
            row_counter = 1  # Initialize row counter for visible rows
            for schedule in schedules:
                if schedule.show_grade_section or schedule.show_subject_code or schedule.show_description:
                    schedule.row_number = row_counter
                    row_counter += 1
                else:
                    schedule.row_number = None  # Hide the row number if the row is empty

        context = {
            "schedules_by_year": sorted_schedules_by_year,
            "student": student,
        }
    else:
        # If the student is not assigned to any section, return a message
        context = {
            "schedules_by_year": None,
            "message": "You are not assigned to any section yet.",
            "student": student,
        }

    return render(request, "student_template/student_view_schedule.html", context)


def student_view_account(request):
    # Get the student object for the currently logged-in user
    student = Students.objects.get(admin=request.user.id)
    
    # Query the enrollment record associated with the student
    enrollment = Enrollment.objects.filter(student_id=student).first()
    
    # Query the balance payment records associated with the enrollment
    balance_payments = BalancePayment.objects.filter(enrollment=enrollment).order_by('-payment_balance_date') if enrollment else None

    # Check if the student has an enrollment record
    context = {
        "enrollment": enrollment,
        "balance_payments": balance_payments,
        "message": "No enrollment or payment records found." if not enrollment else None
    }

    # Render the accounts template
    return render(request, "student_template/student_view_account.html", context)

