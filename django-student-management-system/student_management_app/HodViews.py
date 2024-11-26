from openpyxl.utils import get_column_letter
from openpyxl.styles import Font, PatternFill, Alignment
from django.utils.timezone import now
from django.contrib.auth.hashers import make_password
from decimal import Decimal, InvalidOperation
from django.db import IntegrityError
from django.db.models import Count, F
from django.db import transaction
from datetime import datetime, date
from bs4 import BeautifulSoup
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime, date, time
from datetime import datetime as dt
from django.utils import timezone
from django.db.models import Q, Subquery
import cloudinary.uploader
import openpyxl
import requests
from django.contrib.auth.decorators import login_required

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from student_management_app.EmailBackEnd import EmailBackEnd
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import AllowAny

from student_management_app.models import CustomUser, School_info, Students, ParentGuardian, PreviousSchool, EmergencyContact, Attachment, BalancePayment, AssignSection, Load, Schedule, GradingConfiguration
from student_management_app.models import Staffs, staff_contact_info, staff_employment_info, staff_physical_info, staff_government_ID_info, Staffs_Educ_Background, StudentPromotionHistory
from student_management_app.models import Curriculums, GradeLevel, Enrollment, Enrollment_voucher, Subjects, Section, SessionYearModel
from student_management_app.models import FeedBackStudent, FeedBackStaffs, LeaveReportStudent, LeaveReportStaff, Attendance, AttendanceReport, Classroom
from .forms import EditStudentForm, AddScheduleForm, EditScheduleForm


def admin_home(request):
    all_student_count = Students.objects.count()
    subject_count = Subjects.objects.count()
    gradelevel_count = GradeLevel.objects.count()
    staff_count = Staffs.objects.count()
    load_count = Load.objects.count()
    curriculum_count = Curriculums.objects.count()

    # Serialize GradeLevel data
    grade_levels = GradeLevel.objects.values('GradeLevel_name')
    grade_levels_data = json.dumps(list(grade_levels))  # Serialize data for JSON compatibility

    # Updated query to get subjects grouped by GradeLevel
    subjects_per_gradelevel = Subjects.objects.select_related('GradeLevel_id') \
        .values('GradeLevel_id__GradeLevel_name') \
        .annotate(subject_count=Count('id'))

    # Prepare data to be passed to Chart.js
    gradelevels_datas = [
        {
            "grade_level": item['GradeLevel_id__GradeLevel_name'],  # The grade level name
            "subject_count": item['subject_count']  # The count of subjects per grade level
        }
        for item in subjects_per_gradelevel
    ]

    # Aggregate the number of students per GradeLevel
    students_per_gradelevel = Students.objects.values('GradeLevel_id__GradeLevel_name').annotate(student_count=Count('id'))
    
    # Prepare the data to pass to the template
    student_gradelevel_data = [
        {
            "grade_level": item['GradeLevel_id__GradeLevel_name'],
            "student_count": item['student_count']
        }
        for item in students_per_gradelevel
    ]

    context = {
        "all_student_count": all_student_count,
        "subject_count": subject_count,
        "gradelevel_count": gradelevel_count,
        "staff_count": staff_count,
        "load_count": load_count,
        "curriculum_count": curriculum_count,
        "curriculum_count": curriculum_count,
        "grade_levels_data": grade_levels_data,  # Pass JSON-serialized data to context
        "gradelevels_datas": json.dumps(gradelevels_datas),  # Pass JSON-serialized data to context
        "student_gradelevel_data": json.dumps(student_gradelevel_data),  # Pass JSON-serialized data to context
    }

    return render(request, "hod_template/home_content.html", context)




def add_staff(request):
    return render(request, "hod_template/Add_Template/add_staff_template.html")

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
            max_laod = request.POST.get('max_load')
            middle_name = request.POST.get('middle_name')
            dob = request.POST.get('dob')
            age = request.POST.get('age')
            pob = request.POST.get('pob')
            sex = request.POST.get('sex')
            civil_status = request.POST.get('civil_status')
            citizenship = request.POST.get('citizenship')
            dual_country = request.POST.get('dual_country')

            # Generate a predefined password based on staff details
            current_year = now().year
            predefined_password = f"{first_name.lower()}{last_name.lower()}{current_year}"

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
            user.staffs.citizenship = citizenship
            user.staffs.dual_country = dual_country
            user.save()

            # save staff contact information
            staff_contact_info.objects.create(
                 staffs_id = user.staffs,
                 region = request.POST.get('region-text'),
                 province = request.POST.get('province-text'),
                 city = request.POST.get('city-text'),
                 barangay = request.POST.get('barangay-text'),
                 street = request.POST.get('street'),
                 telephone_no = request.POST.get('telephone_no'),
                 cellphone_no = request.POST.get('cellphone_no'),
                 emergency_contact = request.POST.get('emergency_contact'),
                 emergency_relationship = request.POST.get('emergency_relationship'),
                 medical_condition = request.POST.get('medical_condition'),
            )
            # save staff employment information
            staff_employment_info.objects.create(
                 staffs_id = user.staffs,
                 employee_number = request.POST.get('employee_number'),
                 employee_type = request.POST.get('employee_type'),
                 position = request.POST.get('position'),
                 employment_status = request.POST.get('employment_status'),
            )
            # save staff physical information
            staff_physical_info.objects.create(
                 staffs_id = user.staffs,
                 blood_type = request.POST.get('blood_type'),
                 height = request.POST.get('height'),
                 weight = request.POST.get('weight'),
                 eye_color = request.POST.get('eye_color'),
                 hair_color = request.POST.get('hair_color'),
            )
            # save staff govenrment ID information
            staff_government_ID_info.objects.create(
                 staffs_id = user.staffs,
                 gsis_id = request.POST.get('gsis_id'),
                 philhealth_id = request.POST.get('philhealth_id'),
                 pagibig_id = request.POST.get('pagibig_id'),
                 sss_id = request.POST.get('sss_id'),
                 tin_id = request.POST.get('tin_id'),
            )
            # save staff educational background information
            Staffs_Educ_Background.objects.create(
                 staffs_id = user.staffs,
                 HEA = request.POST.get('HEA'),
                 preferred_subject = request.POST.get('preferred_subject'),
                 Cert_License = request.POST.get('Cert_License'),
                 teaching_exp = request.POST.get('teaching_exp'),
                 skills_competencies = request.POST.get('skills_competencies'),
                 language_spoken = request.POST.get('language_spoken'),
            )
            messages.success(request, "Faculty Added Successfully! Password: " + predefined_password)
            return redirect('add_staff')
        
        except IntegrityError as e:
            messages.error(request, f"Failed to Add Staff: Database error - {str(e)}")
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
    return render(request, "hod_template/Manage_Template/manage_staff_template.html", context)


def edit_staff(request, staff_id):
    staff = Staffs.objects.get(admin=staff_id)

    context = {
        "staff": staff,
        "id": staff_id
    }
    return render(request, "hod_template/Edit_Template/edit_staff_template.html", context)


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


def deactivate_staff(request, staff_id):
    try:
        # Get the CustomUser object related to the staff
        user = CustomUser.objects.get(id=staff_id)

        # Set the user as inactive
        user.is_active = False
        user.save()

        messages.success(request, "Staff account deactivated successfully.")
        return redirect('manage_staff')
    except CustomUser.DoesNotExist:
        messages.error(request, "Staff not found.")
        return redirect('manage_staff')
    except Exception as e:
        messages.error(request, f"Failed to deactivate staff: {str(e)}")
        return redirect('manage_staff')



def add_school(request):
    return render(request, "hod_template/Add_Template/add_school_template.html")

def add_school_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_school')
    else:
        school_name = request.POST.get('school_name')
        school_ID_number = request.POST.get('school_ID_number')
        school_district = request.POST.get('school_district')
        school_division = request.POST.get('school_division')
        school_region = request.POST.get('school_region')
        try:
            school = School_info(
                school_name=school_name,
                school_ID_number=school_ID_number,
                school_district=school_district,
                school_division=school_division,
                school_region=school_region
                )
            school.save()
            messages.success(request, "School Added Successfully!")
            return redirect('add_school')
        except:
            messages.error(request, "Failed to Add School!")
            return redirect('add_school')
        
def manage_school(request):
    schools = School_info.objects.all()
    context = {
        "schools": schools
    }
    return render(request, 'hod_template/Manage_Template/manage_school_template.html', context)

def add_curriculum(request):
    return render(request, "hod_template/Add_Template/add_curriculum_template.html")


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
    curriculums = Curriculums.objects.all()
    curriculums = Curriculums.objects.filter(is_archived=False)
    context = {
        "curriculums": curriculums
    }
    return render(request, 'hod_template/Manage_Template/manage_curriculum_template.html', context)

def edit_curriculum(request, curriculum_id):
    curriculum = Curriculums.objects.get(id=curriculum_id)
    context = {
        "curriculum": curriculum,
        "id": curriculum_id
    }
    return render(request, 'hod_template/Edit_Template/edit_curriculum_template.html', context)

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
    return render(request, 'hod_template/Archive_Template/archived_curriculum_template.html', context)

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
    return render(request, "hod_template/Add_Template/add_gradelevel_template.html", context)

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
        
def export_gradelevels_to_excel(request):
    # Create an in-memory workbook
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'Grade Levels'
    
    # Define the headers
    headers = ['GradeLevel Name', 'Curriculum', 'Date Created', 'Date Updated']
    
    # Define a fill color for the header (e.g., light blue)
    header_fill = PatternFill(start_color="ADD8E6", end_color="ADD8E6", fill_type="solid")
    
    # Add headers to the first row and make them bold with a background color and center alignment
    for col_num, header in enumerate(headers, 1):
        cell = sheet.cell(row=1, column=col_num)
        cell.value = header
        cell.font = Font(bold=True)  # Make the header bold
        cell.fill = header_fill  # Apply background color
        cell.alignment = Alignment(horizontal="center", vertical="center")  # Center-align the text

    # Query all grade levels
    gradelevels = GradeLevel.objects.all()

    # Add data rows starting from row 2 with center alignment
    for row_num, gradelevel in enumerate(gradelevels, 2):
        sheet.cell(row=row_num, column=1).value = gradelevel.GradeLevel_name
        sheet.cell(row=row_num, column=2).value = gradelevel.curriculum_id.curriculum_name  # Assuming curriculum has 'curriculum_name'
        sheet.cell(row=row_num, column=3).value = gradelevel.created_at.strftime('%Y-%m-%d %H:%M:%S')
        sheet.cell(row=row_num, column=4).value = gradelevel.updated_at.strftime('%Y-%m-%d %H:%M:%S')

        # Apply center alignment to all cells in the row
        for col_num in range(1, 5):
            cell = sheet.cell(row=row_num, column=col_num)
            cell.alignment = Alignment(horizontal="center", vertical="center")

    # Adjust column widths to fit the content
    for col in sheet.columns:
        max_length = 0
        column = col[0].column_letter  # Get the column letter (A, B, C, etc.)
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = max_length + 2  # Add some padding to the width
        sheet.column_dimensions[column].width = adjusted_width

    # Prepare the response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=GradeLevels.xlsx'

    # Save the workbook to the response
    workbook.save(response)

    return response

def export_staffs_to_excel(request):
    # Create an in-memory workbook
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'Staffs'
    
    # Define the headers
    headers = ['Last Name', 'First Name', 'Middle Name', 'Email', 'Age', 'Date of Birth', 'Place of Birth', 
               'Sex', 'Civil Rights', 'Height', 'Weight', 'Blood Type', 'GSIG ID', 'PagIbig ID', 
               'PhilHealth ID', 'SSS ID', 'TIN ID', 'Citizenship', 'Address', 'Telephone #',
               'Cellphone #', 'Created At', 'Updated At', 'Is Active']
    
    # Define a fill color for the header (e.g., light blue)
    header_fill = PatternFill(start_color="ADD8E6", end_color="ADD8E6", fill_type="solid")
    
    # Add headers to the first row and make them bold with a background color and center alignment
    for col_num, header in enumerate(headers, 1):
        cell = sheet.cell(row=1, column=col_num)
        cell.value = header
        cell.font = Font(bold=True)  # Make the header bold
        cell.fill = header_fill  # Apply background color
        cell.alignment = Alignment(horizontal="center", vertical="center")  # Center-align the text

    # Query all grade levels
    staffs = Staffs.objects.all()

    # Add data rows starting from row 2 with center alignment
    for row_num, staff in enumerate(staffs, 2):
        sheet.cell(row=row_num, column=1).value = staff.admin.last_name
        sheet.cell(row=row_num, column=2).value = staff.admin.first_name
        sheet.cell(row=row_num, column=3).value = staff.middle_name
        sheet.cell(row=row_num, column=4).value = staff.admin.email
        sheet.cell(row=row_num, column=5).value = staff.age
        sheet.cell(row=row_num, column=6).value = staff.dob
        sheet.cell(row=row_num, column=7).value = staff.pob
        sheet.cell(row=row_num, column=8).value = staff.sex
        sheet.cell(row=row_num, column=9).value = staff.civil_status
        sheet.cell(row=row_num, column=10).value = staff.height
        sheet.cell(row=row_num, column=11).value = staff.weight
        sheet.cell(row=row_num, column=12).value = staff.blood_type
        sheet.cell(row=row_num, column=13).value = staff.gsis_id
        sheet.cell(row=row_num, column=14).value = staff.pagibig_id
        sheet.cell(row=row_num, column=15).value = staff.philhealth_id
        sheet.cell(row=row_num, column=16).value = staff.sss_id
        sheet.cell(row=row_num, column=17).value = staff.tin_id
        sheet.cell(row=row_num, column=18).value = staff.citizenship
        sheet.cell(row=row_num, column=19).value = staff.permanent_address
        sheet.cell(row=row_num, column=20).value = staff.telephone_no
        sheet.cell(row=row_num, column=21).value = staff.cellphone_no
        sheet.cell(row=row_num, column=22).value = staff.created_at.strftime('%Y-%m-%d %H:%M:%S')
        sheet.cell(row=row_num, column=23).value = staff.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        sheet.cell(row=row_num, column=24).value = staff.admin.is_active

        # Apply center alignment to all cells in the row
        for col_num in range(1, 25):
            cell = sheet.cell(row=row_num, column=col_num)
            cell.alignment = Alignment(horizontal="center", vertical="center")

    # Adjust column widths to fit the content
    for col in sheet.columns:
        max_length = 0
        column = col[0].column_letter  # Get the column letter (A, B, C, etc.)
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = max_length + 2  # Add some padding to the width
        sheet.column_dimensions[column].width = adjusted_width

    # Prepare the response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=StaffRecord.xlsx'

    # Save the workbook to the response
    workbook.save(response)

    return response

def export_students_to_excel(request):
    # Create an in-memory workbook
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'Students'
    
    # Define the headers
    headers = ['Last Name', 'First Name', 'Middle Name', 'Email', 'Grade Level', 'Age', 'Date of Birth', 'Place of Birth', 
               'Sex', 'Nationality', 'Religion', 'Rank In Family', 'Telephone #',
               'Mobile #', 'Start Semester', 'End Semester', 'Created At', 'Updated At', 'Is Active']
    
    # Define a fill color for the header (e.g., light blue)
    header_fill = PatternFill(start_color="ADD8E6", end_color="ADD8E6", fill_type="solid")
    
    # Add headers to the first row and make them bold with a background color and center alignment
    for col_num, header in enumerate(headers, 1):
        cell = sheet.cell(row=1, column=col_num)
        cell.value = header
        cell.font = Font(bold=True)  # Make the header bold
        cell.fill = header_fill  # Apply background color
        cell.alignment = Alignment(horizontal="center", vertical="center")  # Center-align the text

    # Query all grade levels
    students = Students.objects.all()

    # Add data rows starting from row 2 with center alignment
    for row_num, student in enumerate(students, 2):
        sheet.cell(row=row_num, column=1).value = student.admin.last_name
        sheet.cell(row=row_num, column=2).value = student.admin.first_name
        sheet.cell(row=row_num, column=3).value = student.middle_name
        sheet.cell(row=row_num, column=4).value = student.admin.email
        sheet.cell(row=row_num, column=5).value = student.GradeLevel_id.GradeLevel_name
        sheet.cell(row=row_num, column=6).value = student.age
        sheet.cell(row=row_num, column=7).value = student.dob
        sheet.cell(row=row_num, column=8).value = student.sex
        sheet.cell(row=row_num, column=9).value = student.pob
        sheet.cell(row=row_num, column=10).value = student.nationality
        sheet.cell(row=row_num, column=11).value = student.religion
        sheet.cell(row=row_num, column=12).value = student.rank_in_family
        sheet.cell(row=row_num, column=13).value = student.telephone_nos
        sheet.cell(row=row_num, column=14).value = student.mobile_phone_nos
        sheet.cell(row=row_num, column=15).value = student.session_year_id.session_start_year
        sheet.cell(row=row_num, column=16).value = student.session_year_id.session_end_year
        sheet.cell(row=row_num, column=17).value = student.created_at.strftime('%Y-%m-%d %H:%M:%S')
        sheet.cell(row=row_num, column=18).value = student.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        sheet.cell(row=row_num, column=19).value = student.admin.is_active

        # Apply center alignment to all cells in the row
        for col_num in range(1, 20):
            cell = sheet.cell(row=row_num, column=col_num)
            cell.alignment = Alignment(horizontal="center", vertical="center")

    # Adjust column widths to fit the content
    for col in sheet.columns:
        max_length = 0
        column = col[0].column_letter  # Get the column letter (A, B, C, etc.)
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = max_length + 2  # Add some padding to the width
        sheet.column_dimensions[column].width = adjusted_width

    # Prepare the response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=StudentRecord.xlsx'

    # Save the workbook to the response
    workbook.save(response)

    return response


def manage_gradelevel(request):
    gradelevels = GradeLevel.objects.all()
    context = {
        "gradelevels": gradelevels
    }
    return render(request, 'hod_template/Manage_Template/manage_gradelevel_template.html', context)


def edit_gradelevel(request, GradeLevel_id):
    gradelevel = GradeLevel.objects.get(id=GradeLevel_id)
    context = {
        "gradelevel": gradelevel,
        "id": GradeLevel_id
    }
    return render(request, 'hod_template/Edit_Template/edit_gradelevel_template.html', context)


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
    session_years = SessionYearModel.objects.filter(is_archived=False)
    context = {
        "session_years": session_years
    }
    return render(request, "hod_template/Manage_Template/manage_session_template.html", context)

def add_session(request):
    # Get the latest session year if it exists
    latest_session = SessionYearModel.objects.order_by('-session_end_year').first()

    if latest_session:
        # Use the end year of the last session as the start year of the new session
        last_end_year = latest_session.session_end_year.year
        # Set the new session years based on the last session
        session_start_year = f"{last_end_year}-06-01"  # June 1 of the last session's end year
        session_end_year = f"{last_end_year + 1}-03-31"  # March 31 of the next year
    else:
        # If no session exists, set default values, e.g., for the current year
        current_year = datetime.now().year
        session_start_year = f"{current_year}-06-01"  # June 1 of the current year
        session_end_year = f"{current_year + 1}-03-31"  # March 31 of the next year

    print(f"Session Start Year: {session_start_year}, Session End Year: {session_end_year}")  # Debug print

    return render(request, "hod_template/Add_Template/add_session_template.html", {
        'session_start_year': session_start_year,
        'session_end_year': session_end_year
    })

def add_session_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_session')
    else:
        session_start_year = request.POST.get('session_start_year')
        session_end_year = request.POST.get('session_end_year')
        session_limit = request.POST.get('session_limit')
        session_status = "Active"

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
    return render(request, "hod_template/Edit_Template/edit_session_template.html", context)

def edit_session_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('manage_session')
    else:
        session_id = request.POST.get('session_id')
        session_start_year = request.POST.get('session_start_year')
        session_end_year = request.POST.get('session_end_year')
        session_limit = request.POST.get('session_limit')
        session_status = request.POST.get('session_status')

        try:
            session_year = SessionYearModel.objects.get(id=session_id)
            session_year.session_start_year = session_start_year
            session_year.session_end_year = session_end_year
            session_year.session_limit = session_limit
            session_year.session_status = session_status
            session_year.save()

            messages.success(request, "Session Year Updated Successfully.")
            return redirect('manage_session')
        except Exception as e:
            messages.error(request, f"Failed to Update Session Year: {e}")
            return redirect('manage_session')

def archived_sessions(request):
    # Filter session years with status 'Archived'
    session_years = SessionYearModel.objects.filter(is_archived=True)
    context = {
        "session_years": session_years
    }
    return render(request, 'hod_template/Archive_Template/archived_session_template.html', context)

def archive_session(request, session_id):
    session_year = get_object_or_404(SessionYearModel, id=session_id)
    session_year.is_archived = True
    session_year.session_status = "Inactive"
    session_year.save()
    messages.success(request, "Session archived successfully!")
    return redirect('manage_session')

def unarchive_session(request, session_id):
    session_year = get_object_or_404(SessionYearModel, id=session_id)
    session_year.is_archived = False
    session_year.session_status = "Active"
    session_year.save()
    messages.success(request, "Session unarchived successfully!")
    return redirect('manage_session')

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
    return render(request, 'hod_template/Add_Template/add_student2_template.html', context)

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
            upload_result = cloudinary.uploader.upload(profile_pic, folder="media/")
            profile_pic_url = upload_result.get('url')

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

def add_enrollment(request):
    # Get all grade levels that are not already associated with an Enrollment_voucher
    enrolled_grade_levels = Enrollment_voucher.objects.values('GradeLevel_id_id')
    gradelevels = GradeLevel.objects.exclude(id__in=Subquery(enrolled_grade_levels))
    context = {
        "gradelevels": gradelevels,
    }
    return render(request, 'hod_template/Add_Template/add_enrollment_template.html', context)

def add_enrollment_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_enrollment')

    # Retrieve and convert values from the form
    def safe_decimal(value, field_name):
        """Helper function to safely convert to Decimal with error logging."""
        try:
            return Decimal(value.strip() or '0.00')
        except InvalidOperation:
            messages.error(request, f"Invalid input for {field_name}. Please check your values.")
            raise

    try:
        # Convert and log values
        GradeLevel_id = request.POST.get('GradeLevel_id')
        registration_fee = safe_decimal(request.POST.get('registration_fee', '0.00'), 'registration fee')
        misc_fee = safe_decimal(request.POST.get('misc_fee', '0.00'), 'misc fee')
        tuition_fee = safe_decimal(request.POST.get('tuition_fee', '0.00'), 'tuition fee')
        total_fee = safe_decimal(request.POST.get('total_fee', '0.00'), 'total fee')
        
        # Create and save the enrollment instance
        enrollment = Enrollment_voucher(
            GradeLevel_id = GradeLevel.objects.get(id=GradeLevel_id),
            registration_fee=registration_fee,
            misc_fee=misc_fee,
            tuition_fee=tuition_fee,
            total_fee=total_fee,
        )
        
        enrollment.save()
        messages.success(request, "Enrollment Added Successfully!")
    except Exception as e:
        messages.error(request, f"Failed to Add Enrollment! Error: {str(e)}")
    return redirect('add_enrollment')

def manage_enrollment(request):
    # Filter students with "Pending" status
    students = Students.objects.filter(student_status="Pending")

    # Create a dictionary of vouchers by GradeLevel_id
    enrollment_vouchers = {voucher.GradeLevel_id.id: voucher for voucher in Enrollment_voucher.objects.all()}

    # Annotate each student with the relevant voucher
    for student in students:
        student.voucher = enrollment_vouchers.get(student.GradeLevel_id.id)

    context = {
        "students": students,
        'now': timezone.now(),
    }
    return render(request, 'hod_template/Manage_Template/manage_enrollment_template.html', context)

def update_student_status(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        try:
            student = Students.objects.get(id=student_id)
            student.student_status = "Paying"
            student.save()
            return JsonResponse({'success': True, 'message': 'Status updated successfully.'})
        except Students.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Student not found.'})

    return JsonResponse({'success': False, 'message': 'Invalid request.'})

# Update batch of students' statuses
def update_batch_student_status(request):
    if request.method == 'POST':
        student_ids = request.POST.getlist('student_ids[]')  # A list of student IDs
        try:
            students = Students.objects.filter(id__in=student_ids)
            students.update(student_status="Paying")
            return JsonResponse({'success': True, 'message': 'Batch status updated successfully.'})
        except Students.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Students not found.'})

    return JsonResponse({'success': False, 'message': 'Invalid request.'})

def manage_enrollment_voucher(request):
    enrollment_vouchers = Enrollment_voucher.objects.all()
    context = {
        "enrollment_vouchers": enrollment_vouchers,
    }
    return render(request, 'hod_template/Manage_Template/manage_enrollment_voucher_template.html', context)

def edit_enrollment(request, enrollment_id):
    # Retrieve the enrollment instance
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    
    # Prepare context with existing data from the enrollment instance
    context = {
        "enrollment_id": enrollment.id,
        "student_id": enrollment.student_id.id,
        "student_name": f"{enrollment.student_id.admin.first_name} {enrollment.student_id.admin.last_name}",
        "registration_fee": enrollment.registration_fee,
        "misc_fee": enrollment.misc_fee,
        "tuition_fee": enrollment.tuition_fee,
        "total_fee": enrollment.total_fee,
        "downpayment": enrollment.downpayment,
        "discount": enrollment.discount,
        "discount_amount": enrollment.discount_amount,
        "balance": enrollment.balance,
        "installment_payment": enrollment.installment_payment,
        "installment_option": enrollment.installment_option,
        "assessed_by": enrollment.assessed_by,
        "assessed_date": enrollment.assessed_date,
        "payment_received_by": enrollment.payment_received_by,
        "payment_amount": enrollment.payment_amount,
        "payment_date": enrollment.payment_date,
        "enrollment_status": enrollment.enrollment_status,
        "remarks": enrollment.remarks,
    }

    # Check for attachments and add them to the context if they exist
    attachment = getattr(enrollment, 'attachment', None)
    if attachment is not None:
        context.update({
            "id_picture_file": attachment.id_picture_file or '',  # Provide default if None
            "birth_certificate_file": attachment.psa_file or '',  # Provide default if None
            "form_138_file": attachment.form_138_file or '',  # Provide default if None
            "attachment_remarks": attachment.attachment_remarks or '',  # Provide default if None
        })
    else:
        # If no attachment exists, you might want to set default values for the context
        context.update({
            "id_picture_file": '',
            "birth_certificate_file": '',
            "form_138_file": '',
            "attachment_remarks": '',
        })

    # Render the edit template with populated data
    return render(request, "hod_template/Edit_Template/edit_enrollment_template.html", context)

def edit_enrollment_save(request, enrollment_id):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('edit_enrollment', enrollment_id=enrollment_id)

    # Retrieve the existing enrollment instance
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    student_instance = enrollment.student_id

    # Retrieve and convert values from the form
    def safe_decimal(value, field_name):
        """Helper function to safely convert to Decimal with error logging."""
        try:
            return Decimal(value.strip() or '0.00')
        except InvalidOperation:
            messages.error(request, f"Invalid input for {field_name}. Please check your values.")
            raise

    try:
        # Convert and log values
        enrollment.registration_fee = safe_decimal(request.POST.get('registration_fee', '0.00'), 'registration fee')
        enrollment.misc_fee = safe_decimal(request.POST.get('misc_fee', '0.00'), 'misc fee')
        enrollment.tuition_fee = safe_decimal(request.POST.get('tuition_fee', '0.00'), 'tuition fee')
        enrollment.total_fee = safe_decimal(request.POST.get('total_fee', '0.00'), 'total fee')
        enrollment.downpayment = safe_decimal(request.POST.get('downpayment', '0.00'), 'downpayment')
        enrollment.discount = safe_decimal(request.POST.get('discount', '0.00'), 'discount')
        enrollment.discount_amount = safe_decimal(request.POST.get('discount_amount', '0.00'), 'discount amount')
        enrollment.balance = safe_decimal(request.POST.get('balance', '0.00'), 'balance')
        enrollment.installment_payment = safe_decimal(request.POST.get('installment_payment', '0.00'), 'installment payment')
        enrollment.payment_amount = safe_decimal(request.POST.get('payment_amount', '0.00'), 'payment amount')

        enrollment.installment_option = request.POST.get('installment_option', 'Monthly')
        enrollment.assessed_by = request.POST.get('assessed_by', '')
        enrollment.assessed_date = request.POST.get('assessed_date', None)
        enrollment.payment_received_by = request.POST.get('payment_received_by', '')
        enrollment.payment_date = request.POST.get('payment_date', None)
        enrollment.enrollment_status = request.POST.get('enrollment_status', 'Pending')
        enrollment.remarks = request.POST.get('remarks', '')

        # Save the updated enrollment instance
        enrollment.save()

        # Handle file uploads from the request
        if request.POST.get('include_id_picture'):
            enrollment.attachment.id_picture_file = request.FILES.get('id_picture_file')
        if request.POST.get('include_birth_certificate'):
            enrollment.attachment.psa_file = request.FILES.get('birth_certificate_file')
        if request.POST.get('include_form_138'):
            enrollment.attachment.form_138_file = request.FILES.get('form_138_file')

        enrollment.attachment.attachment_remarks = request.POST.get('attachment_remarks', '')
        enrollment.attachment.save()

        messages.success(request, "Enrollment Updated Successfully!")
    except Exception as e:
        messages.error(request, f"Failed to Update Enrollment! Error: {str(e)}")

    return redirect('edit_enrollment', enrollment_id=enrollment_id)

def update_balance(request, enrollment_id=None):
    # Fetch enrollment based on enrollment_id
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)

    if request.method == 'POST':
        # Get form data from POST request
        payment_balance_amount = request.POST.get('payment_balance_amount')
        payment_balance_date = request.POST.get('payment_balance_date')
        payment_balance_remarks = request.POST.get('payment_balance_remarks')

        try:
            # Remove commas and convert to Decimal
            payment_balance_amount = Decimal(payment_balance_amount.replace(',', ''))

            # Store previous balance
            past_balance = enrollment.balance

            # Update the balance (ensure both are Decimal for arithmetic)
            enrollment.balance -= payment_balance_amount
            enrollment.save()

            # Create a new payment record with past balance
            BalancePayment.objects.create(
                enrollment=enrollment,
                payment_balance_amount=payment_balance_amount,
                payment_balance_date=payment_balance_date,
                payment_balance_remarks=payment_balance_remarks,
                past_balance=past_balance
            )

            # Success message
            messages.success(request, f'Balance updated successfully. Current balance: {enrollment.balance:.2f}, Past balance: {past_balance:.2f}')
            return redirect('manage_enrollment')

        except IntegrityError:
            messages.error(request, 'There was an error updating the balance. Please try again.')
        except Exception as e:
            messages.error(request, f'An unexpected error occurred: {str(e)}')

    return render(request, 'hod_template/Manage_Template/manage_enrollment_template.html', {
        'enrollment': enrollment,
        'enrollments': Enrollment.objects.all(),
    })  
 
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
    return render(request, 'hod_template/Manage_Template/manage_student_template.html', context)

def edit_student(request, student_id):
    student = Students.objects.get(admin=student_id)
    sessions = SessionYearModel.objects.all()
    gradelevels = GradeLevel.objects.all()
    parentguardian = ParentGuardian.objects.filter(students_id=student).first()
    previousschool = PreviousSchool.objects.filter(students_id=student).first()
    emergencycontact = EmergencyContact.objects.filter(students_id=student).first()

    context = {
        "student": student,
        "rank_in_family": student.rank_in_family,
        "sessions": sessions,
        "gradelevels": gradelevels,
        "parentguardian": parentguardian, 
        "previousschool": previousschool,
        "emergencycontact": emergencycontact,
    }

    return render(request, 'hod_template/Edit_Template/edit_student_template.html', context)

def edit_student_save(request, student_id):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('edit_student', student_id=student_id)

    try:
        # Fetch the student based on the provided student_id
        student = Students.objects.get(id=student_id)
        user = student.user  # The associated CustomUser instance

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
            upload_result = cloudinary.uploader.upload(profile_pic, folder="media/")
            profile_pic_url = upload_result.get('url')

        # Update the user details
        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        # Update student details
        student.middle_name = middlename
        student.suffix = suffix
        student.nickname = nickname
        student.address = address
        student.sex = sex
        student.age = age
        student.dob = dob
        student.pob = pob
        student.nationality = nationality
        student.religion = religion
        student.rank_in_family = rank_in_family
        student.telephone_nos = telephone_nos
        student.mobile_phone_nos = mobile_phone_nos
        student.is_covid_vaccinated = is_covid_vaccinated
        student.date_of_vaccination = date_of_vaccination

        if profile_pic_url:
            student.profile_pic = profile_pic_url
        
        # Assign GradeLevel and Session Year
        gradelevel_obj = GradeLevel.objects.get(id=GradeLevel_id)
        session_year_obj = SessionYearModel.objects.get(id=session_year_id)
        student.GradeLevel_id = gradelevel_obj
        student.session_year_id = session_year_obj

        # Save updated student record
        student.save()

        # Update Parent/Guardian Information (if needed)
        parent_guardian = ParentGuardian.objects.get_or_create(students_id=student)
        parent_guardian.father_name = request.POST.get('father_name')
        parent_guardian.father_occupation = request.POST.get('father_occupation')
        parent_guardian.mother_name = request.POST.get('mother_name')
        parent_guardian.mother_occupation = request.POST.get('mother_occupation')
        parent_guardian.guardian_name = request.POST.get('guardian_name')
        parent_guardian.guardian_occupation = request.POST.get('guardian_occupation')
        parent_guardian.save()

        # Update Previous School Information (if needed)
        previous_school = PreviousSchool.objects.get_or_create(students_id=student)
        previous_school.previous_school_name = request.POST.get('previous_school_name')
        previous_school.previous_school_address = request.POST.get('previous_school_address')
        previous_school.previous_grade_level = request.POST.get('previous_grade_level')
        previous_school.previous_school_year_attended = request.POST.get('previous_school_year_attended')
        previous_school.previous_teacher_name = request.POST.get('previous_teacher_name')
        previous_school.save()

        # Update Emergency Contact Information (if needed)
        emergency_contact = EmergencyContact.objects.get_or_create(students_id=student)
        emergency_contact.emergency_contact_name = request.POST.get('emergency_contact_name')
        emergency_contact.emergency_contact_relationship = request.POST.get('emergency_contact_relationship')
        emergency_contact.emergency_contact_address = request.POST.get('emergency_contact_address')
        emergency_contact.emergency_contact_phone = request.POST.get('emergency_contact_phone')
        emergency_contact.emergency_enrolling_teacher = request.POST.get('emergency_enrolling_teacher')
        emergency_contact.emergency_date = request.POST.get('emergency_date')
        emergency_contact.emergency_referred_by = request.POST.get('emergency_referred_by')
        emergency_contact.save()

        messages.success(request, "Student Information Updated Successfully!")
        return redirect('edit_student', student_id=student_id)

    except Students.DoesNotExist:
        messages.error(request, "Student Not Found!")
        return redirect('edit_student', student_id=student_id)

    except Exception as e:
        messages.error(request, f"Failed to Update Student! Error: {str(e)}")
        return redirect('edit_student', student_id=student_id)

def deactivate_student(request, student_id):
    student = Students.objects.get(admin=student_id)
    try:
        # Set the is_active field of the associated CustomUser to False
        student.admin.is_active = False
        student.admin.save()
        
        messages.success(request, "Student Deactivated Successfully.")
        return redirect('manage_student')
    except Exception as e:
        print(e)
        messages.error(request, "Failed to Deactivate Student.")
        return redirect('manage_student')

def manage_section(request):
    gradelevels = GradeLevel.objects.all()
    sections = Section.objects.all()

    context = {
        "sections": sections,
        "gradelevels":gradelevels,
    }
    return render(request, "hod_template/Manage_Template/manage_section_template.html", context)

def add_section(request):
    gradelevels = GradeLevel.objects.all()
    context = {
        "gradelevels":gradelevels,
    }
    return render(request, 'hod_template/Add_Template/add_section_template.html', context)

def add_section_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_section')
    else:
        section_name = request.POST.get('section_name')
        section_limit = request.POST.get('section_limit')
        section_soft_limit = request.POST.get('section_soft_limit')
        GradeLevel_id = request.POST.get('gradelevel')
        gradelevel = GradeLevel.objects.get(id=GradeLevel_id)
        
        try:
            section = Section(
                section_name = section_name,
                section_soft_limit = section_soft_limit,
                section_limit = section_limit,
                GradeLevel_id=gradelevel)
            section.save()
            messages.success(request, "Section Added Successfully!")
            return redirect('add_section')
        except:
            messages.error(request, "Failed to Add Section!")
            return redirect('add_section')

def edit_section(request, section_id):

    section = Section.objects.get(id=section_id)
    gradelevel = GradeLevel.objects.all()

    context = {
        "section": section,
        "gradelevel":gradelevel,
    }

    return render(request, 'hod_template/Edit_Template/edit_section_template.html', context)

def edit_section_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        section_id = request.POST.get('section_id')
        section_name = request.POST.get('section_name')
        section_limit = request.POST.get('section_limit')
        section_soft_limit = request.POST.get('section_soft_limit')
        GradeLevel_id = request.POST.get('gradelevel')
        
        try:
            section = Section.objects.get(id=section_id)
            section.section_name = section_name

            gradelevel = GradeLevel.objects.get(id=GradeLevel_id)
            section.GradeLevel_id = gradelevel

            section_limit = section_limit
            section_soft_limit = section_soft_limit

            section.save()

            messages.success(request, "Section Updated Successfully.")
            # return redirect('/edit_subject/'+subject_id)
            return HttpResponseRedirect(reverse("edit_section", kwargs={"section_id":section_id}))
        except:
            messages.error(request, "Failed to Update Section.")
            return HttpResponseRedirect(reverse("edit_section", kwargs={"section_id":section_id}))
            # return redirect('/edit_subject/'+subject_id)

def add_subject(request):
    curriculums = Curriculums.objects.all()
    gradelevels = GradeLevel.objects.all()
    context = {
        "curriculums": curriculums,
        "gradelevels": gradelevels
        
    }
    return render(request, 'hod_template/Add_Template/add_subject_template.html', context)

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
    return render(request, 'hod_template/Manage_Template/manage_subject_template.html', context)

def manage_classroom(request):
    classroom = Classroom.objects.all()
    context = {
        "classrooms": classroom
    }
    return render(request, 'hod_template/Manage_Template/manage_classroom_template.html', context)

def fetch_classroom(request):
    api_url = "https://inventoryapp1-o2l3.onrender.com/classroom/"

    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        data = response.json()
        classrooms = data.get("classrooms", [])

        # Step 1: Fetch all IDs from the external API
        external_ids = [classroom["id"] for classroom in classrooms]

        # Step 2: Update or create records for all received data
        for classroom in classrooms:
            Classroom.objects.update_or_create(
                id=classroom["id"],
                defaults={
                    "classroom_name": classroom["classroom_name"],
                    "status": classroom["status"],  # Handle new 'status' field
                },
            )

        # Step 3: Identify and delete records that are no longer in the external API
        Classroom.objects.exclude(id__in=external_ids).delete()

        # Add a success message
        messages.success(request, "Classrooms synchronized successfully.")
        return redirect("manage_classroom")  # Redirect to the same page

    except requests.RequestException as e:
        messages.error(request, f"Request failed: {str(e)}")
        return redirect("manage_classroom")

    except Exception as e:
        messages.error(request, f"An unexpected error occurred: {str(e)}")
        return redirect("manage_classroom")

# class ManageSubjectsAPIView(APIView):
#     permission_classes = [IsAuthenticated]  # Only authenticated users

#     def post(self, request):
#         refresh_token = request.data.get("refresh_token")
#         if not refresh_token:
#             return Response({"error": "Refresh token is required"}, status=400)

#         try:
#             token = RefreshToken(refresh_token)

#             if token.check_blacklist():
#                 return Response({"error": "Token is blacklisted"}, status=403)
            
#             user_id = token.get("user_id")

#             user = CustomUser.objects.get(id=user_id)

#             if user.user_type != "1":
#                 return Response({"error": "You do not have permission to view this resource."}, status=403)

#             subjects = Subjects.objects.all().values(
#                 "id", 
#                 "curriculum_id__curriculum_name", 
#                 "GradeLevel_id__GradeLevel_name",
#                 "subject_name", 
#                 "subject_description", 
#                 "subject_code", 
#                 "subject_hours", 
#                 "created_at", 
#                 "updated_at"
#             )
#             return Response({"subjects": list(subjects)}, status=200)
        
#         except TokenError as e:
#             return Response({"error": f"Token error: {str(e)}"}, status=403)
#         except CustomUser.DoesNotExist:
#             return Response({"error": "User not found"}, status=404)
#         except Exception as e:
#             return Response({"error": str(e)}, status=400)

def edit_subject(request, subject_id):
    subject = Subjects.objects.get(id=subject_id)
    gradelevels = GradeLevel.objects.all()
    
    context = {
        "subject": subject,
        "gradelevels": gradelevels,
        "id": subject_id
    }
    return render(request, 'hod_template/Edit_Template/edit_subject_template.html', context)

def edit_subject_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        subject_id = request.POST.get('subject_id')
        GradeLevel_id = request.POST.get('gradelevel')
        subject_name = request.POST.get('subject')
        
        subject_code = request.POST.get('subject_code')
        subject_description = request.POST.get('subject_description')
        subject_hours = request.POST.get('subject_hours')
        
        try:
            subject = Subjects.objects.get(id=subject_id)
            subject.subject_name = subject_name
            
            gradelevel = GradeLevel.objects.get(id=GradeLevel_id)
            subject.GradeLevel_id = gradelevel
            
            subject.subject_code = subject_code
            subject.subject_description = subject_description
            subject.subject_hours = subject_hours
            
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
    # Filter grade levels for students with student_status="Enrolled"
    gradelevels = GradeLevel.objects.filter(
        id__in=Students.objects.filter(
            student_status="Enrolled"  # Only include enrolled students
        ).values_list('GradeLevel_id', flat=True)
    )
    context = {
        "gradelevels": gradelevels,
    }
    return render(request, 'hod_template/Add_Template/add_assignsection_template.html', context)


# def add_assignsection(request):
#     # Filter grade levels only for students present in the Enrollment table
#     gradelevels = GradeLevel.objects.filter(
#         id__in=Students.objects.filter(
#             id__in=Enrollment.objects.values_list('student_id', flat=True)
#         ).values_list('GradeLevel_id', flat=True)
#     )
#     context = {
#         "gradelevels": gradelevels,
#     }
#     return render(request, 'hod_template/Add_Template/add_assignsection_template.html', context)

def load_sections_and_students(request):
    gradelevel_id = request.GET.get('gradelevel_id')
    
    # Fetch sections and students filtered by GradeLevel
    sections = Section.objects.filter(GradeLevel_id=gradelevel_id)

    # Get all students in the GradeLevel who are NOT already assigned to a section
    assigned_students = AssignSection.objects.filter(GradeLevel_id=gradelevel_id).values_list('Student_id', flat=True)
    students = Students.objects.filter(
        GradeLevel_id=gradelevel_id,
        student_status="Enrolled"  # Only include students with status "Enrolled"
    ).exclude(id__in=assigned_students)

    # Prepare data for response
    section_list = [{"id": section.id, "name": section.section_name} for section in sections]
    student_list = [{"id": student.id, "name": f"{student.admin.first_name} {student.admin.last_name}"} for student in students]
    
    return JsonResponse({'sections': section_list, 'students': student_list})

# def load_sections_and_students(request):
#     gradelevel_id = request.GET.get('gradelevel_id')
    
#     # Fetch sections by GradeLevel
#     sections = Section.objects.filter(GradeLevel_id=gradelevel_id)

#     # Get all students in the GradeLevel who are NOT already assigned to a section
#     assigned_students = AssignSection.objects.filter(GradeLevel_id=gradelevel_id).values_list('Student_id', flat=True)
#     students = Students.objects.filter(
#         GradeLevel_id=gradelevel_id,
#         id__in=Enrollment.objects.values_list('student_id', flat=True)  # Only include enrolled students
#     ).exclude(id__in=assigned_students)

#     # Prepare data for response
#     section_list = [{"id": section.id, "name": section.section_name} for section in sections]
#     student_list = [{"id": student.id, "name": f"{student.admin.first_name} {student.admin.last_name}"} for student in students]
    
#     return JsonResponse({'sections': section_list, 'students': student_list})


def add_assignsection_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_assignsection')
    else:
        try:
            gradelevel_id = request.POST.get('GradeLevel_id')
            gradelevel = GradeLevel.objects.get(id=gradelevel_id)

            section_id = request.POST.get('section_id')
            section = Section.objects.get(id=section_id)

            # Get the list of student_ids
            student_ids = request.POST.getlist('student_ids')

            if not student_ids:
                messages.error(request, "No students selected!")
                return redirect('add_assignsection')

            # Check the current count of students in this section
            current_count = AssignSection.objects.filter(section_id=section).count()
            remaining_slots = section.section_limit - current_count

            # Filter students to add based on remaining slots
            students_to_add = student_ids[:remaining_slots]  # Students that can be added within the limit
            students_not_added = student_ids[remaining_slots:]  # Students exceeding the limit

            # Proceed to save the assignment for each student within the limit
            for student_id in students_to_add:
                student = Students.objects.get(id=student_id)
                assignsection = AssignSection(
                    GradeLevel_id=gradelevel, 
                    section_id=section,
                    Student_id=student
                )
                assignsection.save()

            # Prepare a success message
            success_message = f"{len(students_to_add)} students assigned successfully to section '{section.section_name}'."
            
            # If there are students that couldn't be added, prepare a warning message
            if students_not_added:
                not_added_names = [Students.objects.get(id=student_id).admin.get_full_name() for student_id in students_not_added]
                warning_message = f"However, the following students could not be assigned due to the section limit of {section.section_limit}: {', '.join(not_added_names)}."
                messages.warning(request, warning_message)
            
            messages.success(request, success_message)
            return redirect('add_assignsection')

        except Exception as e:
            messages.error(request, f"Failed to Assign Section! Error: {e}")
            return redirect('add_assignsection')



def add_load(request):
    # Fetch all necessary data for the context
    session_years = SessionYearModel.objects.all()
    curriculums = Curriculums.objects.all()
    assignsections = AssignSection.objects.select_related('GradeLevel_id', 'section_id').distinct('GradeLevel_id', 'section_id')
    gradelevels = GradeLevel.objects.all()
    sections = Section.objects.all()
    subjects = Subjects.objects.all()
    
    staffs = CustomUser.objects.filter(user_type='2')
    # Fetching existing loads to display in the table
    loads = Load.objects.select_related('curriculum_id', 'AssignSection_id', 'subject_id', 'staff_id').all()  
    context = {
        "session_years":session_years,
        "curriculums": curriculums,
        "assignsections": assignsections,
        "gradelevels": gradelevels,
        "sections": sections,
        "subjects": subjects,
        "staffs": staffs,
        "loads": loads,
    }
    return render(request, 'hod_template/Add_Template/add_load_template.html', context)

def add_load_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_load')
    else:
        try:
            # Retrieve form data
            session_year_id = request.POST.get('session_year_id')
            session_id = SessionYearModel.objects.get(id=session_year_id)

            curriculum_id = request.POST.get('curriculum_id')
            curriculum = Curriculums.objects.get(id=curriculum_id)

            assignsection_id = request.POST.get('AssignSection_id')  # Adjusted to use AssignSection_id
            assignsection = AssignSection.objects.get(id=assignsection_id)

            subject_id = request.POST.get('subject_id')
            subject = Subjects.objects.get(id=subject_id)

            staff_id = request.POST.get('staff_id')
            staff_user = CustomUser.objects.get(id=staff_id)

            is_advisory = request.POST.get('is_advisory')

            # Check if the subject is already assigned to this section in the same session
            conflicting_load = Load.objects.filter(
                session_year_id=session_id,
                AssignSection_id=assignsection,
                subject_id=subject
            ).first()  # Get the first conflicting load record

            if conflicting_load:
                conflict_details = (
                    f"Conflict detected: {assignsection.GradeLevel_id.GradeLevel_name} - {assignsection.section_id.section_name} "
                    f"already has {conflicting_load.staff_id.first_name} "
                    f"{conflicting_load.staff_id.last_name} assigned for subject {subject.subject_name}."
                )
                messages.warning(request, f"WARNING!!! {conflict_details}")
                return redirect('add_load')

            # Check for duplicate load entry with the same staff
            if Load.objects.filter(
                session_year_id=session_id,
                curriculum_id=curriculum,
                AssignSection_id=assignsection,
                subject_id=subject,
                staff_id=staff_user
            ).exists():
                messages.warning(request, "WARNING!!! This load record already exists for this faculty.")
                return redirect('add_load')

            # Get the related Staff instance
            staff = Staffs.objects.get(admin=staff_user)

            # Count the current number of loads for the selected academic year
            current_load = Load.objects.filter(
                session_year_id=session_id,
                staff_id=staff_user
            ).count()

            # Check if the current load exceeds or equals the staff's max_load for the selected academic year
            if current_load >= staff.max_load:
                messages.error(request, f"{staff_user.first_name} {staff_user.last_name} has reached the maximum load limit of {staff.max_load} for the academic year {session_id.session_start_year} - {session_id.session_end_year}.")
                return redirect('add_load')

            # Saving the load
            load = Load(
                session_year_id=session_id,
                curriculum_id=curriculum,
                AssignSection_id=assignsection,
                subject_id=subject,
                staff_id=staff_user,
                is_advisory=is_advisory
            )
            load.save()

            messages.success(request, "Load Added Successfully!")
            return redirect('add_load')

        except Exception as e:
            messages.error(request, f"Failed to Add Load! Error: {e}")
            return redirect('add_load')



def add_schedule(request):
    gradelevels = GradeLevel.objects.all()
    sections = Section.objects.all()
    loads = Load.objects.all()  
    context = {
        'gradelevels': gradelevels,
        'sections': sections,
        "loads": loads,  
    }
    return render(request, 'hod_template/Add_Template/add_schedule_template.html', context)


def add_schedule_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_schedule')
    else:
        try:
            # Retrieve form data
            session_year_id = request.POST.get('session_year_id')
            session_id = SessionYearModel.objects.get(id=session_year_id)
            
            staff_id = request.POST.get('staff_id')
            staff = CustomUser.objects.get(id=staff_id)

            load_id = request.POST.get('load_id')
            load = Load.objects.get(id=load_id)

            day_of_week = request.POST.get('day_of_week')
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')

            # Convert start and end times to Python time objects
            start_time_obj = time.fromisoformat(start_time)
            end_time_obj = time.fromisoformat(end_time)

            # Set the allowed time range
            allowed_start = time(7, 0)  # 7:00 AM
            allowed_end = time(17, 0)   # 5:00 PM

            # Check if the times fall within the allowed range
            if not (allowed_start <= start_time_obj < allowed_end) or not (allowed_start < end_time_obj <= allowed_end):
                messages.warning(request, "Schedule times must be between 8:00 AM and 3:00 PM.")
                return redirect('add_schedule')

            # Check for any overlapping schedules
            conflicting_schedules = Schedule.objects.filter(
                session_year_id=session_id,
                staff_id=staff,
                day_of_week=day_of_week
            ).filter(
                Q(start_time__lt=end_time_obj) & Q(end_time__gt=start_time_obj)
            )

            if conflicting_schedules.exists():
                # Get details of the first conflicting schedule for the message
                conflict = conflicting_schedules.first()
                conflict_details = (
                    f"Staff {staff.first_name} {staff.last_name} already has a schedule for "
                    f"{conflict.load_id.subject_id.subject_name} on {day_of_week} from "
                    f"{conflict.start_time.strftime('%I:%M %p')} to {conflict.end_time.strftime('%I:%M %p')}."
                )

                messages.warning(request, f"WARNING!!! Schedule conflict detected: {conflict_details}")
                return redirect('add_schedule')

            # Save the new schedule if no conflicts
            schedule = Schedule(
                session_year_id=session_id,
                staff_id=staff, 
                load_id=load,
                day_of_week=day_of_week,
                start_time=start_time,
                end_time=end_time
            )
            schedule.save()

            messages.success(request, "Schedule Added Successfully!")
            return redirect('add_schedule')
        
        except Exception as e:
            print(e)  # For debugging
            messages.error(request, f"Failed to Add Schedule! Error: {e}")
            return redirect('add_schedule')

    # Return the data as a JSON response
    return JsonResponse(load_data, safe=False)

def manage_assign_section(request):
    assignsections = AssignSection.objects.all()
    context = {
        "assignsections": assignsections
    }
    return render(request, 'hod_template/Manage_Template/manage_assignsection_template.html', context)

def manage_load_scheduling(request):
    loads = Load.objects.all()
    context = {
        "loads": loads,
    }
    return render(request, 'hod_template/Manage_Template/manage_load_template.html', context)

def manage_class_scheduling(request):
    gradelevels = GradeLevel.objects.all()
    sections = Section.objects.all()
    schedules = Schedule.objects.all()
    context = {
        "gradelevels": gradelevels,
        "sections": sections,
        "schedules": schedules,
    }
    return render(request, 'hod_template/Manage_Template/manage_schedule_template.html', context)

def filter_schedules(request):
    gradelevel_id = request.GET.get('gradelevel_id')
    section_id = request.GET.get('section_id')

    if gradelevel_id and section_id:
        schedules = Schedule.objects.filter(
            load_id__AssignSection_id__GradeLevel_id_id=gradelevel_id,
            load_id__AssignSection_id__section_id_id=section_id
        ).select_related('load_id', 'staff_id')

        schedule_data = [
            {
                'id': schedule.id,
                'grade_section': f"{schedule.load_id.AssignSection_id.GradeLevel_id.GradeLevel_name} - {schedule.load_id.AssignSection_id.section_id.section_name}",
                'subject': schedule.load_id.subject_id.subject_name,
                'staff': f"{schedule.staff_id.first_name} {schedule.staff_id.last_name}",
                'day_of_week': schedule.day_of_week,
                'start_time': schedule.start_time.strftime('%I:%M %p'),
                'end_time': schedule.end_time.strftime('%I:%M %p')
            }
            for schedule in schedules
        ]
        return JsonResponse({'schedules': schedule_data})
    return JsonResponse({'schedules': []})

def fetch_schedules(request):
    grade_level_id = request.GET.get('gradelevel_id')
    section_id = request.GET.get('section_id')

    if grade_level_id and section_id:
        schedules = Schedule.objects.filter(
            load_id__AssignSection_id__GradeLevel_id=grade_level_id,
            load_id__AssignSection_id__section_id=section_id
        ).select_related('load_id__AssignSection_id', 'load_id__subject_id', 'staff_id')
        
        schedule_data = [
            {
                'id': schedule.id,
                'grade_level': schedule.load_id.AssignSection_id.GradeLevel_id.GradeLevel_name,
                'section': schedule.load_id.AssignSection_id.section_id.section_name,
                'subject': schedule.load_id.subject_id.subject_name,
                'staff': f"{schedule.staff_id.first_name} {schedule.staff_id.last_name}",
                'day_of_week': schedule.day_of_week,
                'start_time': schedule.start_time.strftime("%I:%M %p"),
                'end_time': schedule.end_time.strftime("%I:%M %p"),
            }
            for schedule in schedules
        ]
        
        return JsonResponse({'schedules': schedule_data}, safe=False)

    return JsonResponse({'schedules': []}, safe=False)


def fetch_load_data(request):
    grade_level_id = request.GET.get('gradelevel_id')
    section_id = request.GET.get('section_id')

    if grade_level_id and section_id:
        # Get the load_ids that are already scheduled
        scheduled_load_ids = Schedule.objects.values_list('load_id', flat=True)

        # Filter out the loads that are already scheduled
        loads = Load.objects.filter(
            AssignSection_id__GradeLevel_id=grade_level_id,
            AssignSection_id__section_id=section_id
        ).exclude(id__in=scheduled_load_ids).select_related('AssignSection_id', 'subject_id', 'staff_id')
        
        load_data = [
            {
                'id': load.id,
                'session_year': f"{load.session_year_id.session_start_year.year}-{load.session_year_id.session_end_year.year}",
                'subject': load.subject_id.subject_name,
                'staff': f"{load.staff_id.first_name} {load.staff_id.last_name}",
                'grade_level': load.AssignSection_id.GradeLevel_id.GradeLevel_name,
                'section': load.AssignSection_id.section_id.section_name,
            }
            for load in loads
        ]
        
        return JsonResponse({'loads': load_data}, safe=False)

    return JsonResponse({'loads': []}, safe=False)

def check_schedule_conflict(request):
    if request.method == 'GET':
        day_of_week = request.GET.get('day_of_week')
        start_time = request.GET.get('start_time')
        end_time = request.GET.get('end_time')
        gradelevel_id = request.GET.get('gradelevel_id')
        section_id = request.GET.get('section_id')

        # Ensure all required data is provided
        if not (day_of_week and start_time and end_time and gradelevel_id and section_id):
            return JsonResponse({"conflict": False, "message": "Incomplete data provided."})

        # Convert times to time objects
        start_time = time.fromisoformat(start_time)
        end_time = time.fromisoformat(end_time)

        # Check for schedule conflicts in the database
        conflicts = Schedule.objects.filter(
            load_id__AssignSection_id__GradeLevel_id=gradelevel_id,
            load_id__AssignSection_id__section_id=section_id,
            day_of_week=day_of_week,
        ).filter(
            Q(start_time__lt=end_time) & Q(end_time__gt=start_time)  # Overlapping condition
        )

        # If conflicts exist, return conflict details
        if conflicts.exists():
            # Get the first conflicting schedule for detailed response
            conflicting_schedule = conflicts.first()
            
            # Format the start and end times to include AM/PM
            formatted_start_time = conflicting_schedule.start_time.strftime("%I:%M %p")  # Example: 02:30 PM
            formatted_end_time = conflicting_schedule.end_time.strftime("%I:%M %p")      # Example: 03:20 PM
            
            return JsonResponse({
                "conflict": True,
                "message": (
                    f"Time conflict detected with existing schedule for "
                    f"{conflicting_schedule.load_id.subject_id.subject_name} taught by {conflicting_schedule.load_id.staff_id.first_name} "
                    f"on {conflicting_schedule.day_of_week} from {formatted_start_time} to {formatted_end_time}."
                )
            })

        # No conflicts found
        return JsonResponse({"conflict": False, "message": "No conflicts detected."})

    # Return a 405 Method Not Allowed for non-GET requests
    return JsonResponse({"error": "Invalid request method. Only GET is allowed."}, status=405)

@csrf_exempt
def save_schedule(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("Received Data:", data)  # Log the incoming data

            schedules = data.get('schedules', [])
            for schedule in schedules:
                # Retrieve the Load object using the provided load_id
                load = Load.objects.get(id=schedule['load_id'])  # Get the load associated with this schedule
                
                # Create the schedule entry
                Schedule.objects.create(
                    load_id=load,  # Use load_id directly here
                    day_of_week=schedule['day_of_week'],
                    start_time=schedule['start_time'],
                    end_time=schedule['end_time']
                )

            # Set a success message in the session (you can also include this in the response if needed)
            messages.success(request, "Schedule/s saved successfully!")

            # Return a JsonResponse with the redirect URL
            return JsonResponse({
                "message": "Schedules saved successfully!",
                "redirect_url": "/add_schedule/"  # Include the redirect URL in the response
            })
        except Exception as e:
            print(e)
            return JsonResponse({"message": str(e)}, status=400)
    
    return JsonResponse({"message": "Invalid request method"}, status=405)

def search_schedule(request):
    query = request.GET.get('query', '').strip()  # Get the query and trim spaces

    # Redirect to the schedule management page if the query is empty
    if not query:
        return redirect('manage_class_scheduling')  # Use the name of your URL pattern for manage_class_scheduling

    # Try to parse the time query (e.g., '08:00 a.m.')
    time_query = None
    try:
        # Convert query to 24-hour time format
        time_query = dt.strptime(query, '%I:%M %p').time()  # '%I:%M %p' is the format for '08:00 a.m.'
    except ValueError:
        pass  # If the time format doesn't match, just ignore

    if time_query:
        # If time query is valid, filter by start_time and end_time
        schedules = Schedule.objects.filter(
            Q(start_time__exact=time_query) | Q(end_time__exact=time_query)
        )
    else:
        # Otherwise, perform search based on other criteria
        schedules = Schedule.objects.filter(
            Q(load_id__subject_id__subject_name__icontains=query) |
            Q(load_id__staff_id__first_name__icontains=query) |
            Q(load_id__staff_id__last_name__icontains=query) |
            Q(load_id__AssignSection_id__GradeLevel_id__GradeLevel_name__icontains=query) |
            Q(load_id__AssignSection_id__section_id__section_name__icontains=query)
        )

    gradelevels = GradeLevel.objects.all()
    sections = Section.objects.all()

    context = {
        "gradelevels": gradelevels,
        "sections": sections,
        "schedules": schedules,
        "search_query": query,  # Pass the search query to the template
    }

    return render(request, 'hod_template/Manage_Template/manage_schedule_template.html', context)
    


def edit_schedule(request, schedule_id):
    # Adding Schedule ID into Session Variable
    request.session['schedule_id'] = schedule_id

    try:
        # Retrieve the schedule object using the provided schedule_id
        schedule = Schedule.objects.get(id=schedule_id)
    except Schedule.DoesNotExist:
        messages.error(request, "Schedule does not exist.")
        return redirect('manage_class_scheduling')  # Adjust this redirect based on your URL names

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

    return render(request, "hod_template/Edit_Template/edit_schedule_template.html", context)

def edit_schedule_save(request):
    if request.method != "POST":
        return HttpResponse("Invalid Method!")
    else:
        schedule_id = request.session.get('schedule_id')
        if schedule_id is None:
            return redirect('/manage_class_scheduling')

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



