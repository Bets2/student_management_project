from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json


from .models import CustomUser, Staffs, Courses, Subjects, Customers, SessionYearModel, Attendance, AttendanceReport, LeaveReportStaff, FeedBackStaffs, CustomerResult


def staff_home(request):

    # Fetching All Customers under Staff
    print(request.user.id)
    subjects = Subjects.objects.filter(staff_id=request.user.id)
    print(subjects)
    course_id_list = []
    for subject in subjects:
        course = Courses.objects.get(id=subject.course_id.id)
        course_id_list.append(course.id)

    final_course = []
    # Removing Duplicate Course Id
    for course_id in course_id_list:
        if course_id not in final_course:
            final_course.append(course_id)

    print(final_course)
    customers_count = Customers.objects.filter(
        course_id__in=final_course).count()
    subject_count = subjects.count()
    print(subject_count)
    print(customers_count)

    # Fetch All Attendance Count
    attendance_count = Attendance.objects.filter(
        subject_id__in=subjects).count()

    # Fetch All Approve Leave
    # print(request.user)
    print(request.user.user_type)
    staff = Staffs.objects.get(admin=request.user.id)
    leave_count = LeaveReportStaff.objects.filter(staff_id=staff.id,
                                                  leave_status=1).count()

    # Fetch Attendance Data by Subjects
    subject_list = []
    attendance_list = []
    for subject in subjects:
        attendance_count1 = Attendance.objects.filter(
            subject_id=subject.id).count()
        subject_list.append(subject.subject_name)
        attendance_list.append(attendance_count1)

    customers_attendance = Customers.objects.filter(course_id__in=final_course)
    customer_list = []
    customer_list_attendance_present = []
    customer_list_attendance_absent = []
    for customer in customers_attendance:
        attendance_present_count = AttendanceReport.objects.filter(status=True,
                                                                   customer_id=customer.id).count()
        attendance_absent_count = AttendanceReport.objects.filter(status=False,
                                                                  customer_id=customer.id).count()
        customer_list.append(customer.admin.first_name +
                             " " + customer.admin.last_name)
        customer_list_attendance_present.append(attendance_present_count)
        customer_list_attendance_absent.append(attendance_absent_count)

    context = {
        "customers_count": customers_count,
        "attendance_count": attendance_count,
        "leave_count": leave_count,
        "subject_count": subject_count,
        "subject_list": subject_list,
        "attendance_list": attendance_list,
        "customer_list": customer_list,
        "attendance_present_list": customer_list_attendance_present,
        "attendance_absent_list": customer_list_attendance_absent
    }
    return render(request, "staff_template/staff_home_template.html", context)


def staff_take_attendance(request):
    subjects = Subjects.objects.filter(staff_id=request.user.id)
    session_years = SessionYearModel.objects.all()
    context = {
        "subjects": subjects,
        "session_years": session_years
    }
    return render(request, "staff_template/take_attendance_template.html", context)


def staff_apply_leave(request):
    print(request.user.id)
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
            leave_report = LeaveReportStaff(staff_id=staff_obj,
                                            leave_date=leave_date,
                                            leave_message=leave_message,
                                            leave_status=0)
            leave_report.save()
            messages.success(request, "Applied for Leave.")
            return redirect('staff_apply_leave')
        except:
            messages.error(request, "Failed to Apply Leave")
            return redirect('staff_apply_leave')


def staff_feedback(request):
    return render(request, "staff_template/staff_feedback_template.html")


def staff_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('staff_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        staff_obj = Staffs.objects.get(admin=request.user.id)

        try:
            add_feedback = FeedBackStaffs(staff_id=staff_obj,
                                          feedback=feedback,
                                          feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('staff_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('staff_feedback')


@csrf_exempt
def get_customers(request):

    subject_id = request.POST.get("subject")
    session_year = request.POST.get("session_year")

    # Customers enroll to Course, Course has Subjects
    # Getting all data from subject model based on subject_id
    subject_model = Subjects.objects.get(id=subject_id)

    session_model = SessionYearModel.objects.get(id=session_year)

    customers = Customers.objects.filter(course_id=subject_model.course_id,
                                         session_year_id=session_model)

    # Only Passing Customer Id and Customer Name Only
    list_data = []

    for customer in customers:
        data_small = {"id": customer.admin.id,
                      "name": customer.admin.first_name+" "+customer.admin.last_name}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def save_attendance_data(request):

    # Get Values from Staf Take Attendance form via AJAX (JavaScript)
    # Use getlist to access HTML Array/List Input Data
    customer_ids = request.POST.get("customer_ids")
    subject_id = request.POST.get("subject_id")
    attendance_date = request.POST.get("attendance_date")
    session_year_id = request.POST.get("session_year_id")

    subject_model = Subjects.objects.get(id=subject_id)
    session_year_model = SessionYearModel.objects.get(id=session_year_id)

    json_customer = json.loads(customer_ids)

    try:
        # First Attendance Data is Saved on Attendance Model
        attendance = Attendance(subject_id=subject_model,
                                attendance_date=attendance_date,
                                session_year_id=session_year_model)
        attendance.save()

        for cust in json_customer:
            # Attendance of Individual Customer saved on AttendanceReport Model
            customer = Customers.objects.get(admin=cust['id'])
            attendance_report = AttendanceReport(customer_id=customer,
                                                 attendance_id=attendance,
                                                 status=cust['status'])
            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("Error")


def staff_update_attendance(request):
    subjects = Subjects.objects.filter(staff_id=request.user.id)
    session_years = SessionYearModel.objects.all()
    context = {
        "subjects": subjects,
        "session_years": session_years
    }
    return render(request, "staff_template/update_attendance_template.html", context)


@csrf_exempt
def get_attendance_dates(request):

    # Getting Values from Ajax POST 'Fetch Customer'
    subject_id = request.POST.get("subject")
    session_year = request.POST.get("session_year_id")

    # Customers enroll to Course, Course has Subjects
    # Getting all data from subject model based on subject_id
    subject_model = Subjects.objects.get(id=subject_id)

    session_model = SessionYearModel.objects.get(id=session_year)
    attendance = Attendance.objects.filter(subject_id=subject_model,
                                           session_year_id=session_model)

    # Only Passing Customer Id and Customer Name Only
    list_data = []

    for attendance_single in attendance:
        data_small = {"id": attendance_single.id,
                      "attendance_date": str(attendance_single.attendance_date),
                      "session_year_id": attendance_single.session_year_id.id}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data),
                        content_type="application/json", safe=False)


@csrf_exempt
def get_attendance_customer(request):

    # Getting Values from Ajax POST 'Fetch Customer'
    attendance_date = request.POST.get('attendance_date')
    attendance = Attendance.objects.get(id=attendance_date)

    attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)
    # Only Passing Customer Id and Customer Name Only
    list_data = []

    for customer in attendance_data:
        data_small = {"id": customer.customer_id.admin.id,
                      "name": customer.customer_id.admin.first_name+" "+customer.customer_id.admin.last_name, "status": customer.status}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data),
                        content_type="application/json",
                        safe=False)


@csrf_exempt
def update_attendance_data(request):
    customer_ids = request.POST.get("customer_ids")

    attendance_date = request.POST.get("attendance_date")
    attendance = Attendance.objects.get(id=attendance_date)

    json_customer = json.loads(customer_ids)

    try:

        for cust in json_customer:

            # Attendance of Individual Customer saved on AttendanceReport Model
            customer = Customers.objects.get(admin=cust['id'])

            attendance_report = AttendanceReport.objects.get(customer_id=customer,
                                                             attendance_id=attendance)
            attendance_report.status = cust['status']

            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("Error")


def staff_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    staff = Staffs.objects.get(admin=user)

    context = {
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
    subjects = Subjects.objects.filter(staff_id=request.user.id)
    session_years = SessionYearModel.objects.all()
    context = {
        "subjects": subjects,
        "session_years": session_years,
    }
    return render(request, "staff_template/add_result_template.html", context)


def staff_add_result_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('staff_add_result')
    else:
        customer_admin_id = request.POST.get('customer_list')
        assignment_marks = request.POST.get('assignment_marks')
        exam_marks = request.POST.get('exam_marks')
        subject_id = request.POST.get('subject')

        customer_obj = Customers.objects.get(admin=customer_admin_id)
        subject_obj = Subjects.objects.get(id=subject_id)

        try:
            # Check if Customers Result Already Exists or not
            check_exist = CustomerResult.objects.filter(subject_id=subject_obj,
                                                        customer_id=customer_obj).exists()
            if check_exist:
                result = CustomerResult.objects.get(subject_id=subject_obj,
                                                    customer_id=customer_obj)
                result.subject_assignment_marks = assignment_marks
                result.subject_exam_marks = exam_marks
                result.save()
                messages.success(request, "Result Updated Successfully!")
                return redirect('staff_add_result')
            else:
                result = CustomerResult(customer_id=customer_obj,
                                        subject_id=subject_obj,
                                        subject_exam_marks=exam_marks,
                                        subject_assignment_marks=assignment_marks)
                result.save()
                messages.success(request, "Result Added Successfully!")
                return redirect('staff_add_result')
        except:
            messages.error(request, "Failed to Add Result!")
            return redirect('staff_add_result')
