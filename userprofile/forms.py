"""
    Application: HealthNet
    File: /patientUpdate/forms.py
    Authors:
        - Nathan Stevens
        - Philip Bedward
        - Daniel Herzig
        - George Herde
        - Samuel Launt

    Description:
        - This file contains all view controller information
"""
from django.apps import apps
from django import forms
from base.models import EmergencyContact, Insurance, Address, Doctor, Nurse, Admin, Person
from django.contrib.auth.models import User
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import NumberInput

address = apps.get_model('base', 'Address')
person = apps.get_model('base', 'Person')
insurance = apps.get_model('base', 'Insurance')
doctor = apps.get_model('base', 'Doctor')
nurse = apps.get_model('base', 'Nurse')
admin = apps.get_model('base', 'Admin')
hosp = apps.get_model('base', 'Hospital')

def snnValidate(value):
    if (value < 100000000) or (value >= 1000000000):
        raise ValidationError('Error: Not a SSN XXXXXXXXX')


def zipValidate(value):
    if (value < 10000) or (value > 100000):
        raise ValidationError('Error: Not a zip code XXXXX')


def phoneValidate(value):
    if (value < 1000000000) or (value > 10000000000):
        raise ValidationError('Error: Not a full Phone number XXXXXXXXXX')


def stateValidator(value):
    from base.us_states import STATES_NORMALIZED
    if str(value).lower() not in STATES_NORMALIZED:
        raise ValidationError('Error: Not a US state')
"""
EVERYTHING ELSE
"""



# Custom forms for the PatientRegistration
class UserForm(forms.ModelForm):
    """
    @class: UserForm
    @description: This form is where the User information is updated
    """
    first_name = forms.CharField(required=True, label='First Name:',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=True, label='Last Name:',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, label='Email:',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(required=True, label='Username:',
                               help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))

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
    phoneNumber = forms.IntegerField(widget=NumberInput, label='Phone Number:', required=True,validators=[phoneValidate])

    class Meta:
        model = Person
        fields = ('birthday', 'phoneNumber')
        exclude = ('ssn',)


class InsuranceForm(forms.ModelForm):
    """
    @class: InsuranceForm
    @description: This form is where the Insurance information is supplied
    """
    name = forms.CharField(label='Name:',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    policyNumber = forms.IntegerField(label='Policy Number:')

    class Meta:
        model = Insurance
        fields = ('name', 'policyNumber')
        exclude = ('addressID',)


class AddressForm(forms.ModelForm):
    """
    @class: AddressForm
    @description: This form is where the Address information is provided
    """
    state = forms.CharField(required=True, label='State:', validators=[stateValidator],
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    street = forms.CharField(required=True, label='Street:',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.CharField(required=True, label='City:',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    zip = forms.CharField(required=True, label='Zip:',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Address
        fields = ('street', 'zip', 'city', 'state')


class EmergencyContactForm(forms.ModelForm):
    """
    @class: EmergencyContactForm
    @description: This form is where the Emergency Contact information is entered
    """
    firstName = forms.CharField(required=True, label='First Name:',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    lastName = forms.CharField(required=True, label='Last Name:',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    emergencyNumber = forms.IntegerField(widget=NumberInput, label='Emergency Phone Number:', required=True,
                                         validators=[phoneValidate])


    class Meta:
        model = EmergencyContact
        fields = ('firstName', 'lastName', 'emergencyNumber')
        exclude = ('personID',)


class AdminForm(forms.ModelForm):
    hospital = forms.ModelChoiceField(queryset=admin.objects.all(), empty_label='Choose A Hospital')

    class Meta:
        model = Admin
        fields = ('hospital',)


class updateDoctorForm(forms.ModelForm):
    licenseNumber = forms.IntegerField(required=True, widget=forms.NumberInput, label='License Number:')
    specialty = forms.CharField(required=True, label='Specialty:',
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Doctor
        fields = ('licenseNumber', 'specialty')
        exclude = ('patientID', 'personID', 'hospitalID')


class DeleteDoctor(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = []


class updateNurseForm(forms.ModelForm):
    license_number = forms.IntegerField(required=True, widget=forms.NumberInput, label='License Number:')
    department = forms.CharField(required=True, label='Department:',
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Nurse
        fields = ('license_number', 'department')
        exclude = ('personID', 'hospitalID')


class DeleteNurse(forms.ModelForm):
    class Meta:
        model = Nurse
        fields = []


class updateAdminForm(forms.ModelForm):
    hospitalID = forms.ModelChoiceField(queryset=hosp.objects.all(), to_field_name='name', label='Hospital')

    class Meta:
        model = Admin
        fields = ('hospitalID',)


class DeleteAdmin(forms.ModelForm):
    class Meta:
        model = Admin
        fields = []

class MoveNurse(forms.ModelForm):
    hospitals = forms.ModelChoiceField(queryset=hosp.objects.all(),to_field_name='name',empty_label='Choose A Hospital')
    class Meta:
        model = Nurse
        fields = ('hospitals',)
        exclude = ('department','license_number','personID','addressID')

    def __init__(self,hospitalID,*args,**kwargs):
        super(MoveNurse, self).__init__(*args,**kwargs)
        self.fields['hospitals'].queryset = hosp.objects.exclude(id=hospitalID)

class MoveDoctor(forms.ModelForm):
    hospitals = forms.ModelChoiceField(queryset=hosp.objects.all(),to_field_name='name',empty_label='Choose A Hospital')
    class Meta:
        model = Doctor
        fields = ('hospitals',)
        exclude = ('department','license_number','personID','addressID')

    def __init__(self,hospitalID,*args,**kwargs):
        super(MoveNurse, self).__init__(*args,**kwargs)
        self.fields['hospitals'].queryset = hosp.objects.exclude(id=hospitalID)

class PreferredHospitalForm(forms.Form):

    hospital = forms.ModelChoiceField(queryset=hosp.objects.all(),label="1.",to_field_name='name',empty_label='Choose A Hospital')

class RootMoveNurseForm(forms.ModelForm):
    personnel = forms.ModelChoiceField(queryset=Nurse.objects.all(),empty_label='Choose a Nurse',label='Nurse:')
    destinationHosp = forms.ModelChoiceField(queryset=hosp.objects.all(),to_field_name='name',empty_label='Choose A Hospital',label='Destination:')

    class Meta:
        model = Nurse
        fields = ('personnel','destinationHosp')
        exclude = ('department','license_number','personID','addressID')

class RootMoveDoctorForm(forms.ModelForm):
    personnel = forms.ModelChoiceField(queryset=Doctor.objects.all(),empty_label='Choose a Nurse',label='Nurse:')
    destinationHosp = forms.ModelChoiceField(queryset=hosp.objects.all(),to_field_name='name',empty_label='Choose A Hospital',label='Destination:')

    class Meta:
        model = Doctor
        fields = ('personnel','destinationHosp')
        exclude = ('department','license_number','personID','addressID')