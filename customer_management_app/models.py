from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class SessionYearModel(models.Model):
    id = models.AutoField(primary_key=True)
    session_start_year = models.DateField()
    session_end_year = models.DateField()
    objects = models.Manager()


# Overriding the Default Django Auth
# User and adding One More Field (user_type)
class CustomUser(AbstractUser):
    HOD = '1'
    STAFF = '2'
    CUSTOMER = '3'

    EMAIL_TO_USER_TYPE_MAP = {
        'hod': HOD,
        'staff': STAFF,
        'customer': CUSTOMER
    }

    user_type_data = ((HOD, "HOD"), (STAFF, "Staff"), (CUSTOMER, "Customer"))
    user_type = models.CharField(
        default=1, choices=user_type_data, max_length=10)


class AdminHOD(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Staffs(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Courses(models.Model):
    id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Subjects(models.Model):
    id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=255)

    # need to give default course
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE, default=1)
    staff_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


BEE_LEVEL_DATA = (('Level_1', "Level 1"), ('Level_2', "Level 2"), ('Level_3', "Level 3"), ('Level_4', "Level 4"),
                  ('Level_5', "Level 5"), ('Level_6', "Level 6"), ('Level_7', "Level 7"), ('Level_8', "Level 8"), ('None', "None"))
CUSTOMER_TYPE_DATA = (('Collector', "Collector"),
                      ('Recycler', "Recycler"), ('Quality', "Quality"))

PROVINCE_DATA = (('Gauteng', "Gauteng"), ('Mpumalanga', "Mpumalanga"), ('KZN', "KZN"), ('KZN', "KZN"), ('KZN', "KZN"), ('North_West', "North West"),
                 ('Limpopo', "Limpopo"), ('Western_Cape', "Western Cape"), ('Free_State', "Free State"), ('Eastern_Cape', "Eastern Cape"), ('Northern_Cape', "Northern Cape"))


class Customers(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=50)
    profile_pic = models.FileField(null=True)
    address = models.TextField()
    course_id = models.ForeignKey(
        Courses, on_delete=models.DO_NOTHING, default=1)
    session_year_id = models.ForeignKey(SessionYearModel, null=True,
                                        on_delete=models.CASCADE)
    bee_level = models.CharField(
        choices=BEE_LEVEL_DATA, max_length=64, blank=True, null=True)
    province = models.CharField(
        choices=PROVINCE_DATA, max_length=64, null=True, blank=True)
    city = models.CharField(max_length=64, null=True, blank=True)
    contact_person = models.CharField(max_length=255, null=True)
    email = models.EmailField(null=True)
    comment = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


# BETS ADDED: Model Disbursements

DISBURSEMENT_TYPES_DATA = (('Loan', "Loan"), ('Grant', "Grant"))
DISBURSEMENT_ALLOTMENT_DATA = (('First_Allotment', "First Allotment"), (
    'Second_Allotment', "Second Allotment"), ('Third_Allotment', "Third Allotment"))


class Disbursements(models.Model):
    id = models.AutoField(primary_key=True)
    disbursement_code = models.CharField(max_length=255, null=True, blank=True)
    disbursement_description = models.CharField(
        max_length=255, null=True, blank=True)
    disbursement_application_id = models.CharField(
        max_length=255, null=True, blank=True)
    disbursement_reason = models.CharField(
        max_length=255, null=True, blank=True)
    disbursement_type = models.CharField(
        choices=DISBURSEMENT_TYPES_DATA, max_length=10)
    disbursement_date = models.DateField(null=True, blank=True)
    disbursement_amount = models.FloatField(default=0)
    contract_signed_date = models.DateField(null=True, blank=True)
    disbursement_allotment = models.CharField(
        choices=DISBURSEMENT_ALLOTMENT_DATA, max_length=64)
    disbursement_interest_rate = models.FloatField(default=0)
    repayment_term = models.IntegerField(blank=True)
    total_target = models.FloatField(default=0)
    monthly_target = models.FloatField(default=0)
    target_measurement_unit = models.CharField(max_length=64, default='Tone')
    customer_id = models.ForeignKey(
        Customers, on_delete=models.CASCADE, default=1)
    application_contract_document = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Attendance(models.Model):

    # Subject Attendance
    id = models.AutoField(primary_key=True)
    subject_id = models.ForeignKey(Subjects, on_delete=models.DO_NOTHING)
    attendance_date = models.DateField()
    session_year_id = models.ForeignKey(
        SessionYearModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class AttendanceReport(models.Model):
    # Individual Customer Attendance
    id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(Customers, on_delete=models.DO_NOTHING)
    attendance_id = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class LeaveReportCustomer(models.Model):
    id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(Customers, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class LeaveReportStaff(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class FeedBackCustomer(models.Model):
    id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(Customers, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class FeedBackStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class NotificationCustomer(models.Model):
    id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(Customers, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class NotificationStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    stafff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class CustomerResult(models.Model):
    id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(Customers, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(
        Subjects, on_delete=models.CASCADE, default=1)
    subject_exam_marks = models.FloatField(default=0)
    subject_assignment_marks = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


# Creating Django Signals
@receiver(post_save, sender=CustomUser)
# Now Creating a Function which will
# automatically insert data in HOD, Staff or Customer
def create_user_profile(sender, instance, created, **kwargs):
    # if Created is true (Means Data Inserted)
    if created:

        # Check the user_type and insert the data in respective tables
        if instance.user_type == 1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type == 2:
            Staffs.objects.create(admin=instance)
        if instance.user_type == 3:
            Customers.objects.create(admin=instance,
                                     course_id=Courses.objects.get(id=1),
                                     session_year_id=SessionYearModel.objects.get(
                                         id=1),
                                     address="",
                                     profile_pic="",
                                     gender="")


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhod.save()
    if instance.user_type == 2:
        instance.staffs.save()
    if instance.user_type == 3:
        instance.customers.save()
