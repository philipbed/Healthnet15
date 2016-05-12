"""
    Application: HealthNet
    File: /patientRegistration/forms.py
    Authors:
        - Nathan Stevens
        - Phillip Bedward
        - Daniel Herzig
        - George Herde
        - Samuel Launt

    Description:
        - This file contains all forms for Patient Registration.
"""
from django import forms
from django.apps import apps
from django.contrib.auth.models import User
from django.forms.widgets import NumberInput
from django.forms.extras.widgets import SelectDateWidget
from django.core.exceptions import ValidationError
from base.models import Address, Person, Insurance, Doctor, Nurse, Admin, Hospital, EmergencyContact
from datetime import date

"""
Forms for registering users
"""


class UserForm(forms.ModelForm):
    """
    @class: UserForm
    @description: When a Patient is registering, they al register as a User.
    """

    first_name = forms.CharField(required=True, label='First Name:',
                                 widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=50)
    last_name = forms.CharField(required=True, label='Last Name:',
                                widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=50)
    email = forms.EmailField(required=True, label='Email:',
                             widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=100)
    username = forms.CharField(required=True, label='Username:',
                               help_text='Required. Between 5 and 30 characters. Letters, digits and @/./+/-/_ only.',
                               widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=30, min_length=5)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Password:')
    confirmP = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Confirm Password:')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) > 5:
            return password
        else:
            raise forms.ValidationError("Passwords must be at least 5 characters")

    def clean_confirmP(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('confirmP')

        if not password2:
            raise forms.ValidationError("You must confirm your password")
        if password1 != password2:
            raise forms.ValidationError("Your passwords do not match")
        return password2


class PersonRegistrationForm(forms.ModelForm):
    """
    @class: PersonRegistrationForm
    @description: A Patient's information is linked to the Person model.  When a Patient registers,
                  they provide information for the Person model.
    """
    birthday = forms.DateField(widget=SelectDateWidget(years={1950, 1951, 1952, 1953, 1954, 1955, 1956,
                                                              1957, 1958, 1959, 1960, 1961, 1962, 1963,
                                                              1964, 1965, 1966, 1967, 1968, 1969, 1970,
                                                              1971, 1972, 1973, 1974, 1975, 1976, 1977,
                                                              1978, 1979, 1980, 1981, 1982, 1983, 1984,
                                                              1985, 1986, 1987, 1988, 1989, 1990, 1991,
                                                              1992, 1993, 1994, 1995, 1996, 1997, 1998,
                                                              1999, 2000, 2001, 2002, 2003, 2004, 2005,
                                                              2006, 2007, 2008, 2009, 2010, 2011, 2012,
                                                              2013, 2014, 2015}),
                               label='Birthday:', required=True)
    ssn = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='SSN:', required=True,
                             max_value=1000000000, min_value=100000000)
    phoneNumber = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Phone Number:',
                                     required=True, min_value=100000000, max_value=9999999999)

    class Meta:
        model = Person
        fields = ('ssn', 'birthday', 'phoneNumber')

    def clean_birthday(self):
        date = self.cleaned_data['birthday']
        if date > date.today():
            raise forms.ValidationError("This date is in the future.")
        return date


class InsuranceForm(forms.ModelForm):
    """
    class: InsuranceForm
    @description: When a Patient Registers they must provide Insurance Information.
    """
    name = forms.CharField(label='Name:', required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=100)
    policyNumber = forms.IntegerField(label='Policy Number:', required=True, max_value=999999999, min_value=1,
                                      widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Insurance
        fields = ('name', 'policyNumber')
        exclude = ('addressID',)


class AddressForm(forms.ModelForm):
    """
    @class: AddressForm
    @description: the Address of the Patient
    """

    state = forms.CharField(required=True, label='State:',
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    street = forms.CharField(required=True, label='Street:',
                             widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=100)
    city = forms.CharField(required=True, label='City:',
                           widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=100)
    zip = forms.CharField(required=True, label='Zip:',
                          widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Address
        fields = ('street', 'city', 'state', 'zip')

    def clean_zip(self):
        zip = self.cleaned_data.get('zip')
        zip = int(zip)
        if zip >= 99999:
            raise forms.ValidationError("Not a valid zip code. Use format XXXXX")
        elif zip <= 10000:
            raise forms.ValidationError("Not a valid zip code. Use format XXXXX")
        else:
            return zip

    def clean_state(self):
        from base.us_states import STATES_NORMALIZED

        state = self.cleaned_data.get('state')
        if str(state).lower() not in STATES_NORMALIZED:
            raise ValidationError('Error: Not a US state')
        else:
            return state


class EmergencyContactForm(forms.ModelForm):
    """
    @class: EmergencyContact
    @description: The EmergencyContact for the Patient
    """
    firstName = forms.CharField(required=True, label='First Name:',
                                widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=50)
    lastName = forms.CharField(required=True, label='Last Name:',
                               widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=50)
    emergencyNumber = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                                         label='Emergency Phone Number:', required=True,
                                         min_value=1000000000, max_value=10000000000)

    class Meta:
        model = EmergencyContact
        fields = ('firstName', 'lastName', 'emergencyNumber',)
        exclude = ('personID',)


class DoctorForm(forms.ModelForm):
    licenseNumber = forms.IntegerField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}),
                                       label='License Number:', min_value=1, max_value=10000)
    specialty = forms.CharField(required=True, label='Specialty:', max_length=45,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Doctor
        fields = ('licenseNumber', 'specialty')
        exclude = ('patientID', 'personID', 'hospitalID')


class NurseForm(forms.ModelForm):
    license_number = forms.IntegerField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}),
                                       label='License Number:', min_value=100, max_value=10000)
    department = forms.CharField(required=True, label='Department:', max_length=45,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Nurse
        fields = ('license_number', 'department')
        exclude = ('personID', 'hospitalID')


class AdminForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ('hospitalID',)


class DoctorRootForm(forms.ModelForm):
    hospitalID = forms.ModelChoiceField(queryset=Hospital.objects.all(), to_field_name='name', label='Hospital',
                                        empty_label='-Hospital-')
    licenseNumber = forms.IntegerField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}),
                                       label='License Number:', min_value=1, max_value=10000)
    specialty = forms.CharField(required=True, label='Specialty:',
                                widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=45)

    class Meta:
        model = Doctor
        fields = ('licenseNumber', 'specialty', 'hospitalID')
        exclude = ('patientID', 'personID')


class NurseRootForm(forms.ModelForm):
    license_number = forms.IntegerField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}),
                                       label='License Number:', min_value=100, max_value=10000)

    department = forms.CharField(required=True, label='Department:',
                                 widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=45)

    hospitalID = forms.ModelChoiceField(queryset=Hospital.objects.all(), to_field_name='name',
                                        empty_label='-Hospital-', label='Hospital:')

    class Meta:
        model = Nurse
        fields = ('license_number', 'department', 'hospitalID')
        exclude = ('personID',)


class AdminRootForm(forms.ModelForm):
    hospitalID = forms.ModelChoiceField(queryset=Hospital.objects.all(), to_field_name='name',
                                        empty_label='-Hospital-', label='Hospital', )

    class Meta:
        model = Admin
        fields = ('hospitalID',)
