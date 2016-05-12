from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, redirect
from appointment.views import group_required
from base.models import Person, Patient, MedicalHistory, Nurse, Logger
from .forms import *


# Create your views here.
@login_required
def viewHistory(request, **kwargs):
    if request.user.groups.filter(name='Doctor').exists():
        medical_model = get_object_or_404(MedicalHistory, pk=kwargs.get('pk'))
        #########################################
        # Gather information for report on user #
        #########################################
        patientInfo = Patient.objects.get(medicalID=medical_model)
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
                      + city + ' , ' + state + ' ' + zip

        # Grab the insurance info
        policyNumber = patientInfo.insuranceID.policyNumber
        insuranceName = patientInfo.insuranceID.name

        medical = medical_model

        context = {'patient_model': patientInfo,
                   'medical': medical,
                   'medicalID': patientInfo.medicalID.id,
                   'fullName': fullName,
                   'email': email,
                   'phoneNumber': phoneNumber,
                   'birthday': birthday,
                   'addressInfo': addressInfo,
                   'policyNumber': policyNumber,
                   'insuranceName': insuranceName,
                   'emergencyContact': patientInfo.emergencyContactID,
                   'patientID': person_model.id, }

        return render(request, 'medicalHistory/index.html', context)

    elif request.user.groups.filter(name='Root').exists() or request.user.groups.filter(name='Admin').exists():
        return render(request, 'medicalHistory/wrongHospital.html', {})

    elif request.user.groups.filter(name='Nurse').exists():
        user_model = User.objects.get_by_natural_key(request.user)
        person_model = Person.objects.get(user=user_model)
        nurse_model = Nurse.objects.get(personID=person_model)

        medical_model = get_object_or_404(MedicalHistory, pk=kwargs.get('pk'))
        patientInfo = Patient.objects.get(medicalID=medical_model)
        if patientInfo.hospitalID == nurse_model.hospitalID:
            #########################################
            # Gather information for report on user #
            #########################################
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
                          + city + ' , ' + state + ' ' + zip

            # Grab the insurance info
            policyNumber = patientInfo.insuranceID.policyNumber
            insuranceName = patientInfo.insuranceID.name

            medical = medical_model

            context = {'patient_model': patientInfo,
                       'medical': medical,
                       'medicalID': patientInfo.medicalID.id,
                       'fullName': fullName,
                       'email': email,
                       'phoneNumber': phoneNumber,
                       'birthday': birthday,
                       'addressInfo': addressInfo,
                       'policyNumber': policyNumber,
                       'insuranceName': insuranceName,
                       'emergencyContact': patientInfo.emergencyContactID,
                       'patientID': person_model.id, }

            return render(request, 'medicalHistory/index.html', context)
        else:
            return render(request, 'medicalHistory/wrongHospital.html', {})

    else:
        medical_model = get_object_or_404(MedicalHistory, pk=kwargs.get('pk'))
        patient_model = Patient.objects.get(medicalID=medical_model)
        if patient_model.medicalID is not None:
            medical = medical_model
            create = False
        else:
            medical = []
            create = True

        context = {'patient_model': patient_model, 'medical': medical,
                   'create': create, 'medicalID': patient_model.medicalID.id}

        return render(request, 'medicalHistory/index.html', context)


@login_required
@group_required('Patient')
def createHistory(request):
    if request.method == 'POST':
        medicalForm = MedicalHistoryForm(request.POST)

        if medicalForm.is_valid():
            med = medicalForm.save()
            currentUser = request.user
            user_model = User.objects.get_by_natural_key(currentUser.username)
            person_model = Person.objects.get(user=user_model)
            patient_model = Patient.objects.get(personID=person_model)
            patient_model.medicalID = med
            patient_model.save()

            create = False
            context = {'create': create, 'medical': med,
                       'medicalID': med.id}

            logPerson = Person.objects.get(user=
                                           User.objects.get_by_natural_key(request.user.username))
            Logger.createLog('Created',logPerson,med,None)

            return render(request, 'medicalHistory/index.html', context)

        else:
            logPerson = Person.objects.get(user=
                                           User.objects.get_by_natural_key(request.user.username))
            Logger.createLog('Standard error',logPerson,medicalForm.errors,None)
            print(medicalForm.errors)
    else:
        medicalForm = MedicalHistoryForm()

    context = {'medicalForm': medicalForm}
    return render(request, 'medicalHistory/create.html', context)


@login_required
@group_required('Patient', 'Doctor')
def update(request, **kwargs):
    medID = kwargs.get('pk')
    medical_model = get_object_or_404(MedicalHistory, pk=medID)
    if request.method == 'POST':
        medicalForm = MedicalHistoryForm(request.POST, instance=medical_model)

        if medicalForm.is_valid():

            patient_model = Patient.objects.get(medicalID=medID)
            med = medicalForm.save()
            patient_model.medicalID = med
            patient_model.save()

            logPerson = Person.objects.get(user=
                                           User.objects.get_by_natural_key(request.user.username))
            Logger.createLog('Updated',logPerson,med,None)
            return redirect(reverse('medical:history', kwargs={'pk': medID}))

        else:
            Logger.createLog('Standard error',logPerson,medicalForm.errors,None)
            print(medicalForm.errors)
    else:
        # Grab the char fields
        histSystems = medical_model.histSystems
        histSystemsOther = medical_model.histSystemsOther
        histSurgeryOther = medical_model.histSurgeryOther
        histAllergyOther = medical_model.histAllergyOther
        histAllergyFoodOther = medical_model.histAllergyFoodOther
        histMedicationOther = medical_model.histMedicationOther
        histTobaccoOther = medical_model.histTobaccoOther
        histTobaccoFrequency = medical_model.histTobaccoFrequency
        histTobaccoDuration = medical_model.histTobaccoDuration
        histAlcoholBeer = medical_model.histAlcoholBeer
        histAlcoholShots = medical_model.histAlcoholShots
        histDrugOther = medical_model.histDrugOther
        histFamilyOther = medical_model.histFamilyOther
        histWorkExplain = medical_model.histWorkExplain
        histPrimaryName = medical_model.histPrimaryName
        histPrimaryNumber = medical_model.histPrimaryNumber
        medicalForm = MedicalHistoryForm(instance=medical_model)

        charList = {'histPrimaryNumber': histPrimaryNumber, 'histPrimaryName': histPrimaryName,

                    'histSystems': histSystems, 'histSystemsOther': histSystemsOther,
                    'histAllergyOther': histAllergyOther, 'histAllergyFoodOther': histAllergyFoodOther,
                    'histSurgeryOther': histSurgeryOther, 'histMedicationOther': histMedicationOther,
                    'histTobaccoFrequency': histTobaccoFrequency, 'histTobaccoDuration': histTobaccoDuration,
                    'histAlcoholBeer': histAlcoholBeer, 'histAlcoholShots': histAlcoholShots,
                    'histTobaccoOther': histTobaccoOther, 'histDrugOther': histDrugOther,
                    'histFamilyOther': histFamilyOther, 'histWorkExplain': histWorkExplain, }

    context = {'medicalForm': medicalForm, 'medicalID': medID, }
    context.update(charList)
    return render(request, 'medicalHistory/update.html', context)
