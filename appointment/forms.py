"""
    Application: HealthNet
    File: appointment/forms.py
    Authors:
        - Nathan Stevens
        - Phillip Bedward
        - Daniel Herzig
        - George Herde
        - Samuel Launt

    Description:
        - This file contains all the forms for the appointment update and schedule
          functionality.
"""
from base.models import Appointment, Doctor, Patient
from django.forms.extras.widgets import SelectDateWidget
from django.apps import apps
from django import forms
from datetime import date, datetime


class AppointmentForm(forms.Form):
    """
    @class: AppointmentForm
    @description: This form is used for scheduling an appointment.
    """
    docList = forms.ModelChoiceField(queryset=Doctor.objects.all(), empty_label="Choose A Doctor")
    date_field = forms.DateField(widget=forms.DateInput())
    time = forms.TimeField(widget=forms.TimeInput(format='%I:%M %p'))
    reason = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Appointment
        fields = ('docList', 'date_field', 'time', 'reason')

    def clean_time(self):
        date = self.cleaned_data['date_field']
        time = self.cleaned_data['time']
        curDay = date.today()
        if date < curDay:
            raise forms.ValidationError("This day has passed.")
        elif date == curDay:
            t = datetime.now().time()
            if time < t:
                raise forms.ValidationError("This time has passed.")
        return time

    # Validation on the time and possible conflict with another appointment is checked in the view


class AppointmentNurseForm(forms.Form):
    """
    @class: AppointmentForm
    @description: This form is used for scheduling an appointment.
    """
    patList = forms.ModelChoiceField(queryset=Patient.objects.all(), empty_label="Choose A Patient")
    date_field = forms.DateField(widget=forms.DateInput())
    time = forms.TimeField(widget=forms.TimeInput(format='%I:%M %p'))
    reason = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Appointment
        fields = ('docList', 'date_field', 'time', 'reason', 'patList')

    def __init__(self, *args, **kwargs):
        nurHospital = kwargs.pop('nurHospital')
        super(AppointmentNurseForm, self).__init__(*args, **kwargs)
        hospitalDoctorList = Doctor.objects.filter(hospitalID=nurHospital)
        self.fields['docList'] = forms.ModelChoiceField(queryset=hospitalDoctorList, empty_label="Choose a doctor")


    def clean_time(self):
        date = self.cleaned_data['date_field']
        time = self.cleaned_data['time']
        curDay = date.today()
        if date < curDay:
            raise forms.ValidationError("This day has passed.")
        elif date == curDay:
            t = datetime.now().time()
            if time < t:
                raise forms.ValidationError("This time has passed.")
        return time

    # Validation on the time and possible conflict with another appointment is checked in the view


class AppointmentDoctorForm(forms.Form):
    """
    @class: AppointmentForm
    @description: This form is used for scheduling an appointment.
    """
    patList = forms.ModelChoiceField(queryset=Patient.objects.all(), empty_label="Choose A Patient")
    date_field = forms.DateField(widget=forms.DateInput())
    time = forms.TimeField(widget=forms.TimeInput(format='%I:%M %p'))
    reason = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Appointment
        fields = ('patList', 'date_field', 'time', 'reason')

    def clean_time(self):
        date = self.cleaned_data['date_field']
        time = self.cleaned_data['time']
        curDay = date.today()
        if date < curDay:
            raise forms.ValidationError("This day has passed.")
        elif date == curDay:
            t = datetime.now().time()
            if time < t:
                raise forms.ValidationError("This time has passed.")
        return time

    # Validation on the time and possible conflict with another appointment is checked in the view


class UpdateAppointmentForm(forms.ModelForm):
    docList = forms.ModelChoiceField(queryset=Doctor.objects.all(), empty_label="Choose A Doctor")
    date_field = forms.DateField(widget=forms.DateInput())
    time = forms.TimeField(widget=forms.TimeInput(format='%I:%M %p'))
    reason = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Appointment
        fields = ('docList', 'date_field', 'time', 'reason')

    def clean_time(self):
        date = self.cleaned_data['date_field']
        time = self.cleaned_data['time']
        curDay = date.today()
        if date < curDay:
            raise forms.ValidationError("This day has passed.")
        elif date == curDay:
            t = datetime.now().time()
            if time < t:
                raise forms.ValidationError("This time has passed.")
        return time

    # Validation on the time and possible conflict with another appointment is checked in the view


class DeleteAppointment(forms.ModelForm):
    """
    @class: DeleteAppointment
    @description: This form is used for deleting an appointment
    """

    class Meta:
        model = Appointment
        fields = []
