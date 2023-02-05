from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from decimal import Decimal
from datetime import datetime
import json
from django.contrib.auth.models import User
from customer_management_app.models import CustomUser


# from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy


from .forms import AddCustomerForm, EditCustomerForm, AddDisbursementForm, EditDisbursementForm, AddRepaymentForm, EditRepaymentForm, AddVolumeForm, EditVolumeForm

from .models import CustomUser, Staffs, Courses, Subjects, Customers, SessionYearModel, FeedBackCustomer, FeedBackStaffs, LeaveReportCustomer, LeaveReportStaff, Attendance, AttendanceReport, Disbursements, Repayments, GrantManagement

# For Customers KPI
all_customer_count = Customers.objects.all().count()
customer_count_active = Customers.objects.filter(
    customer_status='Active').count()
customer_count_collector = Customers.objects.filter(
    customer_type='Collector').count()
customer_count_recycler = Customers.objects.filter(
    customer_type='Recycler').count()

# For Disbursement KPIs

disbursement_all = Disbursements.objects.all()
all_disbursement_count = Disbursements.objects.all().count()
total_disbursement_amount = Disbursements.objects.all().aggregate(
    Sum('disbursement_amount'))['disbursement_amount__sum'] or 0.00
total_disbursement_loan_amount = Disbursements.objects.filter(disbursement_type='Loan').aggregate(
    Sum('disbursement_amount'))['disbursement_amount__sum'] or 0.00
total_disbursement_grant_amount = Disbursements.objects.filter(disbursement_type='Grant').aggregate(
    Sum('disbursement_amount'))['disbursement_amount__sum'] or 0.00

# For Repayment KPIs
all_repayment_count = Repayments.objects.all().count()
all_grant_count = GrantManagement.objects.all().count()
total_repayment_amount = Repayments.objects.all().aggregate(
    Sum('repayment_amount'))['repayment_amount__sum'] or 0.00
total_repayment_loan_amount = Repayments.objects.aggregate(
    Sum('repayment_amount'))['repayment_amount__sum'] or 0.00
total_repayment_grant_amount = GrantManagement.objects.aggregate(
    Sum('amount_amortized'))['amount_amortized__sum'] or 0.00

total_fund_balance = total_repayment_amount - total_disbursement_amount

percentage_fund_balance = (total_repayment_amount /
                           total_disbursement_amount)*100

# For Grant Management KPIs
total_volume_actual = GrantManagement.objects.all().aggregate(
    Sum('total_volume_kg'))['total_volume_kg__sum'] or 0.00
total_amount_amortized = GrantManagement.objects.all().aggregate(
    Sum('amount_amortized'))['amount_amortized__sum'] or 0.00
total_amount_impaired = GrantManagement.objects.all().aggregate(
    Sum('amount_impaired'))['amount_impaired__sum'] or 0.00


@login_required
def admin_home(request):

    # all_customer_count = Customers.objects.all().count()
    # customer_count_active = Customers.objects.filter(
    #     customer_status='Active').count()
    subject_count = Subjects.objects.all().count()
    course_count = Courses.objects.all().count()
    staff_count = Staffs.objects.all().count()
    course_all = Courses.objects.all()
    course_name_list = []
    subject_count_list = []
    customer_count_list_in_course = []

    for course in course_all:
        subjects = Subjects.objects.filter(course_id=course.id).count()
        customers = Customers.objects.filter(course_id=course.id).count()
        course_name_list.append(course.course_name)
        subject_count_list.append(subjects)
        customer_count_list_in_course.append(customers)

    subject_all = Subjects.objects.all()
    subject_list = []
    customer_count_list_in_subject = []
    for subject in subject_all:
        course = Courses.objects.get(id=subject.course_id.id)
        customer_count = Customers.objects.filter(course_id=course.id).count()
        subject_list.append(subject.subject_name)
        customer_count_list_in_subject.append(customer_count)

    # For Saffs
    staff_attendance_present_list = []
    staff_attendance_leave_list = []
    staff_name_list = []

    staffs = Staffs.objects.all()
    for staff in staffs:
        subject_ids = Subjects.objects.filter(staff_id=staff.admin.id)
        attendance = Attendance.objects.filter(
            subject_id__in=subject_ids).count()
        leaves = LeaveReportStaff.objects.filter(staff_id=staff.id,
                                                 leave_status=1).count()
        staff_attendance_present_list.append(attendance)
        staff_attendance_leave_list.append(leaves)
        staff_name_list.append(staff.admin.first_name)

    # For Customers
    customer_attendance_present_list = []
    customer_attendance_leave_list = []
    customer_name_list = []

    customers = Customers.objects.all()
    for customer in customers:
        attendance = AttendanceReport.objects.filter(customer_id=customer.id,
                                                     status=True).count()
        absent = AttendanceReport.objects.filter(customer_id=customer.id,
                                                 status=False).count()
        leaves = LeaveReportCustomer.objects.filter(customer_id=customer.id,
                                                    leave_status=1).count()
        customer_attendance_present_list.append(attendance)
        customer_attendance_leave_list.append(leaves+absent)
        customer_name_list.append(customer.admin.first_name)

    context = {
        "all_customer_count": all_customer_count,
        "customer_count_active": customer_count_active,

        "all_disbursement_count": all_disbursement_count,
        "total_disbursement_amount": total_disbursement_amount,
        "total_disbursement_loan_amount": total_disbursement_loan_amount,
        "total_disbursement_grant_amount": total_disbursement_grant_amount,

        "all_repayment_count": all_repayment_count,
        "all_grant_count": all_grant_count,
        "total_repayment_amount": total_repayment_amount,
        "total_repayment_loan_amount": total_repayment_loan_amount,
        "total_repayment_grant_amount": total_repayment_grant_amount,

        "total_fund_balance": total_fund_balance,

        "subject_count": subject_count,
        "course_count": course_count,
        "staff_count": staff_count,
        "course_name_list": course_name_list,
        "subject_count_list": subject_count_list,
        "customer_count_list_in_course": customer_count_list_in_course,
        "subject_list": subject_list,
        "customer_count_list_in_subject": customer_count_list_in_subject,
        "staff_attendance_present_list": staff_attendance_present_list,
        "staff_attendance_leave_list": staff_attendance_leave_list,
        "staff_name_list": staff_name_list,
        "customer_attendance_present_list": customer_attendance_present_list,
        "customer_attendance_leave_list": customer_attendance_leave_list,
        "customer_name_list": customer_name_list
    }
    return render(request, "hod_template/home_content.html", context)


@login_required
def add_staff(request):
    return render(request, "hod_template/add_staff_template.html")


@login_required
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
        address = request.POST.get('address')

        try:
            user = CustomUser.objects.create_user(username=username,
                                                  password=password,
                                                  email=email,
                                                  first_name=first_name,
                                                  last_name=last_name,
                                                  user_type=2)
            user.staffs.address = address
            user.save()
            messages.success(request, "Staff Added Successfully!")
            return redirect('add_staff')
        except:
            messages.error(request, "Failed to Add Staff!")
            return redirect('add_staff')


@login_required
def manage_staff(request):

    staffs = Staffs.objects.all()
    context = {
        "staffs": staffs
    }
    return render(request, "hod_template/manage_staff_template.html", context)


@login_required
def edit_staff(request, staff_id):
    staff = Staffs.objects.get(admin=staff_id)

    context = {
        "staff": staff,
        "id": staff_id
    }
    return render(request, "hod_template/edit_staff_template.html", context)


@login_required
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


@login_required
def delete_staff(request, staff_id):
    staff = Staffs.objects.get(admin=staff_id)
    try:
        staff.delete()
        messages.success(request, "Staff Deleted Successfully.")
        return redirect('manage_staff')
    except:
        messages.error(request, "Failed to Delete Staff.")
        return redirect('manage_staff')


@login_required
def add_course(request):
    return render(request, "hod_template/add_course_template.html")


@login_required
def add_course_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_course')
    else:
        course = request.POST.get('course')
        try:
            course_model = Courses(course_name=course)
            course_model.save()
            messages.success(request, "Course Added Successfully!")
            return redirect('add_course')
        except:
            messages.error(request, "Failed to Add Course!")
            return redirect('add_course')


@login_required
def manage_course(request):
    courses = Courses.objects.all()
    context = {
        "courses": courses
    }
    return render(request, 'hod_template/manage_course_template.html', context)


@login_required
def edit_course(request, course_id):
    course = Courses.objects.get(id=course_id)
    context = {
        "course": course,
        "id": course_id
    }
    return render(request, 'hod_template/edit_course_template.html', context)


@login_required
def edit_course_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        course_id = request.POST.get('course_id')
        course_name = request.POST.get('course')

        try:
            course = Courses.objects.get(id=course_id)
            course.course_name = course_name
            course.save()

            messages.success(request, "Course Updated Successfully.")
            return redirect('/edit_course/'+course_id)

        except:
            messages.error(request, "Failed to Update Course.")
            return redirect('/edit_course/'+course_id)


@login_required
def delete_course(request, course_id):
    course = Courses.objects.get(id=course_id)
    try:
        course.delete()
        messages.success(request, "Course Deleted Successfully.")
        return redirect('manage_course')
    except:
        messages.error(request, "Failed to Delete Course.")
        return redirect('manage_course')


@login_required
def manage_session(request):
    session_years = SessionYearModel.objects.all()
    context = {
        "session_years": session_years
    }
    return render(request, "hod_template/manage_session_template.html", context)


@login_required
def add_session(request):
    return render(request, "hod_template/add_session_template.html")


@login_required
def add_session_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_course')
    else:
        session_start_year = request.POST.get('session_start_year')
        session_end_year = request.POST.get('session_end_year')

        try:
            sessionyear = SessionYearModel(session_start_year=session_start_year,
                                           session_end_year=session_end_year)
            sessionyear.save()
            messages.success(request, "Session Year added Successfully!")
            return redirect("add_session")
        except:
            messages.error(request, "Failed to Add Session Year")
            return redirect("add_session")


@login_required
def edit_session(request, session_id):
    session_year = SessionYearModel.objects.get(id=session_id)
    context = {
        "session_year": session_year
    }
    return render(request, "hod_template/edit_session_template.html", context)


@login_required
def edit_session_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('manage_session')
    else:
        session_id = request.POST.get('session_id')
        session_start_year = request.POST.get('session_start_year')
        session_end_year = request.POST.get('session_end_year')

        try:
            session_year = SessionYearModel.objects.get(id=session_id)
            session_year.session_start_year = session_start_year
            session_year.session_end_year = session_end_year
            session_year.save()

            messages.success(request, "Session Year Updated Successfully.")
            return redirect('/edit_session/'+session_id)
        except:
            messages.error(request, "Failed to Update Session Year.")
            return redirect('/edit_session/'+session_id)


@login_required
def delete_session(request, session_id):
    session = SessionYearModel.objects.get(id=session_id)
    try:
        session.delete()
        messages.success(request, "Session Deleted Successfully.")
        return redirect('manage_session')
    except:
        messages.error(request, "Failed to Delete Session.")
        return redirect('manage_session')


@login_required
def add_customer(request):
    form = AddCustomerForm()
    context = {
        "form": form
    }
    return render(request, 'hod_template/add_customer_template.html', context)


@login_required
def add_customer_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_customer')
    else:
        # form = AddCustomerForm(request.POST, request.FILES)

        # if form.is_valid():

        customer_name = request.POST.get('customer_name')
        customer_type = request.POST.get('customer_type')
        address = request.POST.get('address')
        city = request.POST.get('city')
        province = request.POST.get('province')
        contact_person = request.POST.get('contact_person')
        customer_status = request.POST.get('customer_status')
        bee_level = request.POST.get('bee_level')
        phone = request.POST.get('phone')
        comment = request.POST.get('comment')

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        session_year_id = request.POST.get('session_year_id')
        course_id = request.POST.get('course_id')
        gender = request.POST.get('gender')

        if len(request.FILES) != 0:
            profile_pic = request.FILES('profile_pic')
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
        else:
            profile_pic_url = None

        customer_name = customer_name
        customer_type = customer_type
        address = address
        city = city
        province = province
        contact_person = contact_person
        customer_status = customer_status
        bee_level = bee_level
        phone = phone
        comment = comment

        first_name = first_name
        last_name = last_name
        username = username
        email = email
        password = password

        session_year_id = session_year_id
        course_id = course_id
        gender = gender

        if profile_pic_url != None:
            profile_pic = profile_pic

       # BETS NOTE: Check if user name is already used

        check_existing_user = CustomUser.objects.filter(
            username=username).exists()
        check_existing_company_name = Customers.objects.filter(
            customer_name=customer_name).exists()

        if check_existing_user:
            messages.error(
                request, 'Username already taken! Try using a different username.')
            return redirect('/add_customer')
        elif check_existing_company_name:
            messages.error(
                request, 'Compay Name already exists! Try using a different Company Name.')
            return redirect('/add_customer')
        else:
            # try:
            user = CustomUser.objects.create_user(username=username,
                                                  password=password,
                                                  email=email,
                                                  first_name=first_name,
                                                  last_name=last_name,
                                                  user_type=3)

            user.customers.customer_name = customer_name
            user.customers.customer_type = customer_type
            user.customers.address = address
            user.customers.city = city
            user.customers.province = province
            user.customers.contact_person = contact_person
            user.customers.customer_status = customer_status
            user.customers.bee_level = bee_level
            user.customers.phone = phone
            user.customers.email = email
            user.customers.comment = comment

            # course_obj = Courses.objects.get(id=course_id)
            # user.customers.course_id = course_obj

            # session_year_obj = SessionYearModel.objects.get(
            #     id=session_year_id)
            # user.customers.session_year_id = session_year_id

            # user.customers.gender = gender
            user.customers.profile_pic = profile_pic_url
            user.save()

            # customer = Customers.objects.create(customer_name=customer_name,
            #                                     customer_type=customer_type,
            #                                     address=address,
            #                                     city=city,
            #                                     province=province,
            #                                     contact_person=contact_person,
            #                                     email=email,
            #                                     customer_status=customer_status,
            #                                     bee_level=bee_level,
            #                                     phone=phone,
            #                                     comment=comment,
            #                                     profile_pic=profile_pic_url)
            # customer.save()

        messages.success(request, customer_name +
                         "Customer Added Successfully!")
        return redirect('manage_customer')
        # except:
        # messages.error(request, "Failed to Add Customer!")
        # return redirect('add_customer')
    # else:
        # return redirect('add_customer')


@login_required
def manage_customer(request):

    customers = Customers.objects.all()

    # for filters
    customer_name_contains = request.GET.get('customer_name_contains')

    if is_valid_queryparam(customer_name_contains) and customer_name_contains != 'Select Customer Name...':
        customers = customers.filter(id__exact=customer_name_contains)

    context = {
        "customers": customers,
        "all_customer_count": all_customer_count,
        "customer_count_active": customer_count_active,
        "customer_count_collector": customer_count_collector,
        "customer_count_recycler": customer_count_recycler,
        "customer_name_contains": customer_name_contains
    }
    return render(request, 'hod_template/manage_customer_template.html', context)


@login_required
def edit_customer(request, customer_id):

    # Adding Customer ID into Session Variable
    request.session['customer_id'] = customer_id

    customer = Customers.objects.get(admin=customer_id)
    form = EditCustomerForm(request.POST or None, request.FILES)
    # form = EditCustomerForm()

    # Filling the form with Data from Database
    form.fields['customer_name'].initial = customer.customer_name
    form.fields['customer_type'].initial = customer.customer_type
    form.fields['address'].initial = customer.address
    form.fields['city'].initial = customer.city
    form.fields['province'].initial = customer.province
    form.fields['contact_person'].initial = customer.contact_person
    form.fields['customer_status'].initial = customer.customer_status
    form.fields['bee_level'].initial = customer.bee_level
    form.fields['phone'].initial = customer.phone
    form.fields['comment'].initial = customer.comment

    form.fields['email'].initial = customer.admin.email
    form.fields['username'].initial = customer.admin.username
    # form.fields['password'].initial = customer.admin.password
    form.fields['first_name'].initial = customer.admin.first_name
    form.fields['last_name'].initial = customer.admin.last_name
    form.fields['address'].initial = customer.address
    form.fields['course_id'].initial = customer.course_id.id
    form.fields['gender'].initial = customer.gender
    form.fields['session_year_id'].initial = customer.session_year_id.id

    context = {
        "customer": customer,
        "id": customer_id,
        "username": customer.admin.username,
        "form": form
    }
    return render(request, "hod_template/edit_customer_template.html", context)


@login_required
def edit_customer_save(request):
    if request.method != "POST":
        return HttpResponse("Invalid Method!")
    else:
        customer_id = request.session.get('customer_id')
        if customer_id == None:
            return redirect('/manage_customer')

        else:
            # form = EditCustomerForm(request.POST, request.FILES)
            customer_name = request.POST.get('customer_name')
            customer_type = request.POST.get('customer_type')
            address = request.POST.get('address')
            city = request.POST.get('city')
            province = request.POST.get('province')
            contact_person = request.POST.get('contact_person')
            customer_status = request.POST.get('customer_status')
            bee_level = request.POST.get('bee_level')
            phone = request.POST.get('phone')
            comment = request.POST.get('comment')

            email = request.POST.get('email')
            username = request.POST.get('username')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            address = request.POST.get('address')
            course_id = request.POST.get('course_id')
            gender = request.POST.get('gender')
            session_year_id = request.POST.get('session_year_id')

            # Getting Profile Pic first
            # First Check whether the file is selected or not
            # Upload only if file is selected

            if len(request.FILES) != 0:
                profile_pic = request.FILES('profile_pic')
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None

            # try:
                # First Update into Custom User Model
                user = CustomUser.objects.get(id=customer_id)
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.username = username
                user.save()

                # Then Update Customers Table
                customer_model = Customers.objects.get(admin=customer_id)

                customer_model.customer_name = customer_name
                customer_model.customer_type = customer_type
                customer_model.address = address
                customer_model.city = city
                customer_model.province = province
                customer_model.contact_person = contact_person
                customer_model.customer_status = customer_status
                customer_model.bee_level = bee_level
                customer_model.phone = phone
                customer_model.email = email
                customer_model.comment = comment

                # course = Courses.objects.get(id=course_id)
                # customer_model.course_id = course

                # session_year_obj = SessionYearModel.objects.get(id=session_year_id)
                # customer_model.session_year_id = session_year_obj

                # customer_model.gender = gender
                if profile_pic_url != None:
                    customer_model.profile_pic = profile_pic_url
                customer_model.save()
                # Delete customer_id SESSION after the data is updated
                del request.session['customer_id']

                messages.success(request, "Customer Updated Successfully!")
                return redirect('/edit_customer/'+customer_id)
            # except:
                messages.error(
                    request, "Failed to update Customer. Please contact administrator")
                return redirect('/edit_customer/'+customer_id)

            messages.Success(request, "Customer Updated successfully!")
            return redirect('/edit_customer/'+customer_id)


@login_required
def customer_profile(request, customer_id):
    customer = Customers.objects.get(id=customer_id)
    disbursement = Disbursements.objects.filter(
        customer_id=customer_id)
    repayment = Repayments.objects.filter(customer_id=customer_id)
    grant = GrantManagement.objects.filter(customer_id=customer_id)

    customer_total_disbursement_amount = Disbursements.objects.filter(
        customer_id=customer_id).aggregate(Sum('disbursement_amount'))['disbursement_amount__sum'] or 0.00

    query_set_loan = Disbursements.objects.filter(
        customer_id=customer_id, disbursement_type="Loan")
    customer_total_loans = query_set_loan.aggregate(
        Sum('disbursement_amount'))['disbursement_amount__sum'] or 0.00

    query_set_grant = Disbursements.objects.filter(
        customer_id=customer_id, disbursement_type="Grant")
    customer_total_grant = query_set_grant.aggregate(
        Sum('disbursement_amount'))['disbursement_amount__sum'] or 0.00

    total_loan_repayments = Repayments.objects.filter(customer_id=customer_id).aggregate(
        Sum('repayment_amount'))['repayment_amount__sum'] or 0.00

    if customer_total_disbursement_amount > 0:
        percentage_loan_paid = (total_loan_repayments /
                                customer_total_disbursement_amount)*100
    else:
        percentage_loan_paid = 0.00

    total_grant_amortized = GrantManagement.objects.filter(
        customer_id=customer_id).aggregate(Sum('amount_amortized'))['amount_amortized__sum'] or 0.00

    total_grant_impaired = GrantManagement.objects.filter(
        customer_id=customer_id).aggregate(Sum('amount_impaired'))['amount_impaired__sum'] or 0.00

    context = {
        "disbursements": disbursement,
        "id": customer_id,
        "customer": customer,
        "repayments": repayment,
        "grants": grant,

        "customer_total_disbursement_amount": customer_total_disbursement_amount,
        "customer_total_loans": customer_total_loans,
        "customer_total_grant": customer_total_grant,
        "total_loan_repayments": total_loan_repayments,
        "percentage_loan_paid": percentage_loan_paid,
        "total_grant_amortized": total_grant_amortized,
        "total_grant_impaired": total_grant_impaired
        # "form": form
    }
    return render(request, "hod_template/customer_profile_template.html", context)


@login_required
def delete_customer(request, customer_id):
    customer = Customers.objects.get(admin=customer_id)
    try:
        customer.delete()
        messages.success(request, "Customer Deleted Successfully.")
        return redirect('manage_customer')
    except:
        messages.error(request, "Failed to Delete Customer.")
        return redirect('manage_customer')


# BETS ADDED Disbursment related views here ***************************************************
@login_required
def manage_disbursement(request):
    disbursements = Disbursements.objects.all()
    customer = Customers.objects.all()
    # for filters
    customer_name_contains = request.GET.get('customer_name_contains')

    if is_valid_queryparam(customer_name_contains) and customer_name_contains != 'Select Customer Name...':
        disbursements = disbursements.filter(
            customer_id__exact=customer_name_contains)

    context = {
        "disbursements": disbursements,
        "all_disbursement_count": all_disbursement_count,
        "total_disbursement_amount": total_disbursement_amount,
        "total_disbursement_loan_amount": total_disbursement_loan_amount,
        "total_disbursement_grant_amount": total_disbursement_grant_amount,

        "customers": customer,
        "customer_name_contains": customer_name_contains
    }
    return render(request, 'hod_template/manage_disbursement_template.html', context)


@login_required
def add_disbursement(request):
    customer = Customers.objects.all()
    form = AddDisbursementForm()
    context = {
        "customer": customer,
        "form": form
    }
    return render(request, 'hod_template/add_disbursement_template.html', context)


@login_required
def add_disbursement_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_disbursement')

    else:

        disbursement_code = request.POST.get('disbursement_code')
        disbursement_description = request.POST.get(
            'disbursement_description')
        disbursement_application_id = request.POST.get(
            'disbursement_application_id')
        disbursement_reason = request.POST.get('disbursement_reason')
        disbursement_type = request.POST.get('disbursement_type')
        disbursement_date = request.POST.get('disbursement_date') or None
        disbursement_amount = request.POST.get('disbursement_amount')
        contract_signed_date = request.POST.get(
            'contract_signed_date') or None
        disbursement_monthly_repayment_amount = request.POST.get(
            'disbursement_monthly_repayment_amount')
        disbursement_end = request.POST.get('disbursement_end') or None
        disbursement_allotment = request.POST.get('disbursement_allotment')
        disbursement_interest_rate = request.POST.get(
            'disbursement_interest_rate')
        repayment_term = request.POST.get('repayment_term')
        total_target = request.POST.get('total_target')
        monthly_target = request.POST.get('monthly_target')
        contract_target = request.POST.get('contract_target')
        contract_monthly_target = request.POST.get('contract_monthly_target')
        target_measurement_unit = request.POST.get(
            'target_measurement_unit')
        # application_contract_document = request.FILES['application_contract_document']
        # customer = request.POST.get('customer')
        customer_id = request.POST.get('customer_id')
        if len(request.FILES) != 0:
            application_contract_document = request.FILES(
                'application_contract_document')
            fs = FileSystemStorage()
            filename = fs.save(
                application_contract_document.name, application_contract_document)
            application_contract_document_url = fs.url(filename)
        else:
            application_contract_document_url = None

            # disbursement = Disbursements.objects.get(id)

        disbursement_code = disbursement_code
        disbursement_description = disbursement_description
        disbursement_application_id = disbursement_application_id
        disbursement_reason = disbursement_reason
        disbursement_type = disbursement_type
        disbursement_date = disbursement_date
        disbursement_amount = disbursement_amount
        disbursement_monthly_repayment_amount = disbursement_monthly_repayment_amount
        contract_signed_date = contract_signed_date
        disbursement_end = disbursement_end
        disbursement_allotment = disbursement_allotment
        disbursement_interest_rate = disbursement_interest_rate
        repayment_term = repayment_term
        total_target = total_target
        monthly_target = monthly_target
        contract_target = contract_target
        contract_monthly_target = contract_monthly_target
        target_measurement_unit = target_measurement_unit
        if application_contract_document_url != None:
            application_contract_document = application_contract_document
        # customer_id = customer_id
        customer_id = Customers.objects.get(
            id=customer_id)

        # Check if Disbursement Code is already used before
        check_existing_disbursement_code = Disbursements.objects.filter(
            disbursement_code=disbursement_code).exists()

        if check_existing_disbursement_code:
            messages.error(
                request, 'Disbursement Code you provided has already been used before! Try Create a new Disbursement Code.')
            return redirect('/add_disbursement')
        else:
            # disbursement.application_contract_document = application_contract_document
            disbursement = Disbursements.objects.create(disbursement_code=disbursement_code,
                                                        disbursement_description=disbursement_description,
                                                        disbursement_application_id=disbursement_application_id,
                                                        disbursement_reason=disbursement_reason,
                                                        disbursement_type=disbursement_type,
                                                        disbursement_date=disbursement_date,
                                                        disbursement_amount=disbursement_amount,
                                                        disbursement_monthly_repayment_amount=disbursement_monthly_repayment_amount,
                                                        contract_signed_date=contract_signed_date,
                                                        disbursement_end=disbursement_end,
                                                        disbursement_allotment=disbursement_allotment,
                                                        disbursement_interest_rate=disbursement_interest_rate,
                                                        repayment_term=repayment_term,
                                                        total_target=total_target,
                                                        monthly_target=monthly_target,
                                                        contract_target=contract_target,
                                                        contract_monthly_target=contract_monthly_target,
                                                        target_measurement_unit=target_measurement_unit,
                                                        application_contract_document=application_contract_document_url,
                                                        customer_id=customer_id)

            # Save Disbursements table
            disbursement.save()
            messages.success(request, disbursement_code +
                             "Disbursement details added Successfully.")
            return redirect("/manage_disbursement")


@login_required
def detail_disbursement(request, disbursement_id):

    disbursement = Disbursements.objects.get(id=disbursement_id)
    # repayment = Repayments.objects.get(id=disbursement_id)
    customer = Customers.objects.get(id=disbursement.customer_id.id)

    context = {
        "disbursements": disbursement,
        "id": disbursement_id,
        "customer": customer
        # "form": form
    }
    return render(request, "hod_template/detail_disbursement_template.html", context)


@login_required
def edit_disbursement(request, disbursement_id):

    disbursement = Disbursements.objects.get(id=disbursement_id)
    customer = Customers.objects.all()

    form = EditDisbursementForm(request.POST or None, request.FILES)

    # Filling the form with Data from Database
    form.fields['disbursement_code'].initial = disbursement.disbursement_code
    form.fields['disbursement_description'].initial = disbursement.disbursement_description
    form.fields['disbursement_application_id'].initial = disbursement.disbursement_application_id
    form.fields['disbursement_reason'].initial = disbursement.disbursement_reason
    form.fields['disbursement_type'].initial = disbursement.disbursement_type
    form.fields['disbursement_date'].initial = disbursement.disbursement_date
    form.fields['disbursement_amount'].initial = disbursement.disbursement_amount
    form.fields['disbursement_monthly_repayment_amount'].initial = disbursement.disbursement_monthly_repayment_amount
    form.fields['contract_signed_date'].initial = disbursement.contract_signed_date
    form.fields['disbursement_end'].initial = disbursement.disbursement_end
    form.fields['disbursement_allotment'].initial = disbursement.disbursement_allotment
    form.fields['disbursement_interest_rate'].initial = disbursement.disbursement_interest_rate
    form.fields['repayment_term'].initial = disbursement.repayment_term
    form.fields['total_target'].initial = disbursement.total_target
    form.fields['monthly_target'].initial = disbursement.monthly_target
    form.fields['contract_target'].initial = disbursement.contract_target
    form.fields['contract_monthly_target'].initial = disbursement.contract_monthly_target
    form.fields['monthly_target'].initial = disbursement.monthly_target

    form.fields['target_measurement_unit'].initial = disbursement.target_measurement_unit
    # To Do: BETS finish this here uploading file
    form.fields['application_contract_document'].initial = disbursement.application_contract_document

    form.fields['customer_id'].initial = disbursement.customer_id

    context = {
        'disbursements': disbursement,
        "id": disbursement_id,
        "customer": customer,
        "form": form

    }
    return render(request, "hod_template/edit_disbursement_template.html", context)


@login_required
def edit_disbursement_save(request):
    if request.method != "POST":
        return HttpResponse("Invalied Method.")
    else:
        disbursement_id = request.POST.get('disbursement_id')
        if disbursement_id == None:
            return redirect('/manage_disbursement')

        else:
            disbursement_code = request.POST.get('disbursement_code')
            disbursement_description = request.POST.get(
                'disbursement_description')
            disbursement_application_id = request.POST.get(
                'disbursement_application_id')
            disbursement_reason = request.POST.get('disbursement_reason')
            disbursement_type = request.POST.get('disbursement_type')
            disbursement_date = request.POST.get('disbursement_date') or None
            disbursement_amount = request.POST.get('disbursement_amount')
            disbursement_monthly_repayment_amount = request.POST.get(
                'disbursement_monthly_repayment_amount')
            contract_signed_date = request.POST.get(
                'contract_signed_date') or None
            disbursement_end = request.POST.get('disbursement_end') or None
            disbursement_allotment = request.POST.get('disbursement_allotment')
            disbursement_interest_rate = request.POST.get(
                'disbursement_interest_rate')
            repayment_term = request.POST.get('repayment_term')
            total_target = request.POST.get('total_target')
            monthly_target = request.POST.get('monthly_target')
            contract_target = request.POST.get('contract_target')
            contract_monthly_target = request.POST.get(
                'contract_monthly_target')
            target_measurement_unit = request.POST.get(
                'target_measurement_unit')
            application_contract_document = request.POST.get(
                'application_contract_document')
            customer_id = request.POST.get('customer_id')
            if len(request.FILES) != 0:
                application_contract_document = request.FILES(
                    'application_contract_document')
                fs = FileSystemStorage()
                filename = fs.save(
                    application_contract_document.name, application_contract_document)
                application_contract_document_url = fs.url(filename)
            else:
                application_contract_document_url = None

            disbursement = Disbursements.objects.get(id=disbursement_id)
            disbursement.disbursement_code = disbursement_code
            disbursement.disbursement_description = disbursement_description
            disbursement.disbursement_application_id = disbursement_application_id
            disbursement.disbursement_reason = disbursement_reason
            disbursement.disbursement_type = disbursement_type
            disbursement.disbursement_date = disbursement_date
            disbursement.disbursement_amount = disbursement_amount
            disbursement.disbursement_monthly_repayment_amount = disbursement_monthly_repayment_amount
            disbursement.contract_signed_date = contract_signed_date
            disbursement.disbursement_end = disbursement_end
            disbursement.disbursement_allotment = disbursement_allotment
            disbursement.disbursement_interest_rate = disbursement_interest_rate
            disbursement.repayment_term = repayment_term
            disbursement.total_target = total_target
            disbursement.monthly_target = monthly_target
            disbursement.contract_target = contract_target
            disbursement.contract_monthly_target = contract_monthly_target

            disbursement.target_measurement_unit = target_measurement_unit
            if application_contract_document_url != None:
                disbursement.application_contract_document = application_contract_document
            # disbursement.application_contract_document = application_contract_document

            # disbursement.customer_id = Customers.objects.get(id=customer_id)

            if disbursement.customer_id == None:
                disbursement.customer_id = customer_id
            else:
                disbursement.customer_id = Customers.objects.get(
                    id=customer_id)

            # Save Disbursements table
            disbursement.save()
            messages.success(
                request, "Disbursement details updated Successfully.")
            return redirect('/detail_disbursement/'+disbursement_id)
            # return redirect("/manage_disbursement/")
            # return redirect("/edit_disbursement/"+disbursement_id)
            # except:
            #     messages.error(
            #         request, "BETS....Failed to Update Disbursement details.")
            #     return redirect('/edit_disbursement/'+disbursement_id)


@login_required
def delete_disbursement(request, disbursement_id):
    disbursement = Disbursements.objects.get(id=disbursement_id)
    try:
        disbursement.delete()
        messages.success(request, "Disbursement Deleted Successfully.")
        return redirect('manage_disbursement')
    except:
        messages.error(request, "Failed to Delete Disbursement.")
        return redirect('manage_disbursement')

# ***************************************************************************************
# GRANT MANAGEMENT


@login_required
def manage_grant(request):
    grants = GrantManagement.objects.all()
    customers = Customers.objects.all()
    # for filters
    customer_name_contains = request.GET.get('customer_name_contains')

    if is_valid_queryparam(customer_name_contains) and customer_name_contains != 'Select Customer Name...':
        grants = grants.filter(customer_id__exact=customer_name_contains)

    context = {
        "grants": grants,
        "total_volume_actual": total_volume_actual,
        "total_amount_amortized": total_amount_amortized,
        "total_amount_impaired": total_amount_impaired,

        "customer_name_contains": customer_name_contains,
        "customers": customers
    }
    return render(request, 'hod_template/manage_grant_template.html', context)


@login_required
def add_volume(request):
    customer = Customers.objects.all()
    disbursement = Disbursements.objects.all()
    form = AddVolumeForm()
    context = {
        "customer": customer,
        "disbursement": disbursement,
        "form": form
    }
    return render(request, 'hod_template/add_volume_template.html', context)


@login_required
def add_volume_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_volume')

    else:

        monthly_volume_report_id = request.POST.get('monthly_volume_report_id')
        volume_report_month = request.POST.get('volume_report_month')
        volume_report_year = request.POST.get('volume_report_year')
        hd_kg = request.POST.get('hd_kg')
        ld_kg = request.POST.get('ld_kg')
        lld_kg = request.POST.get('lld_kg')
        pp_kg = request.POST.get('pp_kg')
        pvc_kg = request.POST.get('pvc_kg')
        ps_kg = request.POST.get('ps_kg')
        pet_kg = request.POST.get('pet_kg')
        other_kg = request.POST.get('other_kg')

        total_volume_kg = Decimal(hd_kg) + Decimal(ld_kg) + Decimal(lld_kg) + Decimal(pp_kg) + Decimal(pvc_kg) + \
            Decimal(ps_kg) + Decimal(pet_kg) + \
            Decimal(other_kg)  # request.POST.get('total_volume_kg')

        volume_report_date = request.POST.get('volume_report_date')

        disbursement_id = request.POST.get('disbursement_id')
        customer_id = request.POST.get('customer_id')

        disbursements = Disbursements.objects.get(id=disbursement_id)

        monthly_target = disbursements.monthly_target
        monthly_repayment_amount = disbursements.disbursement_monthly_repayment_amount

        contract_monthly_target = disbursements.contract_monthly_target

        if contract_monthly_target == 0:
            amount_amortized = 0
            amount_impaired = 0
        else:
            if contract_monthly_target <= Decimal(total_volume_kg):
                amount_amortized = monthly_repayment_amount
                amount_impaired = 0
            else:
                amount_impaired = monthly_repayment_amount - ((Decimal(total_volume_kg)/contract_monthly_target)
                                                              * monthly_repayment_amount)
                amount_amortized = monthly_repayment_amount - amount_impaired

        monthly_volume_report_id = monthly_volume_report_id
        volume_report_month = volume_report_month
        volume_report_year = volume_report_year
        hd_kg = hd_kg
        ld_kg = ld_kg
        lld_kg = lld_kg
        pp_kg = pp_kg
        pvc_kg = pvc_kg
        ps_kg = ps_kg
        pet_kg = pet_kg
        other_kg = other_kg
        total_volume_kg = Decimal(total_volume_kg)
        volume_report_date = volume_report_date
        amount_amortized = amount_amortized
        amount_impaired = amount_impaired

        disbursement_id = Disbursements.objects.get(
            id=disbursement_id)
        customer_id = Customers.objects.get(id=customer_id)

        # Validateions
        check_existing_monthly_volume_id = GrantManagement.objects.filter(
            monthly_volume_report_id=monthly_volume_report_id).exists()

        volume_report_date = datetime.strptime(
            (volume_report_date), "%Y-%m-%d")
        contract_signed_date = disbursement_id.contract_signed_date
        contract_signed_date = datetime.strptime(
            str(contract_signed_date), "%Y-%m-%d")

        disbursement_end_date = disbursement_id.disbursement_end
        disbursement_end_date = datetime.strptime(
            str(disbursement_end_date), "%Y-%m-%d")

        if check_existing_monthly_volume_id:
            messages.error(
                request, 'The monthly volue report Id already exists!. Try Creating a unique Id for this volume report.')
            return redirect('/add_volume')
        elif volume_report_date < contract_signed_date:
            messages.error(
                request, 'Volume Report Date can not be before contract start date. Check the report date again.')
            return redirect('/add_volume')
        elif volume_report_date > disbursement_end_date:
            messages.error(
                request, 'Volume Report Date can not be after the contract end date. Check the report date again.')
            return redirect('/add_volume')

        else:
            grantmanagement = GrantManagement.objects.create(monthly_volume_report_id=monthly_volume_report_id,
                                                             volume_report_month=volume_report_month,
                                                             volume_report_year=volume_report_year,
                                                             hd_kg=hd_kg,
                                                             ld_kg=ld_kg,
                                                             lld_kg=lld_kg,
                                                             pp_kg=pp_kg,
                                                             pvc_kg=pvc_kg,
                                                             ps_kg=ps_kg,
                                                             pet_kg=pet_kg,
                                                             other_kg=other_kg,
                                                             total_volume_kg=total_volume_kg,
                                                             volume_report_date=volume_report_date,
                                                             amount_amortized=amount_amortized,
                                                             amount_impaired=amount_impaired,
                                                             disbursement_id=disbursement_id,
                                                             customer_id=customer_id)

        # Save Repayments table
            grantmanagement.save()
            messages.success(
                request, monthly_volume_report_id + " Monthly Volume details added Successfully.")
            return redirect("/manage_grant")


@login_required
def edit_volume(request, volume_id):
    grant = GrantManagement.objects.get(id=volume_id)
    customer = Customers.objects.all()
    disbursement = Disbursements.objects.all()

    form = EditVolumeForm(request.POST or None, request.FILES)

    # Filling the form with Data from Database

    form.fields['monthly_volume_report_id'].initial = grant.monthly_volume_report_id
    form.fields['volume_report_month'].initial = grant.volume_report_month
    form.fields['volume_report_year'].initial = grant.volume_report_year
    form.fields['hd_kg'].initial = grant.hd_kg
    form.fields['ld_kg'].initial = grant.ld_kg
    form.fields['lld_kg'].initial = grant.lld_kg
    form.fields['pp_kg'].initial = grant.pp_kg
    form.fields['pvc_kg'].initial = grant.pvc_kg
    form.fields['ps_kg'].initial = grant.ps_kg
    form.fields['pet_kg'].initial = grant.pet_kg
    form.fields['other_kg'].initial = grant.other_kg
    # form.fields['total_volume_kg'].initial = grant.total_volume_kg
    form.fields['volume_report_date'].initial = grant.volume_report_date
    # form.fields['amount_amortized'].initial = grant.amount_amortized
    # form.fields['amount_impaired'].initial = grant.amount_impaired
    form.fields['disbursement_id'].initial = grant.disbursement_id
    form.fields['customer_id'].initial = grant.customer_id

    context = {
        'grant': grant,
        "id": volume_id,
        "customer": customer,
        "disbursement": disbursement,
        "form": form
    }
    return render(request, "hod_template/edit_volume_template.html", context)


@login_required
def edit_volume_save(request):
    if request.method != "POST":
        return HttpResponse("Invalied Method.")
    else:
        volume_id = request.POST.get('volume_id')
        if volume_id == None:
            return redirect('/manage_grant')

        else:
            monthly_volume_report_id = request.POST.get(
                'monthly_volume_report_id')
            volume_report_month = request.POST.get('volume_report_month')
            volume_report_year = request.POST.get('volume_report_year')
            hd_kg = request.POST.get('hd_kg')
            ld_kg = request.POST.get('ld_kg')
            lld_kg = request.POST.get('lld_kg')
            pp_kg = request.POST.get('pp_kg')
            pvc_kg = request.POST.get('pvc_kg')
            ps_kg = request.POST.get('ps_kg')
            pet_kg = request.POST.get('pet_kg')
            other_kg = request.POST.get('other_kg')
            total_volume_kg = Decimal(hd_kg) + Decimal(ld_kg) + Decimal(lld_kg) + Decimal(pp_kg) + Decimal(pvc_kg) + \
                Decimal(ps_kg) + Decimal(pet_kg) + \
                Decimal(other_kg)  # request.POST.get('total_volume_kg')
            volume_report_date = request.POST.get('volume_report_date')
            # amount_amortized = request.POST.get('amount_amortized')
            # amount_impaired = request.POST.get('amount_impaired')

            disbursement_id = request.POST.get('disbursement_id')
            customer_id = request.POST.get('customer_id')

            grant = GrantManagement.objects.get(id=volume_id)
            grant.monthly_volume_report_id = monthly_volume_report_id
            grant.volume_report_month = volume_report_month
            grant.volume_report_year = volume_report_year
            grant.hd_kg = hd_kg
            grant.ld_kg = ld_kg
            grant.lld_kg = lld_kg
            grant.pp_kg = pp_kg
            grant.pvc_kg = pvc_kg
            grant.ps_kg = ps_kg
            grant.pet_kg = pet_kg
            grant.other_kg = other_kg
            grant.total_volume_kg = Decimal(total_volume_kg)
            grant.volume_report_date = volume_report_date

            disbursements = Disbursements.objects.get(id=disbursement_id)

            monthly_target = disbursements.monthly_target  # this is base_monthly_target
            monthly_repayment_amount = disbursements.disbursement_monthly_repayment_amount

            contract_monthly_target = disbursements.contract_monthly_target

            if contract_monthly_target == 0:
                grant.amount_amortized = 0
                grant.amount_impaired = 0
            else:
                if contract_monthly_target <= Decimal(total_volume_kg):
                    grant.amount_amortized = monthly_repayment_amount
                    grant.amount_impaired = 0
                else:
                    grant.amount_impaired = monthly_repayment_amount - ((Decimal(total_volume_kg)/contract_monthly_target)
                                                                        * monthly_repayment_amount)
                    grant.amount_amortized = monthly_repayment_amount - grant.amount_impaired
            # grant.amount_amortized = 0  # this will be removed in future temp place holder
            # grant.amount_impaired = 0  # this will be removed in future temp place holder

            if grant.customer_id == None:
                grant.customer_id = customer_id
            else:
                grant.customer_id = Customers.objects.get(id=customer_id)

            if grant.disbursement_id == None:
                grant.disbursement_id = disbursement_id
            else:
                grant.disbursement_id = Disbursements.objects.get(
                    id=disbursement_id)

            # Save GrantManagement table

            volume_report_date = datetime.strptime(
                volume_report_date, "%Y-%m-%d")
            contract_signed_date = disbursements.contract_signed_date
            contract_signed_date = datetime.strptime(
                str(contract_signed_date), "%Y-%m-%d")

            disbursement_end_date = disbursements.disbursement_end
            disbursement_end_date = datetime.strptime(
                str(disbursement_end_date), "%Y-%m-%d")

            if volume_report_date < contract_signed_date:
                messages.error(
                    request, 'Volume Report Date can not be before contract start date. Check the volume capture/report date again.')
                return redirect('/edit_volume/'+volume_id)
            elif volume_report_date > disbursement_end_date:
                messages.error(
                    request, 'Volume Report Date can not be after the contract end date. Check the Volume capture/report date again.')
                return redirect('/edit_volume/'+volume_id)

            else:
                grant.save()
                messages.success(
                    request, "Grant Report - Volume details updated Successfully.")
                return redirect("/detail_volume/"+volume_id)
                # return redirect("/edit_volume/"+volume_id)
                # except:
                #     messages.error(
                #         request, "BETS....Failed to Update Repayment details.")
                #     return redirect('/edit_volume/'+volume_id)


@login_required
def detail_volume(request, volume_id):

    grant = GrantManagement.objects.get(id=volume_id)
    customer = Customers.objects.get(id=grant.customer_id.id)
    disbursement = Disbursements.objects.get(id=grant.disbursement_id.id)

    percentage_actual_volume_to_target = (
        (grant.total_volume_kg/disbursement.contract_monthly_target) * 100)

    percentage_actual_volume_to_target = round(
        percentage_actual_volume_to_target, 2)

    # if disbursement.contract_monthly_target <= grant.total_volume_kg:
    #     amount_amortized_calculated = disbursement.disbursement_monthly_repayment_amount
    #     amount_impaired_calculated = 0
    # else:
    #     amount_amortized_calculated = disbursement.disbursement_monthly_repayment_amount - ((grant.total_volume_kg/disbursement.monthly_target)
    #                                                                                         * disbursement.disbursement_monthly_repayment_amount)
    #     amount_impaired_calculated = (
    #         disbursement.disbursement_monthly_repayment_amount - amount_amortized_calculated)

    context = {
        'grant': grant,
        "id": volume_id,
        "customer": customer,
        "disbursement": disbursement,
        # "amount_amortized_calculated": amount_amortized_calculated,
        # "amount_impaired_calculated": amount_impaired_calculated,
        "percentage_actual_volume_to_target": percentage_actual_volume_to_target
        # "form": form
    }
    return render(request, "hod_template/detail_volume_template.html", context)


@login_required
def delete_grant(request, volume_id):
    grant = GrantManagement.objects.get(id=volume_id)
    try:
        grant.delete()
        messages.success(
            request, "ID: " + volume_id + " Grant Volume detail Deleted Successfully.")
        return redirect('manage_grant')
    except:
        messages.error(request, "Failed to Delete Grant volume detail.")
        return redirect('manage_grant')


# ***************************************************************************************
# OVERVIEWS


def is_valid_queryparam(param):
    return param != '' and param is not None


@login_required
def overview(request):

    customers = Customers.objects.all()
    repayments = Repayments.objects.all()
    disbursements = Disbursements.objects.all()
    grants = GrantManagement.objects.all()

    # for filters
    customer_name_contains = request.GET.get('customer_name_contains')
    disbursement_code_contains = request.GET.get('disbursement_code_contains')

    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    province_list_contains = request.GET.get('province_list_contains')
    loans_tick = request.GET.get('loans_tick')
    grants_tick = request.GET.get('grants_tick')

    if is_valid_queryparam(customer_name_contains) and customer_name_contains != 'Select Customer Name...':
        disbursements = disbursements.filter(
            customer_id__exact=customer_name_contains)
        repayments = repayments.filter(
            customer_id__exact=customer_name_contains)
        grants = grants.filter(customer_id__exact=customer_name_contains)

    # elif is_valid_queryparam(province_list_contains):
    #     disbursements = disbursements.filter(id=province_list_contains)

    context = {
        "repayments": repayments,
        "all_repayment_count": all_repayment_count,
        "all_grant_count": all_grant_count,
        "total_repayment_amount": total_repayment_amount,
        "total_repayment_loan_amount": total_repayment_loan_amount,
        "total_repayment_grant_amount": total_repayment_grant_amount,
        "total_fund_balance": total_fund_balance,
        "percentage_fund_balance": percentage_fund_balance,

        "disbursements": disbursements,
        "all_disbursement_count": all_disbursement_count,
        "total_disbursement_amount": total_disbursement_amount,
        "total_disbursement_loan_amount": total_disbursement_loan_amount,
        "total_disbursement_grant_amount": total_disbursement_grant_amount,

        "customers": customers,
        "all_customer_count": all_customer_count,
        "customer_count_active": customer_count_active,
        "customer_count_collector": customer_count_collector,
        "customer_count_recycler": customer_count_recycler,

        "grants": grants,
        "customer_name_contains": customer_name_contains

    }
    return render(request, 'hod_template/overview_template.html', context)

# ***************************************************************************************
# REPAYMENTS


@login_required
def manage_repayment(request):
    repayments = Repayments.objects.all()
    customers = Customers.objects.all()

    customer_name_contains = request.GET.get('customer_name_contains')

    if is_valid_queryparam(customer_name_contains) and customer_name_contains != 'Select Customer Name...':
        repayments = repayments.filter(
            customer_id__exact=customer_name_contains)
    total_disbursement_loan_amount = Disbursements.objects.filter(disbursement_type='Loan').aggregate(
        Sum('disbursement_amount'))['disbursement_amount__sum'] or 0.00

    context = {
        "repayments": repayments,
        "total_repayment_amount": total_repayment_amount,
        "total_repayment_loan_amount": total_repayment_loan_amount,
        "total_repayment_grant_amount": total_repayment_grant_amount,
        "total_fund_balance": total_fund_balance,
        "percentage_fund_balance": percentage_fund_balance,
        "total_disbursement_loan_amount": total_disbursement_loan_amount,

        "customer_name_contains": customer_name_contains,
        "customers": customers
    }
    return render(request, 'hod_template/manage_repayment_template.html', context)


@login_required
def add_repayment(request):
    customer = Customers.objects.all()
    disbursement = Disbursements.objects.all()
    form = AddRepaymentForm()
    context = {
        "customer": customer,
        "disbursement": disbursement,
        "form": form
    }
    return render(request, 'hod_template/add_repayment_template.html', context)


@login_required
def add_repayment_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_repayment')

    else:

        repayment_code = request.POST.get('repayment_code')
        # repayment_type = request.POST.get('repayment_type')
        repayment_description = request.POST.get('repayment_description')
        repayment_amount = request.POST.get('repayment_amount')
        repayment_date = request.POST.get('repayment_date')

        hd_kg = request.POST.get('hd_kg')
        ld_kg = request.POST.get('ld_kg')
        lld_kg = request.POST.get('lld_kg')
        pp_kg = request.POST.get('pp_kg')
        pvc_kg = request.POST.get('pvc_kg')
        ps_kg = request.POST.get('ps_kg')
        pet_kg = request.POST.get('pet_kg')
        other_kg = request.POST.get('other_kg')

        actual_volume_tone = request.POST.get('actual_volume_tone')

        comment = request.POST.get('comment')
        # payment_documentation = request.POST.get('payment_documentation')
        disbursement_id = request.POST.get('disbursement_id')
        customer_id = request.POST.get('customer_id')
        if len(request.FILES) != 0:
            payment_documentation = request.FILES(
                'payment_documentation')
            fs = FileSystemStorage()
            filename = fs.save(payment_documentation.name,
                               payment_documentation)
            payment_documentation_url = fs.url(filename)
        else:
            payment_documentation_url = None

        repayment_code = repayment_code
        # repayment_type = repayment_type
        repayment_description = repayment_description
        repayment_amount = repayment_amount
        repayment_date = repayment_date

        hd_kg = hd_kg
        ld_kg = ld_kg
        lld_kg = lld_kg
        pp_kg = pp_kg
        pvc_kg = pvc_kg
        ps_kg = ps_kg
        pet_kg = pet_kg
        other_kg = other_kg

        actual_volume_tone = Decimal(actual_volume_tone)
        comment = comment
        if payment_documentation_url != None:
            payment_documentation = payment_documentation
        # payment_documentation  = payment_documentation
        # disbursement_id        = disbursement_id
        disbursement_id = Disbursements.objects.get(id=disbursement_id)
        customer_id = Customers.objects.get(id=customer_id)

        # Validateions
        check_existing_repayment_code = Repayments.objects.filter(
            repayment_code=repayment_code).exists()

        repayment_date = datetime.strptime(
            (repayment_date), "%Y-%m-%d")
        contract_signed_date = disbursement_id.contract_signed_date
        contract_signed_date = datetime.strptime(
            str(contract_signed_date), "%Y-%m-%d")

        disbursement_end_date = disbursement_id.disbursement_end
        disbursement_end_date = datetime.strptime(
            str(disbursement_end_date), "%Y-%m-%d")

        if check_existing_repayment_code:
            messages.error(
                request, 'The repayment code you provided already exists!. Try Creating a unique code to capture this repayment.')
            return redirect('/add_repayment')
        elif repayment_date < contract_signed_date:
            messages.error(
                request, 'The Repayment Date can not be before contract start date. Check the repayment date again.')
            return redirect('/add_repayment')
        elif repayment_date > disbursement_end_date:
            messages.error(
                request, 'The Repayment Date can not be after the contract end date. Check the repayment date again.')
            return redirect('/add_repayment')

        else:
            repayment = Repayments.objects.create(repayment_code=repayment_code,
                                                  #   repayment_type=repayment_type,
                                                  repayment_description=repayment_description,
                                                  repayment_amount=repayment_amount,
                                                  repayment_date=repayment_date,
                                                  hd_kg=hd_kg,
                                                  ld_kg=ld_kg,
                                                  lld_kg=lld_kg,
                                                  pp_kg=pp_kg,
                                                  pvc_kg=pvc_kg,
                                                  ps_kg=ps_kg,
                                                  pet_kg=pet_kg,
                                                  other_kg=other_kg,

                                                  actual_volume_tone=actual_volume_tone,
                                                  comment=comment,
                                                  payment_documentation=payment_documentation_url,
                                                  disbursement_id=disbursement_id,
                                                  customer_id=customer_id)

        # Save Repayments table
            repayment.save()
            messages.success(
                request, repayment_code + "Repayment details added Successfully.")
            return redirect("/manage_repayment")


@login_required
def detail_repayment(request, repayment_id):

    repayment = Repayments.objects.get(id=repayment_id)
    customer = Customers.objects.get(id=repayment.customer_id.id)
    disbursement = Disbursements.objects.get(id=repayment.disbursement_id.id)

    percentage_actual_volume_to_target = (
        (repayment.actual_volume_tone/disbursement.contract_monthly_target) * 100)

    context = {
        'repayments': repayment,
        "id": repayment_id,
        "customer": customer,
        "disbursement": disbursement,
        "percentage_actual_volume_to_target": percentage_actual_volume_to_target
        # "form": form
    }
    return render(request, "hod_template/detail_repayment_template.html", context)


@login_required
def edit_repayment(request, repayment_id):

    repayment = Repayments.objects.get(id=repayment_id)
    customer = Customers.objects.all()
    disbursement = Disbursements.objects.all()

    form = EditRepaymentForm(request.POST or None, request.FILES)

    # Filling the form with Data from Database

    form.fields['repayment_code'].initial = repayment.repayment_code
    # form.fields['repayment_type'].initial = repayment.repayment_type
    form.fields['repayment_description'].initial = repayment.repayment_description
    form.fields['repayment_amount'].initial = repayment.repayment_amount
    form.fields['repayment_date'].initial = repayment.repayment_date

    form.fields['hd_kg'].initial = repayment.hd_kg
    form.fields['ld_kg'].initial = repayment.ld_kg
    form.fields['lld_kg'].initial = repayment.lld_kg
    form.fields['pp_kg'].initial = repayment.pp_kg
    form.fields['pvc_kg'].initial = repayment.pvc_kg
    form.fields['ps_kg'].initial = repayment.ps_kg
    form.fields['pet_kg'].initial = repayment.pet_kg
    form.fields['other_kg'].initial = repayment.other_kg

    form.fields['actual_volume_tone'].initial = repayment.actual_volume_tone
    form.fields['comment'].initial = repayment.comment
    form.fields['payment_documentation'].initial = repayment.payment_documentation
    form.fields['disbursement_id'].initial = repayment.disbursement_id
    form.fields['customer_id'].initial = repayment.customer_id

    context = {
        'repayments': repayment,
        "id": repayment_id,
        "customer": customer,
        "disbursement": disbursement,
        "form": form
    }
    return render(request, "hod_template/edit_repayment_template.html", context)


@login_required
def edit_repayment_save(request):
    if request.method != "POST":
        return HttpResponse("Invalied Method.")
    else:
        repayment_id = request.POST.get('repayment_id')
        if repayment_id == None:
            return redirect('/manage_repayment')

        else:
            repayment_code = request.POST.get('repayment_code')
            # repayment_type = request.POST.get('repayment_type')
            repayment_description = request.POST.get('repayment_description')
            repayment_amount = request.POST.get('repayment_amount')
            repayment_date = request.POST.get('repayment_date') or None

            hd_kg = request.POST.get('hd_kg')
            ld_kg = request.POST.get('ld_kg')
            lld_kg = request.POST.get('lld_kg')
            pp_kg = request.POST.get('pp_kg')
            pvc_kg = request.POST.get('pvc_kg')
            ps_kg = request.POST.get('ps_kg')
            pet_kg = request.POST.get('pet_kg')
            other_kg = request.POST.get('other_kg')

            actual_volume_tone = Decimal(hd_kg) + Decimal(ld_kg) + Decimal(lld_kg) + Decimal(pp_kg) + Decimal(pvc_kg) + \
                Decimal(ps_kg) + Decimal(pet_kg) + \
                Decimal(other_kg)
            # actual_volume_tone = request.POST.get('actual_volume_tone')

            comment = request.POST.get('comment')
            payment_documentation = request.POST.get('payment_documentation')
            disbursement_id = request.POST.get('disbursement_id')
            customer_id = request.POST.get('customer_id')

            if len(request.FILES) != 0:
                payment_documentation = request.FILES(
                    'payment_documentation')
                fs = FileSystemStorage()
                filename = fs.save(
                    payment_documentation.name, payment_documentation)
                payment_documentation_url = fs.url(filename)
            else:
                payment_documentation_url = None

            # try:
            repayment = Repayments.objects.get(id=repayment_id)
            repayment.repayment_code = repayment_code
            # repayment.repayment_type = repayment_type
            repayment.repayment_description = repayment_description
            repayment.repayment_amount = repayment_amount
            repayment.repayment_date = repayment_date
            repayment.hd_kg = hd_kg
            repayment.ld_kg = ld_kg
            repayment.lld_kg = lld_kg
            repayment.pp_kg = pp_kg
            repayment.pvc_kg = pvc_kg
            repayment.ps_kg = ps_kg
            repayment.pet_kg = pet_kg
            repayment.other_kg = other_kg

            repayment.actual_volume_tone = Decimal(actual_volume_tone)
            repayment.comment = comment
            repayment.payment_documentation = payment_documentation

            if payment_documentation_url != None:
                repayment.payment_documentation = payment_documentation

            if repayment.customer_id == None:
                repayment.customer_id = customer_id
            else:
                repayment.customer_id = Customers.objects.get(
                    id=customer_id)

            if repayment.disbursement_id == None:
                repayment.disbursement_id = disbursement_id
            else:
                repayment.disbursement_id = Disbursements.objects.get(
                    id=disbursement_id)

            # Validateions
            repayment_date = datetime.strptime(
                (repayment_date), "%Y-%m-%d")
            contract_signed_date = repayment.disbursement_id.contract_signed_date
            contract_signed_date = datetime.strptime(
                str(contract_signed_date), "%Y-%m-%d")

            disbursement_end_date = repayment.disbursement_id.disbursement_end
            disbursement_end_date = datetime.strptime(
                str(disbursement_end_date), "%Y-%m-%d")

            if repayment_date < contract_signed_date:
                messages.error(
                    request, 'The Repayment Date can not be before contract start date. Check the repayment date again.')
                return redirect('/edit_repayment/'+repayment_id)
            elif repayment_date > disbursement_end_date:
                messages.error(
                    request, 'The Repayment Date can not be after the contract end date. Check the repayment date again.')
                return redirect('/edit_repayment/'+repayment_id)

            else:
                # Save Repayment table
                repayment.save()
                messages.success(
                    request, "Repayment details updated Successfully.")
                return redirect("/detail_repayment/"+repayment_id)
                # return redirect("/edit_repayment/"+repayment_id)
                # except:
                #     messages.error(
                #         request, "BETS....Failed to Update Repayment details.")
                #     return redirect('/edit_repayment/'+repayment_id)


@login_required
def delete_repayment(request, repayment_id):
    repayment = Repayments.objects.get(id=repayment_id)
    try:
        repayment.delete()
        messages.success(request, "Repayment detail Deleted Successfully.")
        return redirect('manage_repayment')
    except:
        messages.error(request, "Failed to Delete Repayment.")
        return redirect('manage_repayment')

# ***************************************************************************************
# Subject


@login_required
def add_subject(request):
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type='2')
    context = {
        "courses": courses,
        "staffs": staffs
    }
    return render(request, 'hod_template/add_subject_template.html', context)


@login_required
def add_subject_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_subject')
    else:
        subject_name = request.POST.get('subject')

        course_id = request.POST.get('course')
        course = Courses.objects.get(id=course_id)

        staff_id = request.POST.get('staff')
        staff = CustomUser.objects.get(id=staff_id)

        try:
            subject = Subjects(subject_name=subject_name,
                               course_id=course,
                               staff_id=staff)
            subject.save()
            messages.success(request, "Subject Added Successfully!")
            return redirect('add_subject')
        except:
            messages.error(request, "Failed to Add Subject!")
            return redirect('add_subject')


@login_required
def manage_subject(request):
    subjects = Subjects.objects.all()
    context = {
        "subjects": subjects
    }
    return render(request, 'hod_template/manage_subject_template.html', context)


@login_required
def edit_subject(request, subject_id):
    subject = Subjects.objects.get(id=subject_id)
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type='2')
    context = {
        "subject": subject,
        "courses": courses,
        "staffs": staffs,
        "id": subject_id
    }
    return render(request, 'hod_template/edit_subject_template.html', context)


@login_required
def edit_subject_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        subject_id = request.POST.get('subject_id')
        subject_name = request.POST.get('subject')
        course_id = request.POST.get('course')
        staff_id = request.POST.get('staff')

        try:
            subject = Subjects.objects.get(id=subject_id)
            subject.subject_name = subject_name

            course = Courses.objects.get(id=course_id)
            subject.course_id = course

            staff = CustomUser.objects.get(id=staff_id)
            subject.staff_id = staff

            subject.save()

            messages.success(request, "Subject Updated Successfully.")

            return HttpResponseRedirect(reverse("edit_subject",
                                                kwargs={"subject_id": subject_id}))

        except:
            messages.error(request, "Failed to Update Subject.")
            return HttpResponseRedirect(reverse("edit_subject",
                                                kwargs={"subject_id": subject_id}))


@login_required
def delete_subject(request, subject_id):
    subject = Subjects.objects.get(id=subject_id)
    try:
        subject.delete()
        messages.success(request, "Subject Deleted Successfully.")
        return redirect('manage_subject')
    except:
        messages.error(request, "Failed to Delete Subject.")
        return redirect('manage_subject')


@login_required
@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@login_required
@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@login_required
def customer_feedback_message(request):
    feedbacks = FeedBackCustomer.objects.all()
    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'hod_template/customer_feedback_template.html', context)


@login_required
@csrf_exempt
def customer_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBackCustomer.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")


@login_required
def staff_feedback_message(request):
    feedbacks = FeedBackStaffs.objects.all()
    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'hod_template/staff_feedback_template.html', context)


@login_required
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


@login_required
def customer_leave_view(request):
    leaves = LeaveReportCustomer.objects.all()
    context = {
        "leaves": leaves
    }
    return render(request, 'hod_template/customer_leave_view.html', context)


@login_required
def customer_leave_approve(request, leave_id):
    leave = LeaveReportCustomer.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect('customer_leave_view')


@login_required
def customer_leave_reject(request, leave_id):
    leave = LeaveReportCustomer.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('customer_leave_view')


@login_required
def staff_leave_view(request):
    leaves = LeaveReportStaff.objects.all()
    context = {
        "leaves": leaves
    }
    return render(request, 'hod_template/staff_leave_view.html', context)


@login_required
def staff_leave_approve(request, leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect('staff_leave_view')


@login_required
def staff_leave_reject(request, leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('staff_leave_view')


@login_required
def admin_view_attendance(request):
    subjects = Subjects.objects.all()
    session_years = SessionYearModel.objects.all()
    context = {
        "subjects": subjects,
        "session_years": session_years
    }
    return render(request, "hod_template/admin_view_attendance.html", context)


@login_required
@csrf_exempt
def admin_get_attendance_dates(request):

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
                        content_type="application/json",
                        safe=False)


@login_required
@csrf_exempt
def admin_get_attendance_customer(request):

    # Getting Values from Ajax POST 'Fetch Customer'
    attendance_date = request.POST.get('attendance_date')
    attendance = Attendance.objects.get(id=attendance_date)

    attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)
    # Only Passing Customer Id and Customer Name Only
    list_data = []

    for customer in attendance_data:
        data_small = {"id": customer.customer_id.admin.id,
                      "name": customer.customer_id.admin.first_name+" "+customer.customer_id.admin.last_name,
                      "status": customer.status}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@login_required
def admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)

    context = {
        "user": user
    }
    return render(request, 'hod_template/admin_profile.html', context)


@login_required
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


@login_required
def staff_profile(request):
    pass
