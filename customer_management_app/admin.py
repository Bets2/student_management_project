from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, AdminHOD, Staffs, Courses, Subjects, Customers, Attendance, AttendanceReport, LeaveReportCustomer, LeaveReportStaff, FeedBackCustomer, FeedBackStaffs, NotificationCustomer, NotificationStaffs, Disbursements, Repayments, GrantManagement

# Register your models here.


class UserModel(UserAdmin):
    pass


admin.site.register(CustomUser, UserModel)

admin.site.register(AdminHOD)
admin.site.register(Staffs)
admin.site.register(Courses)
admin.site.register(Subjects)
admin.site.register(Customers)
admin.site.register(Attendance)
admin.site.register(AttendanceReport)
admin.site.register(LeaveReportCustomer)
admin.site.register(LeaveReportStaff)
admin.site.register(FeedBackCustomer)
admin.site.register(FeedBackStaffs)
admin.site.register(NotificationCustomer)
admin.site.register(NotificationStaffs)

# Bets Added
admin.site.register(Disbursements)
admin.site.register(Repayments)
admin.site.register(GrantManagement)
