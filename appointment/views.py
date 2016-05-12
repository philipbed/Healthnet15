"""
    Application: HealthNet
    File: appointment/views.py
    Authors:
        - Nathan Stevens
        - Phillip Bedward
        - Daniel Herzig
        - George Herde
        - Samuel Launt

    Description:
        - This file contains all the view for the appointment functionality
"""
from .forms import *
from json import *
from base.views import group_required
from base.models import Person, Patient, Appointment, Doctor, Nurse, Admin
from datetime import datetime
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.safestring import SafeString


# Create your views here.
def redirectAppointment(request):
    return redirect(reverse('appointment:view'), permanent=True)


@login_required
def scheduleAppointment(request, **kwargs):
    """
    @function: scheduleAppointment
    @description: This function handles a request for scheduling an Appointment.
                  Requires that an appointment does not already exist at the same
                  time for the registering Patient and Doctor.
    """
    # Boolean for successful schedule
    appointment_success = False
    existingAppointment = False
    docApptConflict = False
    patApptConflict = False
    if request.method == 'POST':
        appointmentForm = AppointmentForm(request.POST)

        if (appointmentForm.is_valid()):
            doc = appointmentForm.cleaned_data['docList']
            date = appointmentForm.cleaned_data['date_field']
            time = appointmentForm.cleaned_data['time']
            reason = appointmentForm.cleaned_data['reason']

            user = User.objects.get(username=request.user.username)
            p = Person.objects.get(user=user)
            pat = Patient.objects.get(personID=p)

            """
               Checking to make sure that the Appointment doesn't conflict for the Doctor and
               Patient
            """
            appointmentExists = Appointment.objects.filter(doctorID=doc, patientID=pat,
                                                           aptDate=date, aptTime=time, reason=reason).exists()

            docConflictExists = Appointment.objects.filter(doctorID=doc,
                                                           aptDate=date, aptTime=time, reason=reason).exists()

            patConflictExists = Appointment.objects.filter(patientID=pat,
                                                           aptDate=date, aptTime=time, reason=reason).exists()

            # If appointment makes it through conditionals, appointment_success is true
            if appointmentExists:
                existingAppointment = True
            elif docConflictExists:
                docApptConflict = True
            elif patConflictExists:
                patApptConflict = True
            else:
                appointment_success = True
                # Adds the user as a member of the hospital group
                if not user.groups.filter(name=str(doc.hospitalID)).exists():
                    Group.objects.get(name=str(doc.hospitalID)).user_set.add(user)
                Appointment.objects.create(doctorID=doc, patientID=pat, aptDate=date, aptTime=time, reason=reason)

                # Todo put in logger object create statement
                # No redirect because success message built into HTML
        else:
            pass
    else:
        appointmentForm = AppointmentForm()

    context = {'appointmentForm': appointmentForm,
               'docConflict': docApptConflict,
               'patConflict': patApptConflict,
               'apptConflict': existingAppointment,
               'appointment_success': appointment_success,
               'patient': True,
               }
    return render(request, 'appointment/schedule.html', context)


@login_required
def scheduleDoctor(request, patient=None, **kwargs):
    """
    @function: scheduleAppointment
    @description: This function handles a request for scheduling an Appointment.
                  Requires that an appointment does not already exist at the same
                  time for the registering Patient and Doctor.
    """
    # Boolean for successful schedule
    appointment_success = False
    existingAppointment = False
    docApptConflict = False
    patApptConflict = False

    if request.method == 'POST':
        appointmentForm = AppointmentDoctorForm(request.POST)


        # Get the valid data from the form
        if (appointmentForm.is_valid()):
            pat = appointmentForm.cleaned_data['patList']
            date = appointmentForm.cleaned_data['date_field']
            time = appointmentForm.cleaned_data['time']
            reason = appointmentForm.cleaned_data['reason']

            user = User.objects.get(username=request.user.username)
            d = Person.objects.get(user=user)
            doc = Doctor.objects.get(personID=d)

            """
               Checking to make sure that the Appointment doesn't conflict for the Doctor and
               Patient
            """
            # This searches for clone appointments
            appointmentExists = Appointment.objects.filter(doctorID=doc, patientID=pat,
                                                           aptDate=date, aptTime=time, reason=reason).exists()

            # This searches for appointments with the doctor at the same time
            docConflictExists = Appointment.objects.filter(doctorID=doc,
                                                           aptDate=date, aptTime=time, reason=reason).exists()

            # This searches for appointments with the patient at the same time
            patConflictExists = Appointment.objects.filter(patientID=pat,
                                                           aptDate=date, aptTime=time, reason=reason).exists()

            # If appointment makes it through conditionals, appointment_success is true
            if appointmentExists:
                existingAppointment = True
            elif docConflictExists:
                docApptConflict = True
            elif patConflictExists:
                patApptConflict = True
            else:
                appointment_success = True
                Appointment.objects.create(doctorID=doc, patientID=pat, aptDate=date, aptTime=time, reason=reason)
                # No redirect because success message built into HTML
        else:
            pass

    else:
        appointmentForm = AppointmentDoctorForm()
        # If there is a patient passed in
        if patient is not None:
            appointmentForm.fields['patList'].initial = patient

    context = {'appointmentForm': appointmentForm,
               'docConflict': docApptConflict,
               'patConflict': patApptConflict,
               'apptConflict': existingAppointment,
               'appointment_success': appointment_success,
               'doctor': True, }
    return render(request, 'appointment/schedule.html', context)


@login_required
def scheduleNurse(request, patient=None, **kwargs):
    """
    @function: scheduleAppointment
    @description: This function handles a request for scheduling an Appointment.
                  Requires that an appointment does not already exist at the same
                  time for the registering Patient and Doctor.
    """
    user = User.objects.get(username=request.user.username)
    n = Person.objects.get(user=user)
    nurseUser = Nurse.objects.get(personID=n)

    # Boolean for successful schedule
    appointment_success = False
    existingAppointment = False
    docApptConflict = False
    patApptConflict = False

    if request.method == 'POST':
        appointmentForm = AppointmentNurseForm(request.POST, nurHospital=nurseUser.hospitalID)

        # Get the valid data from the form
        if (appointmentForm.is_valid()):
            pat = appointmentForm.cleaned_data['patList']
            doc = appointmentForm.cleaned_data['docList']
            date = appointmentForm.cleaned_data['date_field']
            time = appointmentForm.cleaned_data['time']
            reason = appointmentForm.cleaned_data['reason']

            """
               Checking to make sure that the Appointment doesn't conflict for the Doctor and
               Patient
            """
            # This searches for clone appointments
            appointmentExists = Appointment.objects.filter(doctorID=doc, patientID=pat,
                                                           aptDate=date, aptTime=time, reason=reason).exists()

            # This searches for appointments with the doctor at the same time
            docConflictExists = Appointment.objects.filter(doctorID=doc,
                                                           aptDate=date, aptTime=time, reason=reason).exists()

            # This searches for appointments with the patient at the same time
            patConflictExists = Appointment.objects.filter(patientID=pat,
                                                           aptDate=date, aptTime=time, reason=reason).exists()

            # If appointment makes it through conditionals, appointment_success is true
            if appointmentExists:
                existingAppointment = True
            elif docConflictExists:
                docApptConflict = True
            elif patConflictExists:
                patApptConflict = True
            else:

                appointment_success = True
                Appointment.objects.create(doctorID=doc, patientID=pat, aptDate=date, aptTime=time, reason=reason)
                # No redirect because success message built into HTML
        else:
            pass

    else:
        appointmentForm = AppointmentNurseForm(nurHospital=nurseUser.hospitalID)
        # If there is a patient passed in
        if patient is not None:
            appointmentForm.fields['patList'].initial = patient

    context = {'appointmentForm': appointmentForm,
               'docConflict': docApptConflict,
               'patConflict': patApptConflict,
               'apptConflict': existingAppointment,
               'appointment_success': appointment_success,
               'nurse': True, }
    return render(request, 'appointment/schedule.html', context)


@login_required
def viewAppointment(request, **kwargs):
    """
    @function: viewAppointment
    @description: Functionality for viewing an appointment
    """
    user_model = User.objects.get_by_natural_key(request.user.username)
    person_model = Person.objects.get(user=user_model)

    if Patient.objects.filter(personID=person_model).exists():
        patient_model = Patient.objects.get(personID=person_model)

        # Grab the appts
        appts = Appointment.objects.all().filter(patientID=patient_model.id,
                                                 aptDate__gte=datetime.today()).order_by('aptDate', 'aptTime')

        context = {'appointments': appts, 'cal': populateCalendar(request)}
        return render(request, 'appointment/viewAppointments.html', context)

    elif Doctor.objects.filter(personID=person_model).exists():
        doctor_model = Doctor.objects.get(personID=person_model)

        # Grab the appts
        appts = Appointment.objects.all().filter(doctorID=doctor_model.id,
                                                 aptDate__gte=datetime.today()).order_by('aptDate', 'aptTime')

        context = {'appointments': appts, 'cal': populateCalendar(request)}
        return render(request, 'appointment/viewAppointments.html', context)

    elif Nurse.objects.filter(personID=person_model).exists():
        nurseModel = Nurse.objects.get(personID=person_model)
        appts, nurseCal = nurseCalendar(nurseModel)
        context = {'appointments': appts, 'cal': nurseCal, 'employeeModel': nurseModel}
        return render(request, 'appointment/viewAppointments.html', context)

    elif Admin.objects.filter(personID=person_model).exists():
        adminModel = Admin.objects.get(personID=person_model)
        appts, nurseCal = nurseCalendar(adminModel)
        context = {'appointments': appts, 'cal': nurseCal, 'employeeModel': adminModel}
        return render(request, 'appointment/viewAppointments.html', context)

    else:
        return render(request, 'appointment/viewAppointments.html', {})


def nurseViewAppointments(request, **kwargs):
    """
    @function: viewAppointment
    @description: Functionality for viewing an appointment
    """
    current_user = request.user
    personID = kwargs.get('personID')
    if current_user.is_authenticated():
        user_model = User.objects.get_by_natural_key(current_user.username)
        person_model = Person.objects.get(user=user_model)
        nurseModel = Patient.objects.get(personID=person_model)

        # Grab the appts
        appts, nurseCal = nurseCalendar(request)

        context = {'appointments': appts, 'cal': nurseCal}
        return render(request, 'appointment/viewAppointments.html', context)

    else:
        return render(request, 'appointment/viewAppointments.html', {})


@login_required
def updateAppointment(request, **kwargs):
    """
    @function: updateAppointment
    @description: updates an appointment, and pre-fills the Time, Date, and Reason fields
    """
    appID = kwargs.get('pk')
    appointment_model = Appointment.objects.get(id=appID)
    if request.method == 'POST':
        updateAppt = UpdateAppointmentForm(request.POST, instance=appointment_model)

        if updateAppt.is_valid():
            doc = updateAppt.cleaned_data['docList']
            date = updateAppt.cleaned_data['date_field']
            time = updateAppt.cleaned_data['time']
            reason = updateAppt.cleaned_data['reason']

            appointment_model.doctorID = doc
            appointment_model.aptDate = date
            appointment_model.aptTime = time
            appointment_model.reason = reason
            appointment_model.save()
            return HttpResponseRedirect(reverse('appointment:view'))

        else:
            print(updateAppt.errors)


    else:
        updateAppt = UpdateAppointmentForm(instance=appointment_model)

    dateStr = getDateAsString(appointment_model.aptDate)
    timeStr = str(appointment_model.aptTime)
    reasonStr = str(appointment_model.reason)
    context = {'form': updateAppt,
               'appointmentID': appID,
               'date': dateStr,
               'time': timeStr,
               'reason': reasonStr
               }

    return render(request, 'appointment/appointment_form.html', context)


@login_required
@group_required('Patient', 'Doctor', 'Admin', 'Root')
def deleteAppointment(request, **kwargs):
    """
    @function: deleteAppointment
    @description: Removes/Cancels an appointment for a user
    """
    appID = kwargs.get('pk')
    appointment_model = get_object_or_404(Appointment, id=appID)
    if request.method == 'POST':
        form = DeleteAppointment(request.POST, instance=appointment_model)
        if form.is_valid():
            appointment_model.delete()
            return HttpResponseRedirect(reverse('appointment:view'))
    else:
        form = DeleteAppointment(instance=appointment_model)
        template_vars = {'form': form,
                         'appointmentID': appID,
                         'appointment': appointment_model,
                         }
    return render(request, 'appointment/deleteAppointment.html', template_vars)


def populateCalendar(request):
    """
    @function: populateCalendar
    @description: Fills the calendar with the appointments for an
                  individual (depends on type of user)
    """
    currentUser = request.user
    usr = User.objects.get(username=currentUser.username)
    personObj = Person.objects.get(user=usr)
    events = []
    docExists = Doctor.objects.filter(personID=personObj).exists()
    patientExists = Patient.objects.filter(personID=personObj.id).exists()

    # if the doctor exists then the viewer is a doctor
    if docExists:
        viewer = Doctor.objects.get(personID=personObj)
        appointmentExists = Appointment.objects.filter(doctorID=viewer.id).exists()
        if appointmentExists:
            appointmentSet = Appointment.objects.filter(doctorID=viewer.id, aptDate__gte=datetime.today())
            for appt in appointmentSet:
                event = {}
                event['title'] = "Patient: " + appt.patientID.__str__()
                startString = datetime.combine(appt.aptDate, appt.aptTime).strftime('%Y-%m-%dT%X')
                event["start"] = startString
                event[
                    "description"] = "You have an appointment with <b> Dr. " + appt.doctorID.__str__() + " </b> at <b>" \
                                     + appt.aptTime.strftime('%I') + "</b> on <b> " + appt.aptDate.strftime(
                    '%x') + "</b> for the following reason: <br><em>" \
                                     + appt.reason + "</em>"
                event["allDay"] = False
                events.append(event)
            events = dumps(events)

    elif patientExists:
        viewer = Patient.objects.get(personID=personObj)
        appointmentExists = Appointment.objects.filter(patientID=viewer.id).exists()
        if appointmentExists:
            appointmentSet = Appointment.objects.filter(patientID=viewer.id, aptDate__gte=datetime.today())
            for appt in appointmentSet:
                event = {}
                event['title'] = appt.doctorID.__str__()
                startString = datetime.combine(appt.aptDate, appt.aptTime).strftime('%Y-%m-%dT%X')
                event["start"] = startString
                event[
                    "description"] = "You have an appointment with <b> Dr. " + appt.doctorID.__str__() + " </b> at <b>" \
                                     + appt.aptTime.strftime('%I') + "</b> on <b> " + appt.aptDate.strftime(
                    '%x') + "</b> for the following reason: <br><em>" \
                                     + appt.reason + "</em>"
                event["allDay"] = False
                events.append(event)
            events = dumps(events)

    return SafeString(events)


def nurseCalendar(nurse):
    allAppointments = Appointment.objects.filter(aptDate__gte=datetime.today())

    nursesAppts = []
    events = []

    # if the appointment is in the same hospital as the nurse
    # then add it to the list of nurse's appointments
    for appt in allAppointments:

        if ((appt.doctorID.hospitalID.id == nurse.hospitalID.id)):
            # This second confirmation doesn't work yet, because patient isn't added
            # to hospital records yet
            # and (appt.patientID.hospitalID == nurse.hospitalID)):
            nursesAppts.append(appt)

    # add the events to a hashmap then add each hashmap to a list
    # so it can be json dumped for use by the calendar
    for appt in nursesAppts:
        event = {}
        event['title'] = appt.doctorID.__str__()
        startString = datetime.combine(appt.aptDate, appt.aptTime).strftime('%Y-%m-%dT%X')
        event["start"] = startString
        event["description"] = appt.patientID.__str__() + " has an appointment with <b> Dr. " \
                               + appt.doctorID.__str__() + " </b> at <b>" + appt.aptTime.strftime('%I') + "</b> on <b> " \
                               + appt.aptDate.strftime('%x') + "</b> for the following reason: <br><em>" \
                               + appt.reason + "</em>"
        events.append(event)
    events = dumps(events)

    return nursesAppts, SafeString(events)


def getDateAsString(date):
    strDate = str(datetime.strftime(date, '%m/%d/%Y'))
    return strDate
