from django.apps import apps
from django import forms
from django.utils import timezone
from django.contrib.auth.models import User

prescription = apps.get_model('base', 'Prescription')
medication = apps.get_model('base', 'Medication')
Patient = apps.get_model('base', 'Patient')
Doctor = apps.get_model('base', 'Doctor')

class PrescriptionForm(forms.ModelForm):
    patient = forms.ModelChoiceField(queryset=Patient.objects.all(), empty_label="Choose a patient")
    amount = forms.IntegerField(label='Amount:', required=True, help_text='MG')
    refill = forms.IntegerField(label='Refill:', required=True, help_text='refills')
    timestamp = forms.DateTimeField()
    
    class Meta:
        model = prescription
        fields = ('patient', 'amount', 'refill',)
        exclude =('medicationID','doctor', 'timestamp')

class MedicationForm(forms.ModelForm):
    name = forms.CharField(label='Medication Name', required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label='Medication Description',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = medication
        fields = ('name','description')


class DeletePrescription(forms.ModelForm):
    """
    @class: DeletePrescription
    @description: This form is used for deleting an Prescription
    """
    class Meta:
        model = prescription
        fields = []

