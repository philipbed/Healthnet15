from django import forms
from django.contrib.auth.models import User
from django.apps import apps
from base.models import Person, Hospital


class logFilter(forms.Form):
    """
    @class: logFilter
    @description: This form is used to decide how the log is ordered
    """
    startDate = forms.DateField(widget=forms.DateInput(), required=False, label='Start Date', help_text='MM/DD/YYYY')
    endDate = forms.DateField(widget=forms.DateInput(), required=False, label='End Date', help_text='MM/DD/YYYY')
    ascending = forms.BooleanField(required=False)

    def clean_startDate(self):
        startDate = self.cleaned_data.get('startDate')
        if startDate is None:
            import datetime
            startDate = datetime.datetime.today() - datetime.timedelta(weeks=100)
            return startDate.strftime("%Y%m%d")
        else:
            return startDate.strftime("%Y%m%d")

    def clean_endDate(self):
        endDate = self.cleaned_data.get('endDate')
        import datetime
        if endDate is None:
            endDate = datetime.datetime.today()
            return endDate.strftime("%Y%m%d")
        else:
            startDate = self.cleaned_data.get('startDate')
            startDate = datetime.date(year=int(str(startDate)[:4]),
                                      month=int(str(startDate)[4:6]),
                                      day=int(str(startDate)[6:]))
            if endDate > startDate:
                return endDate.strftime("%Y%m%d")
            else:
                raise forms.ValidationError('End Date Needs to be after the start date')

    def clean_ascending(self):
        ascending = self.cleaned_data.get('ascending')
        if ascending:
            return 1
        else:
            return 0


class statFilter(forms.Form, ):
    """
    @class: statFilter
    @description: This form is used to decide the range for statistics
    """
    startDate = forms.DateField(widget=forms.DateInput(), required=False, label='Start Date', help_text='MM/DD/YYYY')
    endDate = forms.DateField(widget=forms.DateInput(), required=False, label='End Date', help_text='MM/DD/YYYY')
    hospital = forms.ModelChoiceField(queryset=Hospital.objects.all(), label='Hospital', required=False)

    def __init__(self, *args, **kwargs):
        hospital_filter = kwargs.pop('hospital_filter', None)
        super(statFilter, self).__init__(*args, **kwargs)
        if hospital_filter is not None:
            self.fields['hospital'] = forms.ModelChoiceField(queryset=Hospital.objects.filter(id=hospital_filter.id),
                                                             empty_label='Choose a hospital',
                                                             label='Hospital', required=True)
        else:
            self.fields['hospital'] = forms.ModelChoiceField(queryset=Hospital.objects.all(),
                                                             empty_label='Choose a hospital',
                                                             label='Hospital', required=False)

    def clean_startDate(self):
        startDate = self.cleaned_data.get('startDate')
        if startDate is None:
            import datetime
            startDate = datetime.datetime.today() - datetime.timedelta(weeks=100)
            return startDate.strftime("%Y%m%d")
        else:
            return startDate.strftime("%Y%m%d")

    def clean_endDate(self):
        endDate = self.cleaned_data.get('endDate')
        import datetime
        if endDate is None:
            endDate = datetime.datetime.today()
            return endDate.strftime("%Y%m%d")
        else:
            startDate = self.cleaned_data.get('startDate')
            startDate = datetime.date(year=int(str(startDate)[:4]),
                                      month=int(str(startDate)[4:6]),
                                      day=int(str(startDate)[6:]))
            if endDate > startDate:
                return endDate.strftime("%Y%m%d")
            else:
                raise forms.ValidationError('End Date Needs to be after the start date')

    def clean_hospital(self):
        hospital = self.cleaned_data.get('hospital')
        if hospital is None:
            return None
        else:
            return hospital