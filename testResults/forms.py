
from django import forms
from base.models import testResults, Patient
from django.contrib.auth.models import User

CHOICES = ((True,'Yes'),(False,'No'))
class TestUploadForm(forms.ModelForm):
    results = forms.FileField(widget=forms.ClearableFileInput(),label='Upload A File')
    comments = forms.CharField(widget=forms.Textarea(),label="Additional Comments",required=False)
    patient = forms.ModelChoiceField(Patient.objects.all(),empty_label='Choose A Patient',label="Patients")
    published = forms.TypedChoiceField(choices=CHOICES,label="Release for view?",widget=forms.RadioSelect)
    class Meta:
        model = testResults
        fields = ['results','comments','patient','published']
        exclude = ('doctor',)


class UpdateTestResultForm(forms.ModelForm):
    results = forms.FileField()
    comments = forms.CharField(widget=forms.Textarea(),label="Additional Comments",required=False)
    patient = forms.ModelChoiceField(Patient.objects.all(),empty_label='Choose A Patient',label="Patients")
    published = forms.TypedChoiceField(choices=CHOICES,label="Release for view?",widget=forms.RadioSelect)
    class Meta:
        model = testResults
        fields = ['results','comments','patient','published']
        exclude = ('doctor',)
