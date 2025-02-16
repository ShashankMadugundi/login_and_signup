# from django import forms
# from django.core.validators import RegexValidator
# from django.contrib.auth.password_validation import validate_password
# from .models import User
# from django.core.exceptions import ValidationError
# from django.core.validators import RegexValidator

# class UserRegistrationForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), validators=[
#         RegexValidator(
#             regex=r'^(?=.*[A-Z])(?=.*\W).{8,}$',
#             message='Password must be at least 8 characters long, include one uppercase letter and one special character.'
#         ),
#         validate_password
#     ])
#     confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

#     class Meta:
#         model = User
#         fields = ['full_name', 'email', 'mobile_number', 'password']
        
#         widgets = {
#             'full_name': forms.TextInput(attrs={'placeholder': 'Name'}),
#             'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
#             'mobile_number': forms.TextInput(attrs={'placeholder': 'Mobile Number'}),
#         }
#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         if User.objects.filter(email=email).exists():
#             raise forms.ValidationError("Email already exists.")
#         return email

#     def clean_mobile_number(self):
#         mobile_number = self.cleaned_data.get('mobile_number')
        
#         # Validate 10-digit mobile number
#         validator = RegexValidator(regex=r'^\d{10}$', message="Enter a valid 10-digit mobile number.")
#         try:
#             validator(mobile_number)
#         except ValidationError:
#             raise forms.ValidationError("Enter a valid mobile number.")
    
#         # Check if mobile number already exists
#         if User.objects.filter(mobile_number=mobile_number).exists():
#             raise forms.ValidationError("Mobile number already registered.")
        
#         return mobile_number
#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get('password')
#         confirm_password = cleaned_data.get('confirm_password')

#         if password != confirm_password:
#             self.add_error('confirm_password', "Passwords do not match.")


# from django import forms

# # class UserLoginForm(forms.Form):
# #     email = forms.EmailField()
# #     password = forms.CharField(widget=forms.PasswordInput)

# class UserLoginForm(forms.Form):
#     email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email","class":"form-control"}))
#     password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password","class":"form-control"}))







from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from .models import User

class UserRegistrationForm(forms.ModelForm):
    COUNTRY_CODES = [
    ('+1', 'USA'),
    ('+91', 'IND'),
    ('+44', 'UK'),
    ('+61', 'AUS'),
    ('+81', 'JPN'),
    ('+49', 'GER'),
    ('+33', 'FRA'),
    ('+55', 'BRA'),
    ('+86', 'CHN'),
    ('+7', 'RUS'),
    ('+996', 'KGZ'),
    ('+856', 'LAO'),
    ('+371', 'LVA'),
    ('+961', 'LBN'),
    ('+266', 'LSO'),
    ('+231', 'LBR'),
    ('+218', 'LBY'),
    ('+423', 'LIE'),
    ('+370', 'LTU'),
    ('+352', 'LUX'),
    ('+853', 'MAC'),
    ('+389', 'MKD'),
    ('+261', 'MDG'),
    ('+265', 'MWI'),
    ('+60', 'MYS'),
    ('+258', 'MOZ'),
    ('+264', 'NAM'),
    ('+674', 'NRU'),
    ('+977', 'NPL'),
    ('+31', 'NLD'),
    ('+599', 'ABW'),
    ('+687', 'NCL'),
    ('+64', 'NZL'),
    ('+850', 'PRK'),
    ('+47', 'NOR'),
    ('+968', 'OMN'),
    ('+92', 'PAK'),
    ('+680', 'PLW'),
    ('+970', 'PSE'),
    ('+507', 'PAN'),
    ('+675', 'PNG'),
    ('+595', 'PRY'),
    ('+51', 'PER'),
    ('+63', 'PHL'),
    ('+48', 'POL'),
    ('+351', 'PRT'),
    ('+1787', 'PRI'),
    ('+590', 'GLP'),
    ('+974', 'QAT'),
    ('+40', 'ROU'),
    ('+250', 'RWA'),
    ('+378', 'SMR'),
    ('+239', 'STP'),
    ('+221', 'SEN'),
    ('+248', 'SYC'),
    ('+232', 'SLE'),
    ('+65', 'SGP'),
    ('+421', 'SVK'),
    ('+386', 'SVN'),
    ('+963', 'SYR'),
    ('+268', 'SWZ'),
    ('+886', 'TWN'),
    ('+992', 'TJK'),
    ('+255', 'TZA'),
    ('+66', 'THA'),
    ('+670', 'TLS'),
    ('+228', 'TGO'),
    ('+216', 'TUN'),
    ('+90', 'TUR'),
    ('+993', 'TKM'),
    ('+256', 'UGA'),
    ('+380', 'UKR'),
    ('+44', 'GBR'),
    ]


    country_code = forms.ChoiceField(choices=COUNTRY_CODES, initial='+91',required=True, widget=forms.Select(attrs={'class': 'form-control'}))

    mobile_number = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Mobile Number'}),
        validators=[RegexValidator(regex=r'^\d{10}$', message="Enter a valid 10-digit mobile number.")]
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        validators=[
            RegexValidator(
                regex=r'^(?=.*[A-Z])(?=.*\W).{8,}$',
                message='Password must be at least 8 characters long, include one uppercase letter and one special character.'
            )
        ]
    )
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['full_name', 'email', 'country_code', 'mobile_number', 'password']

        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email

    def clean_mobile_number(self):
        country_code = self.cleaned_data.get('country_code')
        mobile_number = self.cleaned_data.get('mobile_number')

        if not mobile_number.isdigit() or len(mobile_number) != 10:
            raise forms.ValidationError("Enter a valid 10-digit mobile number.")

        # Get the full number by adding the country code with a "+" symbol.
        full_number = f"{country_code}{mobile_number}"  # Ensure no space here.

        if User.objects.filter(mobile_number=full_number).exists():
            raise forms.ValidationError("Mobile number already registered.")

        print(full_number)
        return full_number

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")




class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email","class":"form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password","class":"form-control"}))
