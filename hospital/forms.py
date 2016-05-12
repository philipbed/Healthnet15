"""
    Application: HealthNet
    File: hospital/forms.py
    Authors:
        - Nathan Stevens
        - Phillip Bedward
        - Daniel Herzig
        - George Herde
        - Samuel Launt

    Description:
        - This file contains all the forms for the hospital creation and update
"""
from django.apps import apps
from django import forms
from base.models import Hospital, Address


class HospitalForm(forms.ModelForm):
    name = forms.CharField(required=True, label='Hospital Name:')

    class Meta:
        model = Hospital
        fields = ('name',)
        exclude = ('addressID',)


class AddressForm(forms.ModelForm):
    """
    @class: AddressForm
    @description: the Address of the Hospital
    """

    class Meta:
        model = Address
        fields = ('street', 'zip', 'city', 'state')


class DeleteHospital(forms.ModelForm):
    class Meta:
        model = Hospital
        fields = []
