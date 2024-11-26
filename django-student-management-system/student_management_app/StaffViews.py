from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from collections import defaultdict


from student_management_app.models import CustomUser, Staffs, GradeLevel, Section, Schedule, AssignSection, Subjects, Load, Students, SessionYearModel, Attendance, AttendanceReport, LeaveReportStaff, FeedBackStaffs, StudentResult, GradingConfiguration



def staff_home(request):
    # Fetching subjects assigned to the staff via the Load model
    loads = Load.objects.filter(staff_id=request.user.id)
    subjects = Subjects.objects.filter(load__in=loads)

    # Fetching all assignsections related to the subjects assigned to this staff
    assignsections = AssignSection.objects.filter(section_id__in=subjects.values_list('id', flat=True)).distinct('section_id', 'GradeLevel_id')

    # Counting students based on the sections and grade levels assigned to the staff's subjects
    students_count = Students.objects.filter(assignsection__in=assignsections).count()

    # Counting the subjects the staff is teaching
    subject_count = subjects.count()

    # Fetching attendance count for the staff's subjects
    attendance_count = Attendance.objects.filter(subject_id__in=subjects).count()

    # Fetching approved leave count for the staff
    leave_count = LeaveReportStaff.objects.filter(staff_id=request.user.id, leave_status=1).count()

    # Fetch attendance data by subjects
    subject_list = []
    attendance_list = []
    for subject in subjects:
        attendance_count_by_subject = Attendance.objects.filter(subject_id=subject.id).count()
        subject_list.append(subject.subject_name)
        attendance_list.append(attendance_count_by_subject)

    # Fetching attendance information for students in the sections assigned to the staff
    students_in_sections = Students.objects.filter(assignsection__in=assignsections)
    student_list = []
    student_list_attendance_present = []
    student_list_attendance_absent = []
    
    for student in students_in_sections:
        attendance_present_count = AttendanceReport.objects.filter(status=True, student_id=student.id).count()
        attendance_absent_count = AttendanceReport.objects.filter(status=False, student_id=student.id).count()
        student_list.append(f"{student.admin.first_name} {student.admin.last_name}")
        student_list_attendance_present.append(attendance_present_count)
        student_list_attendance_absent.append(attendance_absent_count)

    context = {
        "students_count": students_count,
        "attendance_count": attendance_count,
        "leave_count": leave_count,
        "subject_count": subject_count,
        "subject_list": subject_list,
        "attendance_list": attendance_list,
        "student_list": student_list,
        "attendance_present_list": student_list_attendance_present,
        "attendance_absent_list": student_list_attendance_absent,
    }
    return render(request, "staff_template/staff_home_template.html", context)




def staff_take_attendance(request):
    # Get all the loads assigned to the current staff
    loads = Load.objects.filter(staff_id=request.user.id)

    # Get all subjects related to those loads
    subjects = Subjects.objects.filter(load__in=loads)

    # Get all session years
    session_years = SessionYearModel.objects.all()

    context = {
        "subjects": subjects,
        "session_years": session_years
    }
    
    return render(request, "staff_template/take_attendance_template.html", context)


def staff_apply_leave(request):
    staff_obj = Staffs.objects.get(admin=request.user.id)
    leave_data = LeaveReportStaff.objects.filter(staff_id=staff_obj)
    context = {
        "leave_data": leave_data
    }
    return render(request, "staff_template/staff_apply_leave_template.html", context)


def staff_apply_leave_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('staff_apply_leave')
    else:
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')

        staff_obj = Staffs.objects.get(admin=request.user.id)
        try:
            leave_report = LeaveReportStaff(staff_id=staff_obj, leave_date=leave_date, leave_message=leave_message, leave_status=0)
            leave_report.save()
            messages.success(request, "Applied for Leave.")
            return redirect('staff_apply_leave')
        except:
            messages.error(request, "Failed to Apply Leave")
            return redirect('staff_apply_leave')


def staff_feedback(request):
    staff_obj = Staffs.objects.get(admin=request.user.id)
    feedback_data = FeedBackStaffs.objects.filter(staff_id=staff_obj)
    context = {
        "feedback_data":feedback_data
    }
    return render(request, "staff_template/staff_feedback_template.html", context)


def staff_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('staff_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        staff_obj = Staffs.objects.get(admin=request.user.id)

        try:
            add_feedback = FeedBackStaffs(staff_id=staff_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('staff_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('staff_feedback')

@csrf_exempt
def save_attendance_data(request):
    # Get Values from Staf Take Attendance form via AJAX (JavaScript)
    # Use getlist to access HTML Array/List Input Data
    student_ids = request.POST.get("student_ids")
    subject_id = request.POST.get("subject_id")
    attendance_date = request.POST.get("attendance_date")
    session_year_id = request.POST.get("session_year_id")

    subject_model = Subjects.objects.get(id=subject_id)
    session_year_model = SessionYearModel.objects.get(id=session_year_id)

    json_student = json.loads(student_ids)
    # print(dict_student[0]['id'])

    # print(student_ids)
    try:
        # First Attendance Data is Saved on Attendance Model
        attendance = Attendance(subject_id=subject_model, attendance_date=attendance_date, session_year_id=session_year_model)
        attendance.save()

        for stud in json_student:
            # Attendance of Individual Student saved on AttendanceReport Model
            student = Students.objects.get(admin=stud['id'])
            attendance_report = AttendanceReport(student_id=student, attendance_id=attendance, status=stud['status'])
            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("Error")


def staff_update_attendance(request):
    # Fetch the loads assigned to the current staff member
    loads = Load.objects.filter(staff_id=request.user.id)
    
    # Extract the subjects from the loads
    subjects = Subjects.objects.filter(id__in=loads.values_list('subject_id', flat=True))
    
    session_years = SessionYearModel.objects.all()
    
    context = {
        "subjects": subjects,
        "session_years": session_years
    }
    
    return render(request, "staff_template/update_attendance_template.html", context)

@csrf_exempt
def get_attendance_dates(request):
    

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
def get_attendance_student(request):
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


@csrf_exempt
def update_attendance_data(request):
    student_ids = request.POST.get("student_ids")

    attendance_date = request.POST.get("attendance_date")
    attendance = Attendance.objects.get(id=attendance_date)

    json_student = json.loads(student_ids)

    try:
        
        for stud in json_student:
            # Attendance of Individual Student saved on AttendanceReport Model
            student = Students.objects.get(admin=stud['id'])

            attendance_report = AttendanceReport.objects.get(student_id=student, attendance_id=attendance)
            attendance_report.status=stud['status']

            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("Error")


def staff_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    staff = Staffs.objects.get(admin=user)

    context={
        "user": user,
        "staff": staff
    }
    return render(request, 'staff_template/staff_profile.html', context)


def staff_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('staff_profile')
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

            staff = Staffs.objects.get(admin=customuser.id)
            staff.address = address
            staff.save()

            messages.success(request, "Profile Updated Successfully")
            return redirect('staff_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('staff_profile')


def staff_add_result(request):
    # Fetch the grading configuration to check if grading is active
    config = GradingConfiguration.objects.first()

    # Check if grading is active; if not, render the closed template
    if config and not config.is_grading_active:
        return render(request, "staff_template/close_result_template.html")

    # Fetch the loads assigned to the current staff
    loads = Load.objects.filter(staff_id=request.user.id)

    # Fetch all session years
    session_years = SessionYearModel.objects.all()
    
    # Context data to be passed to the template
    context = {
        "loads": loads,
        "session_years": session_years,
    }

    # Render the active grading template when grading is enabled
    return render(request, "staff_template/add_result_template.html", context)

def get_loads_by_academic_year(request):
    session_year_id = request.GET.get('session_year_id')
    loads = Load.objects.filter(session_year_id=session_year_id, staff_id=request.user.id)  # Filter by academic year and staff

    load_data = []
    for load in loads:
        load_data.append({
            'id': load.id,
            'staff_id': load.staff_id.id,
            'grade_level': load.AssignSection_id.GradeLevel_id.GradeLevel_name,
            'section_name': load.AssignSection_id.section_id.section_name,
            'subject_name': load.subject_id.subject_name
        })

    return JsonResponse({'loads': load_data})

# WE don't need csrf_token when using Ajax
@csrf_exempt
def get_students(request):
    print(f"session_year: {request.POST.get('session_year')}, load_id: {request.POST.get('load_id')}")
    try:
        # Getting Values from Ajax POST 'Fetch Student'
        session_year_id = request.POST.get("session_year")  # Added session year filter
        load_id = request.POST.get("load_id")

        if not load_id or not session_year_id:
            return JsonResponse({"error": "Missing load_id or session_year_id"}, status=400)

        # Fetch the Load model based on load_id
        load_model = Load.objects.get(id=load_id)

        # Ensure the session year matches the one selected by the user
        if load_model.session_year_id.id != int(session_year_id):
            return JsonResponse({"error": "Session Year mismatch"}, status=400)

        # Get AssignSection entries based on the section in the selected load
        assign_sections = AssignSection.objects.filter(
            section_id__id=load_model.AssignSection_id.section_id.id,
        )

        # Now, filter students based on the AssignSection records
        students = Students.objects.filter(id__in=assign_sections.values('Student_id'))

        # Fetch results for the filtered students, adjusting for session_year_id
        student_results = StudentResult.objects.filter(
            load_id=load_model,
            load_id__session_year_id__id=session_year_id  # Fixed filtering by session_year
        )

        # Organize the results in a dictionary for easy access
        results_dict = {
            result.student_id.id: {
                "first_quarter": result.subject_first_quarter,
                "second_quarter": result.subject_second_quarter,
                "third_quarter": result.subject_third_quarter,
                "fourth_quarter": result.subject_fourth_quarter,
                "final_grade": result.subject_final_grade
            }
            for result in student_results
        }

        # Prepare the data to be sent back to the front-end
        list_data = []
        for student in students:
            grades = results_dict.get(student.id, {})

            data_small = {
                "id": student.id,
                "student_number": student.student_number,
                "name": f"{student.admin.first_name} {student.admin.last_name}",
                "first_quarter": grades.get("first_quarter", ""),
                "second_quarter": grades.get("second_quarter", ""),
                "third_quarter": grades.get("third_quarter", ""),
                "fourth_quarter": grades.get("fourth_quarter", ""),
                "final_grade": grades.get("final_grade", "")
            }
            list_data.append(data_small)

        # Return the data as a JSON response
        return JsonResponse(list_data, safe=False)

    except Load.DoesNotExist:
        return JsonResponse({"error": "Load not found"}, status=404)
    except AssignSection.DoesNotExist:
        return JsonResponse({"error": "AssignSection not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def staff_add_result_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('staff_add_result')
    else:
        student_admin_id = request.POST.get('student_list')
        load_id = request.POST.get('load_id')

        # Log or print the values to check
        print(f"Student ID: {student_admin_id}, Load ID: {load_id}")

        if not student_admin_id or not load_id:
            messages.error(request, "Invalid data received!")
            return redirect('staff_add_result')

        first_quarter = request.POST.get('first_quarter')
        second_quarter = request.POST.get('second_quarter')
        third_quarter = request.POST.get('third_quarter')
        fourth_quarter = request.POST.get('fourth_quarter')

        try:
            student_obj = Students.objects.get(id=student_admin_id)
            load_obj = Load.objects.get(id=load_id)

            # Convert grades to integers or 0 if empty
            first_quarter = int(first_quarter) if first_quarter else 0
            second_quarter = int(second_quarter) if second_quarter else 0
            third_quarter = int(third_quarter) if third_quarter else 0
            fourth_quarter = int(fourth_quarter) if fourth_quarter else 0

            final_grade = (first_quarter + second_quarter + third_quarter + fourth_quarter) / 4

            # Check if the result already exists
            check_exist = StudentResult.objects.filter(load_id=load_obj, student_id=student_obj).exists()
            if check_exist:
                result = StudentResult.objects.get(load_id=load_obj, student_id=student_obj)
                result.subject_first_quarter = first_quarter
                result.subject_second_quarter = second_quarter
                result.subject_third_quarter = third_quarter
                result.subject_fourth_quarter = fourth_quarter
                result.subject_final_grade = final_grade
                result.save()
                messages.success(request, "Result Updated Successfully!")
            else:
                result = StudentResult(
                    student_id=student_obj,
                    load_id=load_obj,
                    subject_first_quarter=first_quarter,
                    subject_second_quarter=second_quarter,
                    subject_third_quarter=third_quarter,
                    subject_fourth_quarter=fourth_quarter,
                    subject_final_grade=final_grade
                )
                result.save()
                messages.success(request, "Result Added Successfully!")

            # Calculate the general average only for the current academic year
            student_results = StudentResult.objects.filter(
                student_id=student_obj,
                load_id__session_year_id=load_obj.session_year_id  # Filter by the current academic year
            )

            if student_results.exists():
                general_average = student_results.aggregate(Avg('subject_final_grade'))['subject_final_grade__avg']
                
                # Update the general average for each result in the current academic year
                for res in student_results:
                    res.general_average = general_average
                    res.save()

                messages.success(request, f"General Average Updated: {general_average:.2f}")

            return redirect('staff_add_result')

        except Exception as e:
            messages.error(request, f"Failed to Add Result! Error: {e}")
            return redirect('staff_add_result')
        

def staff_view_schedule(request):
    # Get the currently logged-in staff member
    staff = CustomUser.objects.get(id=request.user.id)

    # Get the schedules where the staff member is assigned
    schedules = Schedule.objects.filter(load_id__staff_id=staff).select_related(
        'load_id', 'load_id__session_year_id', 'load_id__AssignSection_id', 'load_id__subject_id'
    )

    # Organize schedules by academic year
    schedules_by_year = {}
    for schedule in schedules:
        academic_year = schedule.load_id.session_year_id
        if academic_year not in schedules_by_year:
            schedules_by_year[academic_year] = []
        schedules_by_year[academic_year].append(schedule)

    # Sort schedules_by_year by academic year in descending order
    sorted_schedules_by_year = dict(
        sorted(schedules_by_year.items(), key=lambda item: item[0].session_start_year, reverse=True)
    )

    context = {
        "schedules_by_year": sorted_schedules_by_year,
        "staff": staff,
    }

    return render(request, "staff_template/staff_view_schedule_template.html", context)



