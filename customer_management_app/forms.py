from django import forms
from .models import Courses, SessionYearModel, Customers


class DateInput(forms.DateInput):
    input_type = "date"


class AddCustomerForm(forms.Form):
    customer_name = forms.CharField(label="Customer Name",
                                    max_length=255,
                                    required=True,
                                    widget=forms.TextInput(attrs={"class": "form-control"}))

    customer_type_list = (
        ('Collector', 'Collector'),
        ('Quality', 'Quality'),
        ('Recycler', 'Recycler')
    )

    customer_type = forms.ChoiceField(label="Customer Type",
                                      choices=customer_type_list,
                                      widget=forms.Select(attrs={"class": "form-control"}))

    address = forms.CharField(label="Address",
                              max_length=255,
                              widget=forms.TextInput(attrs={"class": "form-control"}))
    city = forms.CharField(label="City",
                           max_length=255,
                           widget=forms.TextInput(attrs={"class": "form-control"}))

    PROVINCE_LIST = (('Gauteng', "Gauteng"), ('Mpumalanga', "Mpumalanga"), ('KZN', "KZN"),  ('North_West', "North West"),
                     ('Limpopo', "Limpopo"), ('Western_Cape', "Western Cape"), ('Free_State', "Free State"), ('Eastern_Cape', "Eastern Cape"), ('Northern_Cape', "Northern Cape"))

    province = forms.ChoiceField(label="Province",
                                 choices=PROVINCE_LIST,
                                 widget=forms.Select(attrs={"class": "form-control"}))
    contact_person = forms.CharField(label="Contact Person",
                                     max_length=255,
                                     widget=forms.TextInput(attrs={"class": "form-control"}))

    CUSTOMER_STATUS_LIST = (('Active', "Active"), ('Cancelled', "Cancelled"), ('Contract_Complete',
                                                                               "Contract Complete"), ('Business_Closed', "Business Closed"), ('Other', "Other"))

    customer_status = forms.ChoiceField(label="Customer Ctatus",
                                        choices=CUSTOMER_STATUS_LIST,
                                        widget=forms.Select(attrs={"class": "form-control"}))

    email = forms.EmailField(label="Email",
                             max_length=50,
                             widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="Password",
                               max_length=50,
                               widget=forms.PasswordInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label="First Name",
                                 max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last Name",
                                max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(label="Username",
                               max_length=50,
                               widget=forms.TextInput(attrs={"class": "form-control"}))
    # For Displaying Courses
    try:
        courses = Courses.objects.all()
        course_list = []
        for course in courses:
            single_course = (course.id, course.course_name)
            course_list.append(single_course)
    except:
        print("here")
        course_list = []

    # For Displaying Session Years
    try:
        session_years = SessionYearModel.objects.all()
        session_year_list = []
        for session_year in session_years:
            single_session_year = (session_year.id, str(
                session_year.session_start_year)+" to "+str(session_year.session_end_year))
            session_year_list.append(single_session_year)

    except:
        session_year_list = []

    gender_list = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )

    course_id = forms.ChoiceField(label="Course",
                                  choices=course_list,
                                  widget=forms.Select(attrs={"class": "form-control"}))
    gender = forms.ChoiceField(label="Gender",
                               choices=gender_list,
                               widget=forms.Select(attrs={"class": "form-control"}))
    session_year_id = forms.ChoiceField(label="Session Year",
                                        choices=session_year_list,
                                        widget=forms.Select(attrs={"class": "form-control"}))
    profile_pic = forms.FileField(label="Customer Contracts/Profile Pic",
                                  required=False,
                                  widget=forms.FileInput(attrs={"class": "form-control"}))

    comment = forms.CharField(label="Comment (if any):",
                              max_length=255,
                              widget=forms.TextInput(attrs={"class": "form-control"}))


class EditCustomerForm(forms.Form):
    customer_name = forms.CharField(label="Customer Name",
                                    max_length=255,
                                    required=True,
                                    widget=forms.TextInput(attrs={"class": "form-control"}))

    customer_type_list = (
        ('Collector', 'Collector'),
        ('Quality', 'Quality'),
        ('Recycler', 'Recycler')
    )

    customer_type = forms.ChoiceField(label="Customer Type",
                                      choices=customer_type_list,
                                      widget=forms.Select(attrs={"class": "form-control"}))

    address = forms.CharField(label="Address",
                              max_length=255,
                              widget=forms.TextInput(attrs={"class": "form-control"}))

    city = forms.CharField(label="City",
                           max_length=255,
                           widget=forms.TextInput(attrs={"class": "form-control"}))

    PROVINCE_LIST = (('Gauteng', "Gauteng"), ('Mpumalanga', "Mpumalanga"), ('KZN', "KZN"),  ('North_West', "North West"),
                     ('Limpopo', "Limpopo"), ('Western_Cape', "Western Cape"), ('Free_State', "Free State"), ('Eastern_Cape', "Eastern Cape"), ('Northern_Cape', "Northern Cape"))

    province = forms.ChoiceField(label="Province",
                                 choices=PROVINCE_LIST,
                                 widget=forms.Select(attrs={"class": "form-control"}))
    contact_person = forms.CharField(label="Contact Person",
                                     max_length=255,
                                     widget=forms.TextInput(attrs={"class": "form-control"}))

    CUSTOMER_STATUS_LIST = (('Active', "Active"), ('Cancelled', "Cancelled"), ('Contract_Complete',
                                                                               "Contract Complete"), ('Business_Closed', "Business Closed"), ('Other', "Other"))

    customer_status = forms.ChoiceField(label="Customer Ctatus",
                                        choices=CUSTOMER_STATUS_LIST,
                                        widget=forms.Select(attrs={"class": "form-control"}))

    email = forms.EmailField(label="Email",
                             max_length=50,
                             widget=forms.EmailInput(attrs={"class": "form-control"}))
    # password = forms.CharField(label="Password",
    #                            max_length=50,

    #                            widget=forms.PasswordInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label="First Name",
                                 max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last Name",
                                max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(label="Username",
                               max_length=50,
                               widget=forms.TextInput(attrs={"class": "form-control"}))
    # For Displaying Courses
    try:
        courses = Courses.objects.all()
        course_list = []
        for course in courses:
            single_course = (course.id, course.course_name)
            course_list.append(single_course)
    except:
        print("here")
        course_list = []

    # For Displaying Session Years
    try:
        session_years = SessionYearModel.objects.all()
        session_year_list = []
        for session_year in session_years:
            single_session_year = (session_year.id, str(
                session_year.session_start_year)+" to "+str(session_year.session_end_year))
            session_year_list.append(single_session_year)

    except:
        session_year_list = []

    gender_list = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )

    course_id = forms.ChoiceField(label="Course",
                                  choices=course_list,
                                  widget=forms.Select(attrs={"class": "form-control"}))
    gender = forms.ChoiceField(label="Gender",
                               choices=gender_list,
                               widget=forms.Select(attrs={"class": "form-control"}))
    session_year_id = forms.ChoiceField(label="Session Year",
                                        choices=session_year_list,
                                        widget=forms.Select(attrs={"class": "form-control"}))
    profile_pic = forms.FileField(label="Customer Contracts/Profile Pic",
                                  required=False,
                                  widget=forms.FileInput(attrs={"class": "form-control"}))

    comment = forms.CharField(label="Comment (if any):",
                              max_length=255,
                              required=False,
                              widget=forms.TextInput(attrs={"class": "form-control"}))


class AddDisbursementForm(forms.Form):

    disbursement_code = forms.CharField(label="disbursement_code",
                                        max_length=128,
                                        widget=forms.TextInput(attrs={"class": "form-control"}))
    disbursement_description = forms.CharField(label="disbursement_description",
                                               required=False,
                                               max_length=255,
                                               widget=forms.TextInput(attrs={"class": "form-control"}))
    disbursement_application_id = forms.CharField(label="disbursement_application_id",
                                                  required=False,
                                                  max_length=128,
                                                  widget=forms.TextInput(attrs={"class": "form-control"}))
    disbursement_reason = forms.CharField(label="disbursement_reason",
                                          required=False,
                                          max_length=255,
                                          widget=forms.TextInput(attrs={"class": "form-control"}))

    disbursement_type_list = (('Loan', 'Loan'), ('Grant', 'Grant'))
    disbursement_type = forms.ChoiceField(label="Disbursement Type",
                                          choices=disbursement_type_list,
                                          widget=forms.Select(attrs={"class": "form-control"}))
    disbursement_date = forms.DateField(label="disbursement_date",
                                        widget=forms.SelectDateWidget(attrs={"class": "form-control"}))
    disbursement_amount = forms.DecimalField(label="disbursement_amount",
                                             max_digits=10,
                                             decimal_places=2,
                                             widget=forms.NumberInput(attrs={'id': 'form-control', 'step': "0.01"}))
    contract_signed_date = forms.DateField(label="contract_signed_date",
                                           widget=forms.SelectDateWidget(attrs={"class": "form-control"}))
    disbursement_end = forms.DateField(label="disbursement_end",
                                       widget=forms.SelectDateWidget(attrs={"class": "form-control"}))
    disbursement_allotment = forms.CharField(label="disbursement_allotment",
                                             required=False,  max_length=128,
                                             widget=forms.TextInput(attrs={"class": "form-control"}))
    disbursement_interest_rate = forms.FloatField(label="disbursement_interest_rate",
                                                  required=False,
                                                  widget=forms.TextInput(attrs={"class": "form-control"}))
    repayment_term = forms.IntegerField(label="repayment_term",
                                        widget=forms.TextInput(attrs={"class": "form-control"}))
    total_target = forms.FloatField(label="total_target",
                                    widget=forms.NumberInput(attrs={'id': 'form_homework', 'step': "0.01"}))
    monthly_target = forms.FloatField(label="monthly_target",
                                      widget=forms.NumberInput(attrs={'id': 'form_homework', 'step': "0.01"}))
    target_measurement_unit = forms.CharField(label="target_measurement_unit",
                                              required=False, max_length=128,
                                              widget=forms.TextInput(attrs={"class": "form-control"}))
    application_contract_document = forms.FileField(label="Application Contract Document",
                                                    required=False,
                                                    widget=forms.FileInput(attrs={"class": "form-control"}))

    # For Displaying customers inside Disbursment form
    try:
        customers = Customers.objects.all()
        customer_list = []
        for customer in customers:
            single_customer = (customer.id, customer.name)
            customer_list.append(single_customer)
    except:
        customer_list = []

    customer_id = forms.ChoiceField(
        label="Customer",   choices=customer_list, widget=forms.Select(attrs={"class": "form-control"}))


class EditDisbursementForm(forms.Form):

    disbursement_code = forms.CharField(label="disbursement_code",
                                        max_length=128,
                                        widget=forms.TextInput(attrs={"class": "form-control"}))

    disbursement_description = forms.CharField(label="disbursement_description",
                                               required=False,
                                               max_length=255,
                                               widget=forms.TextInput(attrs={"class": "form-control"}))
    disbursement_application_id = forms.CharField(label="disbursement_application_id",
                                                  required=False,
                                                  max_length=128,
                                                  widget=forms.TextInput(attrs={"class": "form-control"}))
    disbursement_reason = forms.CharField(label="disbursement_reason",
                                          required=False,
                                          max_length=255,
                                          widget=forms.TextInput(attrs={"class": "form-control"}))

    disbursement_type_list = (('Loan', 'Loan'), ('Grant', 'Grant'))
    disbursement_type = forms.ChoiceField(label="Disbursement Type",
                                          choices=disbursement_type_list,
                                          widget=forms.Select(attrs={"class": "form-control"}))
    disbursement_date = forms.DateField(label="disbursement_date",
                                        widget=forms.SelectDateWidget(attrs={"class": "form-control"}))
    disbursement_amount = forms.DecimalField(label="disbursement_amount",
                                             max_digits=10,
                                             decimal_places=2, widget=forms.NumberInput())
    contract_signed_date = forms.DateField(label="contract_signed_date",
                                           widget=forms.SelectDateWidget(attrs={"class": "form-control"}))
    disbursement_end = forms.DateField(label="disbursement_end",
                                       widget=forms.SelectDateWidget(attrs={"class": "form-control"}))
    disbursement_allotment = forms.CharField(label="disbursement_allotment",
                                             required=False,
                                             max_length=128,
                                             widget=forms.TextInput(attrs={"class": "form-control"}))
    disbursement_interest_rate = forms.FloatField(label="disbursement_interest_rate",
                                                  required=False,
                                                  widget=forms.TextInput(attrs={"class": "form-control"}))
    repayment_term = forms.IntegerField(label="repayment_term",
                                        widget=forms.TextInput(attrs={"class": "form-control"}))
    total_target = forms.FloatField(label="total_target",
                                    widget=forms.NumberInput(attrs={'id': 'form_homework', 'step': "0.01"}))
    monthly_target = forms.FloatField(label="monthly_target",
                                      widget=forms.NumberInput(attrs={'id': 'form_homework', 'step': "0.01"}))
    target_measurement_unit = forms.CharField(label="target_measurement_unit",
                                              required=False, max_length=128,
                                              widget=forms.TextInput(attrs={"class": "form-control"}))
    application_contract_document = forms.FileField(label="Application Contract Document",
                                                    required=False,
                                                    widget=forms.FileInput(attrs={"class": "form-control"}))

    # For Displaying customers inside Disbursment form
    try:
        customers = Customers.objects.all()
        customer_list = []
        for customer in customers:
            single_customer = (customer.id, customer.name)
            customer_list.append(single_customer)
    except:
        customer_list = []

    customer_id = forms.ChoiceField(
        label="Customer",   choices=customer_list, widget=forms.Select(attrs={"class": "form-control"}))
