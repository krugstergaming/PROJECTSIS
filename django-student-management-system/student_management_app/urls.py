
from django.urls import path, include
from . import views 
from .import HodViews, StaffViews, StudentViews
from django.contrib.auth import views as auth_views
from django.conf import settings
from .views import LoginAPIView, LogoutView, DecodeRefreshTokenView
# from .HodViews import ManageSubjectsAPIView


urlpatterns = [
    path('', views.loginPage, name="login"),
    path('doLogin/', LoginAPIView.as_view(), name="doLogin"),
    path('get_user_details/', DecodeRefreshTokenView.as_view(), name="get_user_details"),
    path('logout_user/', LogoutView.as_view(), name="logout_user"),
    path('admin_home/', HodViews.admin_home, name="admin_home"),
    path('add_staff/', HodViews.add_staff, name="add_staff"),
    path('add_staff_save/', HodViews.add_staff_save, name="add_staff_save"),

    path('manage_staff/', HodViews.manage_staff, name="manage_staff"),
    path('toggle_grading_state/', HodViews.toggle_grading_state, name='toggle_grading_state'),

    path('edit_staff/<staff_id>/', HodViews.edit_staff, name="edit_staff"),
    path('edit_staff_save/', HodViews.edit_staff_save, name="edit_staff_save"),
    path('delete_staff/<staff_id>/', HodViews.deactivate_staff, name="delete_staff"),


    path('add_curriculum/', HodViews.add_curriculum, name="add_curriculum"),
    path('add_curriculum_save/', HodViews.add_curriculum_save, name="add_curriculum_save"),
    path('manage_curriculum/', HodViews.manage_curriculum, name="manage_curriculum"),
    path('edit_curriculum/<curriculum_id>/', HodViews.edit_curriculum, name="edit_curriculum"),
    path('edit_curriculum_save/', HodViews.edit_curriculum_save, name="edit_curriculum_save"),
    
    path('archive_curriculum/<curriculum_id>/', HodViews.archive_curriculum, name="archive_curriculum"),
    path('unarchive_curriculum/<curriculum_id>/', HodViews.unarchive_curriculum, name="unarchive_curriculum"),
    path('archived_curriculums/', HodViews.archived_curriculums, name='archived_curriculums'),

    path('add_gradelevel/', HodViews.add_gradelevel, name="add_gradelevel"),
    path('add_gradelevel_save/', HodViews.add_gradelevel_save, name="add_gradelevel_save"),
    path('export-gradelevels/', HodViews.export_gradelevels_to_excel, name="export_gradelevels_to_excel"),
    path('export-staffs/', HodViews.export_staffs_to_excel, name="export_staffs_to_excel"),
    path('export-students/', HodViews.export_students_to_excel, name="export_students_to_excel"),
    path('manage_gradelevel/', HodViews.manage_gradelevel, name="manage_gradelevel"),
    path('edit_gradelevel/<GradeLevel_id>/', HodViews.edit_gradelevel, name="edit_gradelevel"),
    path('edit_gradelevel_save/', HodViews.edit_gradelevel_save, name="edit_gradelevel_save"),
    path('delete_gradelevel/<GradeLevel_id>/', HodViews.delete_gradelevel, name="delete_gradelevel"),

    path('manage_session/', HodViews.manage_session, name="manage_session"),
    path('add_session/', HodViews.add_session, name="add_session"),
    path('add_session_save/', HodViews.add_session_save, name="add_session_save"),
    path('edit_session/<session_id>', HodViews.edit_session, name="edit_session"),
    path('edit_session_save/', HodViews.edit_session_save, name="edit_session_save"),
    path('delete_session/<session_id>/', HodViews.delete_session, name="delete_session"),
    
    path('archive_session/<session_id>/', HodViews.archive_session, name="archive_session"),
    path('unarchive_session/<session_id>/', HodViews.unarchive_session, name="unarchive_session"),
    path('archived_sessions/', HodViews.archived_sessions, name='archived_sessions'),


    path('add_student/', HodViews.add_student, name="add_student"),
    path('add_student_save/', HodViews.add_student_save, name="add_student_save"),
    path('edit_student/<student_id>', HodViews.edit_student, name="edit_student"),
    path('edit_student_save/', HodViews.edit_student_save, name="edit_student_save"),
    path('manage_student/', HodViews.manage_student, name="manage_student"),


    # enrollment urls
    path('add_enrollment/', HodViews.add_enrollment, name="add_enrollment"),
    path('add_enrollment_save/', HodViews.add_enrollment_save, name="add_enrollment_save"),
    path('manage_enrollment/', HodViews.manage_enrollment, name="manage_enrollment"),
    path('manage_enrollment_voucher', HodViews.manage_enrollment_voucher, name="manage_enrollment_voucher"),
    path('manage_enrollment/<int:enrollment_id>/', HodViews.update_balance, name="update_balance"),
    path('edit_enrollment/<enrollment_id>/', HodViews.edit_enrollment, name="edit_enrollment"),
    path('edit_enrollment_save/', HodViews.edit_enrollment_save, name="edit_enrollment_save"),

    path('update-student-status/', HodViews.update_student_status, name='update-student-status'),
    path('update-batch-student-status/', HodViews.update_batch_student_status, name='update_batch_student_status'),


    path('add_load/', HodViews.add_load, name="add_load"),
    path('add_load_save/', HodViews.add_load_save, name="add_load_save"),
    # path('edit_load/<load_id>', HodViews.edit_load, name="edit_load"),
    # path('edit_load_save/', HodViews.edit_load_save, name="edit_load_save"),
    # path('manage_load/', HodViews.manage_load, name="manage_load"),



    path('add_assignsection/', HodViews.add_assignsection, name="add_assignsection"),
    path('load_sections_and_students/', HodViews.load_sections_and_students, name='load_sections_and_students'),
    path('add_assignsection_save/', HodViews.add_assignsection_save, name="add_assignsection_save"),
    

    
    path('add_schedule/', HodViews.add_schedule, name="add_schedule"),
    path('add_schedule_save/', HodViews.add_schedule_save, name="add_schedule_save"),
    path('edit_schedule/<schedule_id>', HodViews.edit_schedule, name="edit_schedule"),
    path('edit_schedule_save/', HodViews.edit_schedule_save, name="edit_schedule_save"),

    path('manage_class_scheduling/', HodViews.manage_class_scheduling, name="manage_class_scheduling"),
    path('manage_assign_section/', HodViews.manage_assign_section, name="manage_assign_section"),
    path('manage_load_scheduling/', HodViews.manage_load_scheduling, name="manage_load_scheduling"),

    path('manage_classroom/', HodViews.manage_classroom, name="manage_classroom"),
    path('fetch_classroom/', HodViews.fetch_classroom, name="fetch_classroom"),
    path('filter_schedules/', HodViews.filter_schedules, name='filter_schedules'),
    path('fetch_schedules/', HodViews.fetch_schedules, name='fetch_schedules'), 
    path('fetch_load_data/', HodViews.fetch_load_data, name='fetch_load_data'),
    path('save_schedule/', HodViews.save_schedule, name='save_schedule'),
    path('search_schedule/', HodViews.search_schedule, name='search_schedule'),
    path('check_schedule_conflict/', HodViews.check_schedule_conflict, name='check_schedule_conflict'),

    path('add_subject/', HodViews.add_subject, name="add_subject"),
    path('add_subject_save/', HodViews.add_subject_save, name="add_subject_save"),
    path('manage_subject/', HodViews.manage_subject, name="manage_subject"),
    # path('manage_subject/api', ManageSubjectsAPIView.as_view(), name="manage_subject_json"),
    path('edit_subject/<subject_id>/', HodViews.edit_subject, name="edit_subject"),
    path('edit_subject_save/', HodViews.edit_subject_save, name="edit_subject_save"),
    path('delete_subject/<subject_id>/', HodViews.delete_subject, name="delete_subject"),


    path('add_section/', HodViews.add_section, name="add_section"),
    path('add_section_save/', HodViews.add_section_save, name="add_section_save"),
    path('manage_section/', HodViews.manage_section, name="manage_section"),
    path('edit_section/<section_id>/', HodViews.edit_section, name="edit_section"),
    path('edit_section_save/', HodViews.edit_section_save, name="edit_section_save"),
    # path('delete_section/<section_id>/', HodViews.delete_section, name="delete_section"),

    path('check_email_exist/', HodViews.check_email_exist, name="check_email_exist"),
    path('check_username_exist/', HodViews.check_username_exist, name="check_username_exist"),
    path('student_feedback_message/', HodViews.student_feedback_message, name="student_feedback_message"),
    path('student_feedback_message_reply/', HodViews.student_feedback_message_reply, name="student_feedback_message_reply"),
    path('staff_feedback_message/', HodViews.staff_feedback_message, name="staff_feedback_message"),
    path('staff_feedback_message_reply/', HodViews.staff_feedback_message_reply, name="staff_feedback_message_reply"),
    path('student_leave_view/', HodViews.student_leave_view, name="student_leave_view"),
    path('student_leave_approve/<leave_id>/', HodViews.student_leave_approve, name="student_leave_approve"),
    path('student_leave_reject/<leave_id>/', HodViews.student_leave_reject, name="student_leave_reject"),
    path('staff_leave_view/', HodViews.staff_leave_view, name="staff_leave_view"),
    path('staff_leave_approve/<leave_id>/', HodViews.staff_leave_approve, name="staff_leave_approve"),
    path('staff_leave_reject/<leave_id>/', HodViews.staff_leave_reject, name="staff_leave_reject"),
    path('admin_view_attendance/', HodViews.admin_view_attendance, name="admin_view_attendance"),
    path('admin_get_attendance_dates/', HodViews.admin_get_attendance_dates, name="admin_get_attendance_dates"),
    path('admin_get_attendance_student/', HodViews.admin_get_attendance_student, name="admin_get_attendance_student"),
    path('admin_profile/', HodViews.admin_profile, name="admin_profile"),
    path('admin_profile_update/', HodViews.admin_profile_update, name="admin_profile_update"),
    


    # URLS for Staff
    path('staff_home/', StaffViews.staff_home, name="staff_home"),
    path('staff_take_attendance/', StaffViews.staff_take_attendance, name="staff_take_attendance"),
    path('get_students/', StaffViews.get_students, name="get_students"),
    path('save_attendance_data/', StaffViews.save_attendance_data, name="save_attendance_data"),
    path('staff_update_attendance/', StaffViews.staff_update_attendance, name="staff_update_attendance"),
    path('get_attendance_dates/', StaffViews.get_attendance_dates, name="get_attendance_dates"),
    path('get_attendance_student/', StaffViews.get_attendance_student, name="get_attendance_student"),
    path('update_attendance_data/', StaffViews.update_attendance_data, name="update_attendance_data"),
    path('staff_apply_leave/', StaffViews.staff_apply_leave, name="staff_apply_leave"),
    path('staff_apply_leave_save/', StaffViews.staff_apply_leave_save, name="staff_apply_leave_save"),
    path('staff_feedback/', StaffViews.staff_feedback, name="staff_feedback"),
    path('staff_feedback_save/', StaffViews.staff_feedback_save, name="staff_feedback_save"),
    path('staff_profile/', StaffViews.staff_profile, name="staff_profile"),
    path('staff_profile_update/', StaffViews.staff_profile_update, name="staff_profile_update"),

    path('staff_add_result/', StaffViews.staff_add_result, name="staff_add_result"),
    path('staff_add_result_save/', StaffViews.staff_add_result_save, name="staff_add_result_save"),
    path('get_loads_by_academic_year/', StaffViews.get_loads_by_academic_year, name='get_loads_by_academic_year'),

    path('staff_view_schedule/', StaffViews.staff_view_schedule, name="staff_view_schedule"),
    

    # URSL for Student
    path('student_home/', StudentViews.student_home, name="student_home"),
    path('student_view_attendance/', StudentViews.student_view_attendance, name="student_view_attendance"),
    path('student_view_attendance_post/', StudentViews.student_view_attendance_post, name="student_view_attendance_post"),
    path('student_apply_leave/', StudentViews.student_apply_leave, name="student_apply_leave"),
    path('student_apply_leave_save/', StudentViews.student_apply_leave_save, name="student_apply_leave_save"),
    path('student_feedback/', StudentViews.student_feedback, name="student_feedback"),
    path('student_feedback_save/', StudentViews.student_feedback_save, name="student_feedback_save"),
    path('student_profile/', StudentViews.student_profile, name="student_profile"),
    path('student_profile_update/', StudentViews.student_profile_update, name="student_profile_update"),
    path('student_view_result/', StudentViews.student_view_result, name="student_view_result"),
    path('student_view_schedule/', StudentViews.student_view_schedule, name="student_view_schedule"),
    path('student_view_account/', StudentViews.student_view_account, name="student_view_account"), 

    # enrollment urls
    path('add_enrollment/', HodViews.add_enrollment, name="add_enrollment"),
    path('add_enrollment_save/', HodViews.add_enrollment_save, name="add_enrollment_save"),

    # Password reset    
    path('password_reset/', auth_views.PasswordResetView.as_view(), name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

]
