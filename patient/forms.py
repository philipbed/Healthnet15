"""
    Application: HealthNet
    File: /patient/forms.py
    Authors:
        - Nathan Stevens
        - Philip Bedward
        - Daniel Herzig
        - George Herde
        - Samuel Launt

    Description:
        - This file contains all view controller information
"""
from base.models import ExtendedStay
from django.apps import apps
from django import forms
from django.contrib.auth.models import User
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import NumberInput

address = apps.get_model('base', 'Address')
person = apps.get_model('base', 'Person')
insurance = apps.get_model('base', 'Insurance')
doctor = apps.get_model('base', 'Doctor')
nurse = apps.get_model('base', 'Nurse')
admin = apps.get_model('base', 'Admin')


# Custom forms for the PatientRegistration
class UserForm(forms.ModelForm):
    """
    @class: UserForm
    @description: This form is where the User information is updated
    """
    first_name = forms.CharField(required=True, label='First Name:')
    last_name = forms.CharField(required=True, label='Last Name:')
    email = forms.EmailField(required=True, label='Email:')
    username = forms.CharField(required=True, label='Username:',
                               help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


class PersonRegistrationForm(forms.ModelForm):
    """
    @class: PersonRegistrationForm
    @description: This form is where the Person specific information is entered
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
                               label='Birthday:')
    # ssn = forms.IntegerField(widget=NumberInput, label='SSN:')
    # phoneNumber = USPhoneNumberField()

    class Meta:
        model = apps.get_model('base', 'Person')
        fields = ('birthday', 'phoneNumber')
        exclude = ('ssn',)


class InsuranceForm(forms.ModelForm):
    """
    @class: InsuranceForm
    @description: This form is where the Insurance information is supplied
    """
    name = forms.CharField(label='Name:')
    policyNumber = forms.IntegerField(label='Policy Number:')

    class Meta:
        model = apps.get_model('base', 'Insurance')
        fields = ('name', 'policyNumber')
        exclude = ('addressID',)


class AddressForm(forms.ModelForm):
    """
    @class: AddressForm
    @description: This form is where the Address information is provided
    """
    # zip =  USZipCodeField()
    # state = USStateField()
    #
    class Meta:
        model = apps.get_model('base', 'Address')
        fields = ('street', 'zip', 'city', 'state')


class EmergencyContactForm(forms.ModelForm):
    """
    @class: EmergencyContactForm
    @description: This form is where the Emergency Contact information is entered
    """
    firstName = forms.CharField(required=True, label='First Name:')
    lastName = forms.CharField(required=True, label='Last Name:')
    # emergencyNumber = USPhoneNumberField()


    class Meta:
        model = apps.get_model('base', 'EmergencyContact')
        fields = ('firstName', 'lastName', 'emergencyNumber')
        exclude = ('personID',)


class AdminForm(forms.ModelForm):
    hospital = forms.ModelChoiceField(queryset=admin.objects.all(), empty_label='Choose A Hospital')

    class Meta:
        model = admin
        fields = ('hospital',)


class DeleteDoctor(forms.ModelForm):
    class Meta:
        model = doctor
        fields = []


class DeleteNurse(forms.ModelForm):
    class Meta:
        model = nurse
        fields = []


class DeleteAdmin(forms.ModelForm):
    class Meta:
        model = admin
        fields = []

class AdmitPatient(forms.ModelForm):
    endDate = forms.DateField(label='Choose A date to discharge this patient')
    endTime = forms.TimeField(label='Choose A time to discharge this patient')
    class Meta:
        model = ExtendedStay
        fields = ('endDate','endTime')

class DischargePatient(forms.ModelForm):
    class Meta:
        model = ExtendedStay
        fields = []

class TransferPatientForm(forms.ModelForm):
    class Meta:
        model = ExtendedStay
        fields = []
