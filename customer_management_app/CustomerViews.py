from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
import datetime
from .models import CustomUser, Staffs, Courses, Subjects, Customers, Attendance, AttendanceReport, LeaveReportCustomer, FeedBackCustomer, CustomerResult


def customer_home(request):
    customer_obj = Customers.objects.get(admin=request.user.id)
    total_attendance = AttendanceReport.objects.filter(
        customer_id=customer_obj).count()
    attendance_present = AttendanceReport.objects.filter(customer_id=customer_obj,
                                                         status=True).count()
    attendance_absent = AttendanceReport.objects.filter(customer_id=customer_obj,
                                                        status=False).count()
    course_obj = Courses.objects.get(id=customer_obj.course_id.id)
    total_subjects = Subjects.objects.filter(course_id=course_obj).count()
    subject_name = []
    data_present = []
    data_absent = []
    subject_data = Subjects.objects.filter(course_id=customer_obj.course_id)
    for subject in subject_data:
        attendance = Attendance.objects.filter(subject_id=subject.id)
        attendance_present_count = AttendanceReport.objects.filter(attendance_id__in=attendance,
                                                                   status=True,
                                                                   customer_id=customer_obj.id).count()
        attendance_absent_count = AttendanceReport.objects.filter(attendance_id__in=attendance,
                                                                  status=False,
                                                                  customer_id=customer_obj.id).count()
        subject_name.append(subject.subject_name)
        data_present.append(attendance_present_count)
        data_absent.append(attendance_absent_count)

        context = {
            "total_attendance": total_attendance,
            "attendance_present": attendance_present,
            "attendance_absent": attendance_absent,
            "total_subjects": total_subjects,
            "subject_name": subject_name,
            "data_present": data_present,
            "data_absent": data_absent
        }
        return render(request, "customer_template/customer_home_template.html")


def customer_view_attendance(request):

    # Getting Logged in Customer Data
    customer = Customers.objects.get(admin=request.user.id)

    # Getting Course Enrolled of LoggedIn Customer
    course = customer.course_id

    # Getting the Subjects of Course Enrolled
    subjects = Subjects.objects.filter(course_id=course)
    context = {
        "subjects": subjects
    }
    return render(request, "customer_template/customer_view_attendance.html", context)


def customer_view_attendance_post(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('customer_view_attendance')
    else:
        # Getting all the Input Data
        subject_id = request.POST.get('subject')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Parsing the date data into Python object
        start_date_parse = datetime.datetime.strptime(
            start_date, '%Y-%m-%d').date()
        end_date_parse = datetime.datetime.strptime(
            end_date, '%Y-%m-%d').date()

        # Getting all the Subject Data based on Selected Subject
        subject_obj = Subjects.objects.get(id=subject_id)

        # Getting Logged In User Data
        user_obj = CustomUser.objects.get(id=request.user.id)

        # Getting Customer Data Based on Logged in Data
        cust_obj = Customers.objects.get(admin=user_obj)

        # Now Accessing Attendance Data based on the Range of Date
        # Selected and Subject Selected
        attendance = Attendance.objects.filter(attendance_date__range=(start_date_parse,
                                                                       end_date_parse),
                                               subject_id=subject_obj)
        # Getting Attendance Report based on the attendance
        # details obtained above
        attendance_reports = AttendanceReport.objects.filter(attendance_id__in=attendance,
                                                             customer_id=cust_obj)

        context = {
            "subject_obj": subject_obj,
            "attendance_reports": attendance_reports
        }

        return render(request, 'customer_template/customer_attendance_data.html', context)


def customer_apply_leave(request):
    customer_obj = Customers.objects.get(admin=request.user.id)
    leave_data = LeaveReportCustomer.objects.filter(customer_id=customer_obj)
    context = {
        "leave_data": leave_data
    }
    return render(request, 'customer_template/customer_apply_leave.html', context)


def customer_apply_leave_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('customer_apply_leave')
    else:
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')

        customer_obj = Customers.objects.get(admin=request.user.id)
        try:
            leave_report = LeaveReportCustomer(customer_id=customer_obj,
                                               leave_date=leave_date,
                                               leave_message=leave_message,
                                               leave_status=0)
            leave_report.save()
            messages.success(request, "Applied for Leave.")
            return redirect('customer_apply_leave')
        except:
            messages.error(request, "Failed to Apply Leave")
            return redirect('customer_apply_leave')


def customer_feedback(request):
    customer_obj = Customers.objects.get(admin=request.user.id)
    feedback_data = FeedBackCustomer.objects.filter(customer_id=customer_obj)
    context = {
        "feedback_data": feedback_data
    }
    return render(request, 'customer_template/customer_feedback.html', context)


def customer_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('customer_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        customer_obj = Customers.objects.get(admin=request.user.id)

        try:
            add_feedback = FeedBackCustomer(customer_id=customer_obj,
                                            feedback=feedback,
                                            feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('customer_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('customer_feedback')


def customer_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    customer = Customers.objects.get(admin=user)

    context = {
        "user": user,
        "customer": customer
    }
    return render(request, 'customer_template/customer_profile.html', context)


def customer_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('customer_profile')
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

            customer = Customers.objects.get(admin=customuser.id)
            customer.address = address
            customer.save()

            messages.success(request, "Profile Updated Successfully")
            return redirect('customer_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('customer_profile')


def customer_view_result(request):
    customer = Customers.objects.get(admin=request.user.id)
    customer_result = CustomerResult.objects.filter(customer_id=customer.id)
    context = {
        "customer_result": customer_result,
    }
    return render(request, "customer_template/customer_view_result.html", context)
