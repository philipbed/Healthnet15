"""
    Application: HealthNet
    File: messaging/forms.py
    Authors:
        - Nathan Stevens
        - Phillip Bedward
        - Daniel Herzig
        - George Herde - Samuel Launt

    Description:
        - This file contains all the forms for the messaging functionality.
"""
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from itertools import chain

if "notification" in settings.INSTALLED_APPS and getattr(settings, 'DJANGO_MESSAGES_NOTIFY', True):
    from notification import models as notification
else:
    notification = None

from base.models import Message, Doctor, Nurse, Patient, Person, Admin, Root
from .fields import CommaSeparatedUserField


class ComposeForm(forms.Form):
    """
    A simple default form for private messages.
    """
    # recipient = CommaSeparatedUserField(label=_(u"Recipient"),
    #                                     widget=forms.TextInput(attrs={'class': 'form-control'}))
    recipient = forms.ModelChoiceField(queryset=Person.objects.all(), empty_label="Choose a person")
    subject = forms.CharField(label=_(u"Subject"), max_length=120,
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    body = forms.CharField(label=_(u"Body"), max_length=500,
                           widget=forms.Textarea(attrs={'rows': '12', 'cols': '55', 'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        recipient_filter = kwargs.pop('recipient_filter', None)
        super(ComposeForm, self).__init__(*args, **kwargs)
        if recipient_filter is not None:
            self.fields['recipient']._recipient_filter = recipient_filter
            if recipient_filter == 'Root':
                userList = Person.objects.all()
            else:
                userPK = []
                if recipient_filter == 'Patient':
                    # Add to list the nurses
                    for nur in Nurse.objects.all():
                        userPK.append(nur.personID.id)
                    # Add to list the doctors
                    for doc in Doctor.objects.all():
                        userPK.append(doc.personID.id)

                elif recipient_filter == 'Nurse':
                    # Add to list the patients
                    for pat in Patient.objects.all():
                        userPK.append(pat.personID.id)
                    # Add to list the nurses
                    for nur in Nurse.objects.all():
                        userPK.append(nur.personID.id)
                    # Add to list the doctors
                    for doc in Doctor.objects.all():
                        userPK.append(doc.personID.id)


                elif recipient_filter == 'Doctor':
                    # Add to list the patients
                    for pat in Patient.objects.all():
                        userPK.append(pat.personID.id)
                    # Add to list the nurses
                    for nur in Nurse.objects.all():
                        userPK.append(nur.personID.id)
                    # Add to list the doctors
                    for doc in Doctor.objects.all():
                        userPK.append(doc.personID.id)

                elif recipient_filter == 'Admin':
                    # Add to list the patients
                    for pat in Patient.objects.all():
                        userPK.append(pat.personID.id)
                    # Add to list the nurses
                    for nur in Nurse.objects.all():
                        userPK.append(nur.personID.id)
                    # Add to list the doctors
                    for doc in Doctor.objects.all():
                        userPK.append(doc.personID.id)
                    # Add to the list the admins
                    for adm in Admin.objects.all():
                        userPK.append(adm.personID.id)
                    # Add to the list the root
                    for roo in Root.objects.all():
                        userPK.append(roo.personID.id)
                userList = Person.objects.filter(id__in=userPK)
            self.fields['recipient'] = forms.ModelChoiceField(queryset=userList, empty_label="Choose a person")

    def save(self, sender, parent_msg=None):
        recipients = self.cleaned_data['recipient']
        subject = self.cleaned_data['subject']
        body = self.cleaned_data['body']
        message_list = []

        # Create the message
        msg = Message(
            sender=sender,
            recipient=recipients,
            subject=subject,
            body=body,
        )

        if parent_msg is not None:
            msg.parent_msg = parent_msg
            parent_msg.replied_at = timezone.now()
            parent_msg.save()

        msg.save()
        message_list.append(msg)

        if notification:
            if parent_msg is not None:
                notification.send([sender], "messages_replied", {'message': msg, })
                notification.send([recipients], "messages_reply_received", {'message': msg, })
            else:
                notification.send([sender], "messages_sent", {'message': msg, })
                notification.send([recipients], "messages_received", {'message': msg, })
        return message_list
