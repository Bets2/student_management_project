from django import forms
from .models import Courses, SessionYearModel, Customers, Disbursements, Repayments, GrantManagement


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

    customer_status = forms.ChoiceField(label="Customer Status",
                                        choices=CUSTOMER_STATUS_LIST,
                                        widget=forms.Select(attrs={"class": "form-control"}))

    BEE_LEVEL_DATA = (('Level_1', "Level 1"), ('Level_2', "Level 2"), ('Level_3', "Level 3"), ('Level_4', "Level 4"),
                      ('Level_5', "Level 5"), ('Level_6', "Level 6"), ('Level_7', "Level 7"), ('Level_8', "Level 8"), ('None', "None"))

    bee_level = forms.ChoiceField(label="Bee Level",
                                  choices=BEE_LEVEL_DATA,
                                  widget=forms.Select(attrs={"class": "form-control"}))

    phone = forms.CharField(label="Phone Number",
                            max_length=128,
                            widget=forms.TextInput(attrs={"class": "form-control"}))
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

    BEE_LEVEL_DATA = (('Level_1', "Level 1"), ('Level_2', "Level 2"), ('Level_3', "Level 3"), ('Level_4', "Level 4"),
                      ('Level_5', "Level 5"), ('Level_6', "Level 6"), ('Level_7', "Level 7"), ('Level_8', "Level 8"), ('None', "None"))

    bee_level = forms.ChoiceField(label="Bee Level",
                                  choices=BEE_LEVEL_DATA,
                                  widget=forms.Select(attrs={"class": "form-control"}))

    phone = forms.CharField(label="Phone Number",
                            max_length=128,
                            widget=forms.TextInput(attrs={"class": "form-control"}))

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
    disbursement_amount = forms.DecimalField(label="Disbursement Amount",
                                             max_digits=10,
                                             decimal_places=2,
                                             widget=forms.NumberInput(attrs={'id': 'form-control', 'step': "0.01"}))
    disbursement_monthly_repayment_amount = forms.DecimalField(label="Disbursement Monthly Repayment Amount",
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
    contract_target = forms.FloatField(label="contract_target",
                                       widget=forms.NumberInput(attrs={'id': 'form_homework', 'step': "0.01"}))
    contract_monthly_target = forms.FloatField(label="contract_monthly_target",
                                               widget=forms.NumberInput(attrs={'id': 'form_homework', 'step': "0.01"}))
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
    disbursement_monthly_repayment_amount = forms.DecimalField(label="Disbursement Monthly Repayment Amount",
                                                               max_digits=10,
                                                               decimal_places=2,
                                                               widget=forms.NumberInput(attrs={'id': 'form-control', 'step': "0.01"}))
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

    contract_target = forms.FloatField(label="contract_target",
                                       widget=forms.NumberInput(attrs={'id': 'form_homework', 'step': "0.01"}))
    contract_monthly_target = forms.FloatField(label="contract_monthly_target",
                                               widget=forms.NumberInput(attrs={'id': 'form_homework', 'step': "0.01"}))

    application_contract_document = forms.FileField(label="Application Contract Document",
                                                    required=False,
                                                    widget=forms.FileInput(attrs={"class": "form-control"}))

    # For Displaying customers inside Disbursment form
    try:
        customers = Customers.objects.all()
        customer_list = []
        for customer in customers:
            single_customer = (customer.id, customer.customer_name)
            customer_list.append(single_customer)
    except:
        customer_list = []

    customer_id = forms.ChoiceField(
        label="Customer",   choices=customer_list, widget=forms.Select(attrs={"class": "form-control"}))

# repayment forms


class AddRepaymentForm(forms.Form):
    repayment_code = forms.CharField(label="Repayment Code",
                                     max_length=128,
                                     widget=forms.TextInput(attrs={"class": "form-control"}))
    repayment_type_list = (('Amortization', 'Amortization'),
                           ('Impairment', 'Impairment'))
    repayment_type = forms.ChoiceField(label="Repayment Type",
                                       choices=repayment_type_list,
                                       widget=forms.TextInput(attrs={"class": "form-control"}))
    repayment_description = forms.CharField(label="Repayment Description ",
                                            max_length=255,
                                            widget=forms.TextInput(attrs={"class": "form-control"}))
    repayment_amount = forms.DecimalField(label="Repayment Amount",
                                          max_digits=10,
                                          decimal_places=2,
                                          widget=forms.NumberInput(attrs={'id': 'form-control', 'step': "0.01"}))
    repayment_date = forms.CharField(label="Repayment Date",
                                     max_length=128,
                                     widget=forms.TextInput(attrs={"class": "form-control"}))
    actual_volume_tone = forms.DecimalField(label="Actual Volume Tone",
                                            max_digits=10,
                                            decimal_places=2,
                                            widget=forms.NumberInput(attrs={'id': 'form-control', 'step': "0.01"}))
    comment = forms.CharField(label="Comment if any",
                              max_length=255,
                              widget=forms.TextInput(attrs={"class": "form-control"}))
    payment_documentation = forms.FileField(label="Payment Documentation",
                                            max_length=128,
                                            widget=forms.FileInput(attrs={"class": "form-control"}))

    # For Displaying Disbursement Codes inside Create Repayments form
    try:
        disbursements = Disbursements.objects.all()
        disbursement_code_list = []
        for disbursement in disbursements:
            single_disbursement = (
                disbursement.id, disbursement.disbursement_code)
            disbursement_code_list.append(single_disbursement)
    except:
        disbursement_code_list = []

    disbursement_id = forms.ChoiceField(
        label="Disbursement Codes",   choices=disbursement_code_list, widget=forms.Select(attrs={"class": "form-control"}))

    # For Displaying customers inside Create Repayments form
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


class EditRepaymentForm(forms.Form):
    repayment_code = forms.CharField(label="Repayment Code",
                                     max_length=128,
                                     widget=forms.TextInput(attrs={"class": "form-control"}))
    repayment_type_list = (('Amortization', 'Amortization'),
                           ('Impairment', 'Impairment'))
    repayment_type = forms.ChoiceField(label="Repayment Type",
                                       choices=repayment_type_list,
                                       widget=forms.TextInput(attrs={"class": "form-control"}))
    repayment_description = forms.CharField(label="Repayment Description ",
                                            max_length=255,
                                            widget=forms.TextInput(attrs={"class": "form-control"}))
    repayment_amount = forms.DecimalField(label="Repayment Amount",
                                          max_digits=10,
                                          decimal_places=2,
                                          widget=forms.NumberInput(attrs={'id': 'form-control', 'step': "0.01"}))
    repayment_date = forms.CharField(label="Repayment Date",
                                     max_length=128,
                                     widget=forms.SelectDateWidget(attrs={"class": "form-control"}))

    actual_volume_tone = forms.DecimalField(label="Actual Volume Tone",
                                            max_digits=10,
                                            decimal_places=2,
                                            widget=forms.NumberInput(attrs={'id': 'form-control', 'step': "0.01"}))
    comment = forms.CharField(label="Comment if any",
                              max_length=255,
                              widget=forms.TextInput(attrs={"class": "form-control"}))
    payment_documentation = forms.FileField(label="Payment Documentation",
                                            max_length=128,
                                            widget=forms.FileInput(attrs={"class": "form-control"}))
    # For Displaying Disbursement Codes inside Create Repayments form
    try:
        disbursements = Disbursements.objects.all()
        disbursement_code_list = []
        for disbursement in disbursements:
            single_disbursement = (
                disbursement.id, disbursement.disbursement_code)
            disbursement_code_list.append(single_disbursement)
    except:
        disbursement_code_list = []

    disbursement_id = forms.ChoiceField(
        label="Disbursement Codes",   choices=disbursement_code_list, widget=forms.Select(attrs={"class": "form-control"}))

    # For Displaying customers inside Create Repayments form
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


# Grant Management form
class AddVolumeForm(forms.Form):
    monthly_volume_report_id = forms.CharField(label="Repayment Code",
                                               max_length=128,
                                               widget=forms.TextInput(attrs={"class": "form-control"}))
    volume_report_month_list = (('January', 'January'), ('February', 'February'), ('March', 'March'), ('April', 'April'),
                                ('May', 'May'), ('June', 'June'), ('July',
                                                                   'July'), ('August', 'August'), ('September', 'September'),
                                ('October', 'October'), ('November', 'November'), ('December', 'December'))
    volume_report_month = forms.ChoiceField(
        label="Volume Report Month", choices=volume_report_month_list, widget=forms.TextInput(attrs={"class": "form-control"}))
    volume_report_year_list = (('2014', '2014'), ('2015', '2015'), ('2016', '2016'), ('2017', '2017'), ('2018', '2018'),
                               ('2019', '2019'), ('2020', '2020'), ('2021',
                                                                    '2021'), ('2022', '2022'), ('2023', '2023'),
                               ('2024', '2024'), ('2025', '2025'), ('2026', '2026'), ('2027', '2027'), ('2028', '2028'), ('2029', '2029'), ('2030', '2030'))

    volume_report_year = forms.ChoiceField(
        label="Volume Report Month", choices=volume_report_year_list, widget=forms.TextInput(attrs={"class": "form-control"}))
    hd_kg = forms.DecimalField(label="HD KG",
                               max_digits=10,
                               decimal_places=2,
                               widget=forms.NumberInput(attrs={'id': 'form-control', 'step': "0.01"}))
    ld_kg = forms.DecimalField(label="LD KG",
                               max_digits=10,
                               decimal_places=2,
                               widget=forms.NumberInput(attrs={'id': 'form-control', 'step': "0.01"}))
    lld_kg = forms.DecimalField(label="LLD KGt",
                                max_digits=10,
                                decimal_places=2,
                                widget=forms.NumberInput(attrs={'id': 'form-control', 'step': "0.01"}))
    pp_kg = forms.DecimalField(label="PP KG",
                               max_digits=10,
                               decimal_places=2,
                               widget=forms.NumberInput(attrs={'id': 'form-control', 'step': "0.01"}))
    pvc_kg = forms.DecimalField(label="PVC KG",
                                max_digits=10,
                                decimal_places=2,
                                widget=forms.NumberInput(attrs={'id': 'form-control', 'step': "0.01"}))
    ps_kg = forms.DecimalField(label="PS KG",
                               max_digits=10,
                               decimal_places=2,
                               widget=forms.NumberInput(attrs={'id': 'form-control', 'step': "0.01"}))
    pet_kg = forms.DecimalField(label="PET KG",
                                max_digits=10,
                                decimal_places=2,
                                widget=forms.NumberInput(attrs={'id': 'form-control', 'step': "0.01"}))
    other_kg = forms.DecimalField(label="Other KG",
                                  max_digits=10,
                                  decimal_places=2,
                                  widget=forms.NumberInput(attrs={'id': 'form-control', 'step': "0.01"}))
    total_volume_kg = forms.DecimalField(label="Total Volume KG",
                                         max_digits=10,
                                         decimal_places=2,
                                         widget=forms.NumberInput(attrs={'id': 'form-control', 'step': "0.01"}))
    volume_report_date = forms.CharField(label="Repayment Date",
                                         max_length=128,
                                         widget=forms.TextInput(attrs={"class": "form-control"}))
    amount_amortized = forms.DecimalField(label="Amount Amortized",
                                          max_digits=10,
                                          decimal_places=2,
                                          widget=forms.NumberInput(attrs={'id': 'form-control', 'step': "0.01"}))
    amount_impaired = forms.DecimalField(label="Amount Impaired",
                                         max_digits=10,
                                         decimal_places=2,
                                         widget=forms.NumberInput(attrs={'id': 'form-control', 'step': "0.01"}))

    # For Displaying customers inside Create Repayments form
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

    # For Displaying Disbursement Codes inside Create Repayments form
    try:
        disbursements = Disbursements.objects.all()
        disbursement_code_list = []
        for disbursement in disbursements:
            single_disbursement = (
                disbursement.id, disbursement.disbursement_code)
            disbursement_code_list.append(single_disbursement)
    except:
        disbursement_code_list = []

    disbursement_id = forms.ChoiceField(
        label="Disbursement Codes",   choices=disbursement_code_list, widget=forms.Select(attrs={"class": "form-control"}))


class EditVolumeForm(forms.Form):
    monthly_volume_report_id = forms.CharField(label="Repayment Code",
                                               max_length=128,
                                               widget=forms.TextInput(attrs={"class": "form-control"}))
    volume_report_month_list = (('January', 'January'), ('February', 'February'), ('March', 'March'), ('April', 'April'),
                                ('May', 'May'), ('June', 'June'), ('July',
                                                                   'July'), ('August', 'August'), ('September', 'September'),
                                ('October', 'October'), ('November', 'November'), ('December', 'December'))
    volume_report_month = forms.ChoiceField(
        label="Volume Report Month", choices=volume_report_month_list, widget=forms.TextInput(attrs={"class": "form-control"}))
    volume_report_year_list = (('2014', '2014'), ('2015', '2015'), ('2016', '2016'), ('2017', '2017'), ('2018', '2018'),
                               ('2019', '2019'), ('2020', '2020'), ('2021',
                                                                    '2021'), ('2022', '2022'), ('2023', '2023'),
                               ('2024', '2024'), ('2025', '2025'), ('2026', '2026'), ('2027', '2027'), ('2028', '2028'), ('2029', '2029'), ('2030', '2030'))

    volume_report_year = forms.ChoiceField(
        label="Volume Report Month", choices=volume_report_year_list, widget=forms.TextInput(attrs={"class": "form-control"}))
    hd_kg = forms.DecimalField(label="HD KG",
                               max_digits=10,
                               decimal_places=2,
                               widget=forms.NumberInput(attrs={'id': 'form-control', 'step': "0.01"}))
    ld_kg = forms.DecimalField(label="LD KG",
                               max_digits=10,
                               decimal_places=2,
                               widget=forms.NumberInput(attrs={'id': 'form-control', 'step': "0.01"}))
    lld_kg = forms.DecimalField(label="LLD KGt",
                                max_digits=10,
                                decimal_places=2,
                                widget=forms.NumberInput(attrs={'id': 'form-control', 'step': "0.01"}))
    pp_kg = forms.DecimalField(label="PP KG",
                               max_digits=10,
                               decimal_places=2,
                               widget=forms.NumberInput(attrs={'id': 'form-control', 'step': "0.01"}))

    pvc_kg = forms.DecimalField(label="PVC KG",
                                max_digits=10,
                                decimal_places=2,
                                widget=forms.NumberInput(attrs={'id': 'form-control', 'step': "0.01"}))
    ps_kg = forms.DecimalField(label="PS KG",
                               max_digits=10,
                               decimal_places=2,
                               widget=forms.NumberInput(attrs={'id': 'form-control', 'step': "0.01"}))
    pet_kg = forms.DecimalField(label="PET KG",
                                max_digits=10,
                                decimal_places=2,
                                widget=forms.NumberInput(attrs={'id': 'form-control', 'step': "0.01"}))
    other_kg = forms.DecimalField(label="Other KG",
                                  max_digits=10,
                                  decimal_places=2,
                                  widget=forms.NumberInput(attrs={'id': 'form-control', 'step': "0.01"}))
    total_volume_kg = forms.DecimalField(label="Total Volume KG",
                                         max_digits=10,
                                         decimal_places=2,
                                         widget=forms.NumberInput(attrs={'id': 'form-control', 'step': "0.01"}))
    volume_report_date = forms.CharField(label="Repayment Date",
                                         max_length=128,
                                         widget=forms.TextInput(attrs={"class": "form-control"}))
    amount_amortized = forms.DecimalField(label="Amount Amortized",
                                          max_digits=10,
                                          decimal_places=2,
                                          widget=forms.NumberInput(attrs={'id': 'form-control', 'step': "0.01"}))
    amount_impaired = forms.DecimalField(label="Amount Impaired",
                                         max_digits=10,
                                         decimal_places=2,
                                         widget=forms.NumberInput(attrs={'id': 'form-control', 'step': "0.01"}))

    # For Displaying customers inside Create Repayments form
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

    # For Displaying Disbursement Codes inside Create Repayments form
    try:
        disbursements = Disbursements.objects.all()
        disbursement_code_list = []
        for disbursement in disbursements:
            single_disbursement = (
                disbursement.id, disbursement.disbursement_code)
            disbursement_code_list.append(single_disbursement)
    except:
        disbursement_code_list = []

    disbursement_id = forms.ChoiceField(
        label="Disbursement Codes",   choices=disbursement_code_list, widget=forms.Select(attrs={"class": "form-control"}))
