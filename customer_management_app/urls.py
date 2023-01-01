from django.contrib import admin
from django.urls import path, include
from . import CustomerViews, views
from .import HodViews, StaffViews


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('contact', views.contact, name="contact"),
    path('login/', views.loginUser, name="login"),
    path('logout_user', views.logout_user, name="logout_user"),
    path('registration', views.registration, name="registration"),
    path('doLogin', views.doLogin, name="doLogin"),
    path('doRegistration', views.doRegistration, name="doRegistration"),

    # URLS for Customer
    path('customer_home/', CustomerViews.customer_home, name="customer_home"),
    path('customer_view_attendance/', CustomerViews.customer_view_attendance,
         name="customer_view_attendance"),
    path('customer_view_attendance_post/', CustomerViews.customer_view_attendance_post,
         name="customer_view_attendance_post"),
    path('customer_apply_leave/', CustomerViews.customer_apply_leave,
         name="customer_apply_leave"),
    path('customer_apply_leave_save/', CustomerViews.customer_apply_leave_save,
         name="customer_apply_leave_save"),
    path('customer_feedback/', CustomerViews.customer_feedback,
         name="customer_feedback"),
    path('customer_feedback_save/', CustomerViews.customer_feedback_save,
         name="customer_feedback_save"),
    path('customer_profile/', CustomerViews.customer_profile,
         name="customer_profile"),
    path('customer_profile_update/', CustomerViews.customer_profile_update,
         name="customer_profile_update"),
    path('customer_view_result/', CustomerViews.customer_view_result,
         name="customer_view_result"),


    # URLS for Staff
    path('staff_home/', StaffViews.staff_home, name="staff_home"),
    path('staff_take_attendance/', StaffViews.staff_take_attendance,
         name="staff_take_attendance"),
    path('get_customers/', StaffViews.get_customers, name="get_customers"),
    path('save_attendance_data/', StaffViews.save_attendance_data,
         name="save_attendance_data"),
    path('staff_update_attendance/', StaffViews.staff_update_attendance,
         name="staff_update_attendance"),
    path('get_attendance_dates/', StaffViews.get_attendance_dates,
         name="get_attendance_dates"),
    path('get_attendance_customer/', StaffViews.get_attendance_customer,
         name="get_attendance_customer"),
    path('update_attendance_data/', StaffViews.update_attendance_data,
         name="update_attendance_data"),
    path('staff_apply_leave/', StaffViews.staff_apply_leave,
         name="staff_apply_leave"),
    path('staff_apply_leave_save/', StaffViews.staff_apply_leave_save,
         name="staff_apply_leave_save"),
    path('staff_feedback/', StaffViews.staff_feedback, name="staff_feedback"),
    path('staff_feedback_save/', StaffViews.staff_feedback_save,
         name="staff_feedback_save"),
    path('staff_profile/', StaffViews.staff_profile, name="staff_profile"),
    path('staff_profile_update/', StaffViews.staff_profile_update,
         name="staff_profile_update"),
    path('staff_add_result/', StaffViews.staff_add_result,
         name="staff_add_result"),
    path('staff_add_result_save/', StaffViews.staff_add_result_save,
         name="staff_add_result_save"),

    # URL for Admin
    path('admin_home/', HodViews.admin_home, name="admin_home"),
    path('add_staff/', HodViews.add_staff, name="add_staff"),
    path('add_staff_save/', HodViews.add_staff_save, name="add_staff_save"),
    path('manage_staff/', HodViews.manage_staff, name="manage_staff"),
    path('edit_staff/<staff_id>/', HodViews.edit_staff, name="edit_staff"),
    path('edit_staff_save/', HodViews.edit_staff_save, name="edit_staff_save"),
    path('delete_staff/<staff_id>/',
         HodViews.delete_staff, name="delete_staff"),
    path('add_course/', HodViews.add_course, name="add_course"),
    path('add_course_save/', HodViews.add_course_save, name="add_course_save"),
    path('manage_course/', HodViews.manage_course, name="manage_course"),
    path('edit_course/<course_id>/',
         HodViews.edit_course, name="edit_course"),
    path('edit_course_save/', HodViews.edit_course_save,
         name="edit_course_save"),
    path('delete_course/<course_id>/',
         HodViews.delete_course, name="delete_course"),
    path('manage_session/', HodViews.manage_session, name="manage_session"),
    path('add_session/', HodViews.add_session, name="add_session"),
    path('add_session_save/', HodViews.add_session_save,
         name="add_session_save"),
    path('edit_session/<session_id>',
         HodViews.edit_session, name="edit_session"),
    path('edit_session_save/', HodViews.edit_session_save,
         name="edit_session_save"),
    path('delete_session/<session_id>/',
         HodViews.delete_session, name="delete_session"),
    path('add_customer/', HodViews.add_customer, name="add_customer"),
    path('add_customer_save/', HodViews.add_customer_save,
         name="add_customer_save"),
    path('edit_customer/<customer_id>',
         HodViews.edit_customer, name="edit_customer"),
    path('edit_customer_save/', HodViews.edit_customer_save,
         name="edit_customer_save"),
    path('manage_customer/', HodViews.manage_customer, name="manage_customer"),
    path('delete_customer/<customer_id>/',
         HodViews.delete_customer, name="delete_customer"),

    # URLS for Disbursements
    path('add_disbursement/', HodViews.add_disbursement, name="add_disbursement"),
    path('add_disbursement_save/', HodViews.add_disbursement_save,
         name="add_disbursement_save"),
    path('edit_disbursement/<disbursement_id>',
         HodViews.edit_disbursement, name="edit_disbursement"),
    path('detail_disbursement/<disbursement_id>',
         HodViews.detail_disbursement, name="detail_disbursement"),
    path('edit_disbursement_save/', HodViews.edit_disbursement_save,
         name="edit_disbursement_save"),
    path('manage_disbursement/', HodViews.manage_disbursement,
         name="manage_disbursement"),
    path('delete_disbursement/<disbursement_id>/',
         HodViews.delete_disbursement, name="delete_disbursement"),

    # URLS for Repayments
    path('add_repayment/', HodViews.add_repayment, name="add_repayment"),
    path('add_repayment_save/', HodViews.add_repayment_save,
         name="add_repayment_save"),
    path('edit_repayment/<repayment_id>',
         HodViews.edit_repayment, name="edit_repayment"),
    path('detail_repayment/<repayment_id>',
         HodViews.detail_repayment, name="detail_repayment"),
    path('edit_repayment_save/', HodViews.edit_repayment_save,
         name="edit_repayment_save"),
    path('manage_repayment/', HodViews.manage_repayment,
         name="manage_repayment"),
    path('delete_repayment/<repayment_id>/',
         HodViews.delete_repayment, name="delete_repayment"),


    # URLS for Grantmanagement
    #     path('add_volume/', HodViews.add_volume, name="add_volume"),





    # URLs for Overview
    path('overview/', HodViews.overview,
         name="overview"),


    path('add_subject/', HodViews.add_subject, name="add_subject"),
    path('add_subject_save/', HodViews.add_subject_save,
         name="add_subject_save"),
    path('manage_subject/', HodViews.manage_subject, name="manage_subject"),
    path('edit_subject/<subject_id>/',
         HodViews.edit_subject, name="edit_subject"),
    path('edit_subject_save/', HodViews.edit_subject_save,
         name="edit_subject_save"),
    path('delete_subject/<subject_id>/',
         HodViews.delete_subject, name="delete_subject"),
    path('check_email_exist/', HodViews.check_email_exist,
         name="check_email_exist"),
    path('check_username_exist/', HodViews.check_username_exist,
         name="check_username_exist"),
    path('customer_feedback_message/', HodViews.customer_feedback_message,
         name="customer_feedback_message"),
    path('customer_feedback_message_reply/', HodViews.customer_feedback_message_reply,
         name="customer_feedback_message_reply"),
    path('staff_feedback_message/', HodViews.staff_feedback_message,
         name="staff_feedback_message"),
    path('staff_feedback_message_reply/', HodViews.staff_feedback_message_reply,
         name="staff_feedback_message_reply"),
    path('customer_leave_view/', HodViews.customer_leave_view,
         name="customer_leave_view"),
    path('customer_leave_approve/<leave_id>/',
         HodViews.customer_leave_approve, name="customer_leave_approve"),
    path('customer_leave_reject/<leave_id>/',
         HodViews.customer_leave_reject, name="customer_leave_reject"),
    path('staff_leave_view/', HodViews.staff_leave_view,
         name="staff_leave_view"),
    path('staff_leave_approve/<leave_id>/',
         HodViews.staff_leave_approve, name="staff_leave_approve"),
    path('staff_leave_reject/<leave_id>/',
         HodViews.staff_leave_reject, name="staff_leave_reject"),
    path('admin_view_attendance/', HodViews.admin_view_attendance,
         name="admin_view_attendance"),
    path('admin_get_attendance_dates/', HodViews.admin_get_attendance_dates,
         name="admin_get_attendance_dates"),
    path('admin_get_attendance_customer/', HodViews.admin_get_attendance_customer,
         name="admin_get_attendance_customer"),
    path('admin_profile/', HodViews.admin_profile, name="admin_profile"),
    path('admin_profile_update/', HodViews.admin_profile_update,
         name="admin_profile_update"),

]
