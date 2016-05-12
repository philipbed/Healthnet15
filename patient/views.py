"""
    Application: HealthNet
    File: /patient/views.py
    Authors:
        - Nathan Stevens
        - Philip Bedward
        - Daniel Herzig
        - George Herde
        - Samuel Launt

    Description:
        - This file contains all the views for doctors and nurses to interact
          with patient information
"""
from .forms import *
from base.views import group_required
from base.models import *
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404


# Create your views here.
@login_required
@group_required('Doctor', 'Admin', 'Root', 'Nurse')
def patientList(request):
    """
    Doctors can view all the patients in the system,
    regardless of hospital.
    """
    patients = gatherPatientList(User.objects.get_by_natural_key(request.user.username)).order_by(
        'personID__user__first_name')
    context = {'patients': patients}

    return render(request, 'patient/patientList.html', context)


def gatherPatientList(requestUser):
    person_model = person.objects.get(user=requestUser)
    if Nurse.objects.filter(personID=person_model).exists():
        nursePerson = Nurse.objects.all().get(personID=person_model)
        # Grab the nurse's hospital ID
        hospital_id = nursePerson.hospitalID
        # Grab patients with that hospital ID
        admittedPatients = Patient.objects.all().filter(hospitalID=hospital_id)

        hospitalUsers = Group.objects.get(name=str(hospital_id)).user_set.all()
        personPKList = []
        for user in hospitalUsers:
            personPKList.append(Patient.objects.get(personID=Person.objects.get(user=user)).id)
        patientList = Patient.objects.filter(id__in=personPKList)

        patients = admittedPatients | patientList

    elif Admin.objects.filter(personID=person_model).exists():
        adminPerson = Admin.objects.all().get(personID=person_model)
        hospital_id = adminPerson.hospitalID
        admittedPatients = Patient.objects.all().filter(hospitalID=hospital_id)

        hospitalUsers = Group.objects.get(name=str(hospital_id)).user_set.all()
        personPKList = []
        for user in hospitalUsers:
            personPKList.append(Patient.objects.get(personID=Person.objects.get(user=user)).id)
        patientList = Patient.objects.filter(id__in=personPKList)

        patients = admittedPatients | patientList

    elif Doctor.objects.filter(personID=person_model).exists():
        patients = Patient.objects.all()

    elif Root.objects.filter(personID=person_model).exists():
        patients = Patient.objects.all()

    else:
        patients = []
    return patients


@login_required
@group_required('Nurse', 'Doctor')
def viewPatientDetails(request, **kwargs):
    patID = kwargs.get('pk')
    patientInfo = Patient.objects.get(id=patID)
    ##################
    # Gather information for report on user
    ##################
    person_model = Person.objects.get(id=patientInfo.personID.id)
    user_model = User.objects.get_by_natural_key(person_model.user)
    # Grab the user information forms
    firstName = user_model.first_name
    lastName = user_model.last_name
    # Add the names together
    fullName = firstName + ' ' + lastName
    email = user_model.email

    # Grab the person identified with patient
    phoneNumber = person_model.phoneNumber
    birthday = person_model.birthday

    # Grab the address
    street = patientInfo.addressID.street
    city = patientInfo.addressID.city
    state = patientInfo.addressID.state
    zip = str(patientInfo.addressID.zip)
    # Add all the info together
    addressInfo = street + ' \n' \
                  + city + ', ' + state + ' ' + zip

    # Grab the insurance info
    policyNumber = patientInfo.insuranceID.policyNumber
    insuranceName = patientInfo.insuranceID.name

    # Grab prescription info
    prescriptions = Prescription.objects.all().filter(patientID=patID)

    patients = gatherPatientList(User.objects.get_by_natural_key(request.user.username)).order_by(
        'personID__user__first_name')

    context = {'patient_model': patientInfo,
               'patients': patients,
               'fullName': fullName,
               'email': email,
               'phoneNumber': phoneNumber,
               'birthday': birthday,
               'addressInfo': addressInfo,
               'policyNumber': policyNumber,
               'insuranceName': insuranceName,
               'emergencyContact': patientInfo.emergencyContactID,
               'patientID': person_model.id,
               'prescriptions': prescriptions}
    person = Person.objects.get(user=request.user)      
    docExists = Doctor.objects.filter(personID=person).exists()
    nurseExists = Nurse.objects.filter(personID=person).exists()

    if docExists:
       Logger.createLog('Viewed',person,person_model,Doctor.objects.get(personID=person).hospitalID)
    elif nurseExists:
        Logger.createLog('Viewed',person,person_model,Nurse.objects.get(personID=person).hospitalID)
    return render(request, 'patient/patientListDetails.html', context)



@login_required
@group_required('Doctor', 'Nurse')
def admitPatient(request, pk):
    """
    This function will handle the necessary steps to admit a patient
    to a hospital.

    :param request: dictionary of information sent to the page.
    :param pk: the primary key of an appointment

    :return: renders proper context information to the corresponding html page
    """
    # store data
    apptID = pk
    currUser = request.user
    currAppt = Appointment.objects.get(id=apptID)
    currPatient = currAppt.getPatient()
    personModel = Person.objects.get(user=currUser)
    hospital = currAppt.getHospital()
    if request.method == 'POST':
        form = AdmitPatient(request.POST)

        if form.is_valid():
            # check if a nurse is performing the operation or
            # a doctor

            docExists = Doctor.objects.filter(personID=personModel).exists()
            nurseExists = Nurse.objects.filter(personID=personModel).exists()

            if docExists:
                # set the patients hospital to the doctor's hospital
                docModel = Doctor.objects.get(personID=personModel)
                currPatient.hospitalID = docModel.hospitalID
                currPatient.save()
                Logger.createLog('Admitted',personModel,currPatient.personID,docModel.hospitalID)

            elif nurseExists:
                # set the patients hospital to the nurse's hospital
                nurseModel = Nurse.objects.get(personID=personModel)
                currPatient.hospitalID = nurseModel.hospitalID
                currPatient.save()
                Logger.createLog('Admitted',Nurse.objects.get(personID=personModel),currPatient.personID,nurseModel.hospitalID)

            # set the appointment that this ExtendedStay has
            exStay = form.save(commit=False)
            exStay.appointmentID = currAppt
            exStay.save()

            # return to the appointments page upon success
            
            return HttpResponseRedirect(reverse('appointment:view'))
        else:
            print(form.errors)
    else:
        form = AdmitPatient()

        context = {'apptID': apptID, 'patient': currPatient,
                   'form': form, 'hospital': hospital, 'currAppt': currAppt}
        return render(request, 'patient/admitPatient.html', context)



@login_required
@group_required('Doctor')
def dischargePatient(request, pk):
    """
    performs the necessary operations in order to discharge a patient from a hospital

    :param request: dictionary of information sent to the page.
    :param pk: the primary key of an ExtendedStay object

    :return: renders proper context information to the corresponding html page
    """

    # store data
    exStayID = pk
    currUser = request.user
    currStay = ExtendedStay.objects.get(id=exStayID)
    currPatient = currStay.getPatient()
    personModel = Person.objects.get(user=currUser)
    hospital = currPatient.hospitalID
    if request.method == 'POST':
        form = DischargePatient(request.POST)

        if form.is_valid():

            # delete the current Extended Stay object
            # set the  hospital of the current patient to None

            currStay.delete()
            currPatient.hospitalID = None
            currPatient.save()
            Logger.createLog('Released',personModel,currPatient.personID,Doctor.objects.get(personID=personModel).hospitalID)
            return HttpResponseRedirect(reverse('patient:admittedPats'))
        else:
            Logger.createLog('Standard error',personModel,form.errors,None)
            print(form.errors)
    else:
        form = DischargePatient()

        context = {'stayID': exStayID, 'patient': currPatient, 'form': form, 'hospital': hospital}
        return render(request, 'patient/discharge.html', context)


@login_required
@group_required('Doctor', 'Nurse')
def admittedPatients(request):
    """
    Grabs all of the patients that have been admitted to a certain hospital

    :param request: dictionary of information sent to the page.
    :return: renders proper context information to the corresponding html page
    """

    # store data
    exStays = ExtendedStay.objects.all()
    currUser = request.user
    personModel = Person.objects.get(user=currUser)

    docExists = Doctor.objects.filter(personID=personModel).exists()
    nurseExists = Nurse.objects.filter(personID=personModel).exists()
    filteredStays = []
    hospital = None
    if docExists:
        docModel = Doctor.objects.get(personID=personModel)
        hospital = docModel.hospitalID

        # goes through each of the ExtendedStay objects and only returns the ones
        # that have a patient that has a hospital that matches the doctor's
        filteredStays = getFilteredStays(exStays, docModel)

    elif nurseExists:
        nurseModel = Nurse.objects.get(personID=personModel)
        hospital = nurseModel.hospitalID

        # goes through each of the ExtendedStay objects and only returns the ones
        # that have a patient that has a hospital that matches the doctor'
        filteredStays = getFilteredStays(exStays, nurseModel)
        # filteredStays = list( filter( lambda x: x.getPatient().hospitalID == nurseModel.hospitalID, exStays ) )

    return render(request, 'patient/admittedPatients.html', {'extendedStays': filteredStays, 'hospital': hospital})


@login_required
@group_required('Doctor', 'Admin')
def transferPatient(request, patID):
    currPatient = Patient.objects.get(id=patID)
    hospital = currPatient.hospitalID
    currUser = request.user
    personModel = Person.objects.get(user=currUser)

    othHospital = None
    docExists = Doctor.objects.filter(personID=personModel).exists()
    if docExists:
        othHospital = Doctor.objects.get(personID=personModel).hospitalID
    nurseExists = Nurse.objects.filter(personID=personModel).exists()
    if nurseExists:
        othHospital = Nurse.objects.get(personID=personModel).hospitalID

    # Get your current hospital

    if request.method == 'POST':

        form = TransferPatientForm(request.POST)
        if form.is_valid():
            canTransfer = True
            if docExists:
                docModel = Doctor.objects.get(personID=personModel)
                if currPatient.hospitalID != docModel.hospitalID:
                    # if currPatient.hospitalID == None:
                    #     canTransfer = False
                    #     return render(request,'patient/patientListDetails.html',{'canTransfer':canTransfer})
                    currPatient.hospitalID = docModel.hospitalID
                    currPatient.save()
                    Logger.createLog('Transferred',personModel,currPatient.personID,hospital,othHospital)
                else:
                    return render(request, 'patient/alreadyAdmitted.html',
                                  {'hospital': hospital, 'patID': currPatient.id})

                    # filterededStays = getFilteredStays(exStays, docModel)

            elif nurseExists:
                nurseModel = Nurse.objects.get(personID=personModel)
                if currPatient.hospitalID != nurseModel.hospitalID:
                    # if currPatient.hospitalID == None:
                    #     canTransfer = False
                    #     return render(request,'patient/patientListDetails.html',{'canTransfer':canTransfer})
                    currPatient.hospitalID = nurseModel.hospitalID
                    currPatient.save()
                    Logger.createLog('Transferred',personModel,currPatient.personID,hospital,othHospital)
                else:
                    return render(request, 'patient/alreadyAdmitted.html',
                                  {'hospital': hospital, 'patID': currPatient.id})
                    # filterededStays = getFilteredStays(exStays, nurseModel)
            return HttpResponseRedirect(reverse('patient:patientDetails', kwargs={'pk': patID}))
        else:
            Logger.createLog('Standard error',personModel,form.errors,None)
            print(form.errors)
    else:
        form = TransferPatientForm()
        return render(request, 'patient/transferConfirmation.html',
                      {'form': form, 'patient': currPatient, 
                      'patID': currPatient.id, 'hospital': hospital,
                      'othHospital': othHospital})


@login_required
@group_required('Doctor','Admin')
def transferFailed(request, pk):
    patientModel = get_object_or_404(Patient, id=pk)
    return render(request, 'patient/cannotTransfer.html', {'patient': patientModel})


def getFilteredStays(extendedStays, personnel):
    return list(filter(lambda x: x.getPatient().hospitalID == personnel.hospitalID, extendedStays))
