"""
    Application: HealthNet
    File: /patientUpdate/views.py
    Authors:
        - Nathan Stevens
        - Phillip Bedward
        - Daniel Herzig
        - George Herde
        - Samuel Launt

    Description:
        - This file contains all the forms for updating a Patient's profile
"""
import logging
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response
from django.apps import apps
from django.core.urlresolvers import reverse
from django.template import RequestContext
from base.models import Doctor, Nurse, Admin, Person, Patient, Root, Insurance, Address, Logger, Appointment, Message, inbox_count_for
# from base.models import *
from base.views import group_required
from .forms import *


Cperson = apps.get_model("base", "Person")
doctor = apps.get_model("base", "Doctor")
nurse_model = apps.get_model("base", "Nurse")
admin = apps.get_model("base", "Admin")
root = apps.get_model('base', 'Root')
Cpatient = apps.get_model("base", "Patient")
Caddress = apps.get_model("base", "Address")
Cinsurance = apps.get_model("base", "Insurance")
Cemergencycontact = apps.get_model("base", "EmergencyContact")


# Create your views here.
def userLogin(request):
    """
    @function: userLogin
    @description: This controller definition controls the functionality for
                  when a user logs in.
    """
    # The user is attempting to login, so create a context variable
    loginAttempt = True

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
        # because the request.POST.get('<variable>') returns None, if the value does not exist,
        # while the request.POST['<variable>'] will raise key error exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)

                # Logger.createLog('Logged in',user.personID)
                return HttpResponseRedirect(reverse('profile:userLogin'))
            else:
                disabledAccount = True
                context = {'disabledAccount': disabledAccount,
                           'loginAttempt': loginAttempt}
                # An inactive account was used - no logging in!
                return render(request, 'userprofile/login.html', context)
        else:
            failedLogin = True
            loginAttempt = True
            # Redefine the context variable to include the failedLogin variable
            context = {'failedLogin': failedLogin,
                       'loginAttempt': loginAttempt}
            # Bad login details were provided. So we can't log the user in.
            return render(request, "userprofile/login.html", context)

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        currentUser = request.user.id
        personBool = Person.objects.filter(user=currentUser).exists()
        if personBool:
          person_model = Person.objects.get(user=currentUser)

          if Doctor.objects.filter(personID=person_model).exists():
            doctor_model = Doctor.objects.get(personID=person_model.id)
            appointments = Appointment.objects.all().filter(doctorID=doctor_model, aptDate__gte=datetime.today())[:3]
            messageCount = inbox_count_for(currentUser)
            messages = Message.objects.inbox_for(person_model)[:3]
            context = {'appointments': appointments, 'loginAttempt': loginAttempt, 'messageCount': messageCount,
            'messages': messages}
            return render(request, 'userprofile/login.html', context)

          elif Patient.objects.filter(personID=person_model).exists():
            patient_model = Patient.objects.get(personID=person_model.id)     
            appointments = Appointment.objects.all().filter(patientID=patient_model, aptDate__gte=datetime.today())[:3]
            messageCount = inbox_count_for(currentUser)
            messages = Message.objects.inbox_for(person_model)[:3]
            context = {'appointments': appointments, 'loginAttempt': loginAttempt, 'messageCount': messageCount,
            'messages': messages}
            return render(request, 'userprofile/login.html', context)

          elif Nurse.objects.filter(personID=person_model).exists():
            nurse_model = Nurse.objects.get(personID=person_model.id)
            allAppointments = Appointment.objects.filter(aptDate__gte=datetime.today())
            appointments = []
            for appt in allAppointments:
              if ((appt.doctorID.hospitalID.id == nurse_model.hospitalID.id)):
                appointments.append(appt)
            messageCount = inbox_count_for(currentUser)
            messages = Message.objects.inbox_for(person_model)[:3]
            context = {'appointments': appointments, 'loginAttempt': loginAttempt, 'messageCount': messageCount,
            'messages': messages}
            return render(request, 'userprofile/login.html', context)
          else:
            return render(request, 'userprofile/login.html', {'loginAttempt': loginAttempt})
        else:
            return render(request, 'userprofile/login.html', {'loginAttempt': loginAttempt})




@login_required
def userLogout(request):
    """
    @function: userLogout
    @description: This controller definition controls the functionality for
                  when a user logs out.
    """
    currentUser = request.user
    request.session.items = []
    request.session.modified = True
    logout(request)
    logoutAttempt = True
    return render(request, 'userprofile/logout.html', {'logoutAttempt': logoutAttempt})


@login_required
def viewProfile(request, **kwargs):
    """
    @function: viewProfile
    @description: viewProfile lets the user view their current settings and profile information.
    """
    currentUser = request.user
    user_model = User.objects.get_by_natural_key(currentUser.username)
    # Grab the user information forms
    firstName = user_model.first_name
    lastName = user_model.last_name
    # Add the names together
    fullName = firstName + ' ' + lastName
    email = user_model.email

    # Get the doctor's models
    person_model = Person.objects.get(user=user_model)

    if request.user.groups.filter(name='Patient').exists():
        patientInfo = Cpatient.objects.get(personID=person_model)
        # Grab the person identified with patient
        phoneNumber = patientInfo.personID.phoneNumber
        birthday = patientInfo.personID.birthday

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

        if patientInfo.medicalID == None:
            medicalID = -1
        else:
            medicalID = patientInfo.medicalID.id

        context = {'fullName': fullName,
                   'email': email,
                   'phoneNumber': phoneNumber,
                   'birthday': birthday,
                   'addressInfo': addressInfo,
                   'policyNumber': policyNumber,
                   'insuranceName': insuranceName,
                   'emergencyContact': patientInfo.emergencyContactID,
                   'patientID': person_model.id,
                   'medicalID': medicalID,
                   'patient':Cpatient.objects.get(personID=person_model)}
        return render(request, 'userprofile/profile.html', context)

    elif request.user.groups.filter(name='Doctor').exists():
        doctorInfo = doctor.objects.get(personID=person_model)

        phoneNumber = doctorInfo.personID.phoneNumber
        birthday = doctorInfo.personID.birthday
        # Grab the address
        street = doctorInfo.addressID.street
        city = doctorInfo.addressID.city
        state = doctorInfo.addressID.state
        zip = str(doctorInfo.addressID.zip)
        # Add all the info together
        addressInfo = street + ' \n' \
                      + city + ' , ' + state + ' ' + zip

        hospitalName = doctorInfo.hospitalID.name
        hospitalAddress = doctorInfo.hospitalID.address

        licenseNumber = doctorInfo.licenseNumber
        specialty = doctorInfo.specialty

        context = {'fullName': fullName,
                   'email': email,
                   'phoneNumber': phoneNumber,
                   'birthday': birthday,
                   'addressInfo': addressInfo,
                   'personID': doctorInfo.id,
                   'hospitalName': hospitalName,
                   'hospitalAddress': hospitalAddress,
                   'specialty': specialty,
                   'licenseNumber': licenseNumber,
                   }
        return render(request, 'userprofile/profile.html', context)

    elif request.user.groups.filter(name='Nurse').exists():
        nurseInfo = nurse.objects.get(personID=person_model)

        phoneNumber = nurseInfo.personID.phoneNumber
        birthday = nurseInfo.personID.birthday
        # Grab the address
        street = nurseInfo.addressID.street
        city = nurseInfo.addressID.city
        state = nurseInfo.addressID.state
        zip = str(nurseInfo.addressID.zip)
        # Add all the info together
        addressInfo = street + ' \n' \
                      + city + ' , ' + state + ' ' + zip

        hospitalName = nurseInfo.hospitalID.name
        hospitalAddress = nurseInfo.hospitalID.address

        licenseNumber = nurseInfo.license_number
        department = nurseInfo.department

        context = {'fullName': fullName,
                   'email': email,
                   'phoneNumber': phoneNumber,
                   'birthday': birthday,
                   'addressInfo': addressInfo,
                   'personID': nurseInfo.id,
                   'hospitalName': hospitalName,
                   'hospitalAddress': hospitalAddress,
                   'department': department,
                   'licenseNumber': licenseNumber,
                   }
        return render(request, 'userprofile/profile.html', context)

    elif request.user.groups.filter(name='Admin').exists():
        adminInfo = admin.objects.get(personID=person_model)

        phoneNumber = adminInfo.personID.phoneNumber
        birthday = adminInfo.personID.birthday
        # Grab the address
        street = adminInfo.addressID.street
        city = adminInfo.addressID.city
        state = adminInfo.addressID.state
        zip = str(adminInfo.addressID.zip)
        # Add all the info together
        addressInfo = street + ' \n' \
                      + city + ' , ' + state + ' ' + zip

        hospitalName = adminInfo.hospitalID.name
        hospitalAddress = adminInfo.hospitalID.address

        context = {'fullName': fullName,
                   'email': email,
                   'phoneNumber': phoneNumber,
                   'birthday': birthday,
                   'addressInfo': addressInfo,
                   'personID': adminInfo.id,
                   'hospitalName': hospitalName,
                   'hospitalAddress': hospitalAddress}
        return render(request, 'userprofile/profile.html', context)

    elif request.user.groups.filter(name='Root').exists():
        rootInfo = root.objects.get(personID=person_model)

        phoneNumber = rootInfo.personID.phoneNumber
        birthday = rootInfo.personID.birthday
        context = {'fullName': fullName,
                   'email': email,
                   'phoneNumber': phoneNumber,
                   'birthday': birthday,
                   'personID': rootInfo.id}
        return render(request, 'userprofile/profile.html', context)


@login_required
@group_required('Admin', 'Root')
def AdminView(request, **kwargs):
    """
    @function: viewProfile
    @description: viewProfile lets the user view their current settings and profile information.
    """
    personID = kwargs.get('pk')
    person_model = Person.objects.get(id=personID)
    user_model = User.objects.get_by_natural_key(person_model.user.username)
    # Grab the user information forms
    firstName = user_model.first_name
    lastName = user_model.last_name
    # Add the names together
    fullName = firstName + ' ' + lastName
    email = user_model.email

    if user_model.groups.filter(name='Patient').exists():
        patientInfo = Patient.objects.get(personID=person_model)
        # Grab the person identified with patient
        phoneNumber = patientInfo.personID.phoneNumber
        birthday = patientInfo.personID.birthday

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

        if patientInfo.medicalID == None:
            medicalID = -1
        else:
            medicalID = patientInfo.medicalID.id

        context = {'fullName': fullName,
                   'email': email,
                   'phoneNumber': phoneNumber,
                   'birthday': birthday,
                   'addressInfo': addressInfo,
                   'policyNumber': policyNumber,
                   'insuranceName': insuranceName,
                   'emergencyContact': patientInfo.emergencyContactID,
                   'patientID': person_model.id,
                   'medicalID': medicalID,
                   'patient': True}
        return render(request, 'userprofile/Adminprofile.html', context)

    elif user_model.groups.filter(name='Doctor').exists():
        doctorInfo = Doctor.objects.get(personID=person_model)

        phoneNumber = doctorInfo.personID.phoneNumber
        birthday = doctorInfo.personID.birthday
        # # Grab the address
        # street = patientInfo.addressID.street
        # city = patientInfo.addressID.city
        # state = patientInfo.addressID.state
        # zip = str(patientInfo.addressID.zip)
        # # Add all the info together
        # addressInfo = street + ' \n' \
        #               + city + ' , ' + state + ' ' + zip

        hospitalName = doctorInfo.hospitalID.name
        hospitalAddress = doctorInfo.hospitalID.address

        licenseNumber = doctorInfo.licenseNumber
        specialty = doctorInfo.specialty

        context = {'fullName': fullName,
                   'email': email,
                   'phoneNumber': phoneNumber,
                   'birthday': birthday,
                   # 'addressInfo': addressInfo,
                   'personID': doctorInfo.id,
                   'hospitalName': hospitalName,
                   'hospitalAddress': hospitalAddress,
                   'specialty': specialty,
                   'licenseNumber': licenseNumber,
                   'doctor': True}
        return render(request, 'userprofile/Adminprofile.html', context)

    elif user_model.groups.filter(name='Nurse').exists():
        nurseInfo = Nurse.objects.get(personID=person_model)

        phoneNumber = nurseInfo.personID.phoneNumber
        birthday = nurseInfo.personID.birthday
        # # Grab the address
        # street = patientInfo.addressID.street
        # city = patientInfo.addressID.city
        # state = patientInfo.addressID.state
        # zip = str(patientInfo.addressID.zip)
        # # Add all the info together
        # addressInfo = street + ' \n' \
        #               + city + ' , ' + state + ' ' + zip

        hospitalName = nurseInfo.hospitalID.name
        hospitalAddress = nurseInfo.hospitalID.address

        licenseNumber = nurseInfo.license_number
        department = nurseInfo.department

        context = {'fullName': fullName,
                   'email': email,
                   'phoneNumber': phoneNumber,
                   'birthday': birthday,
                   # 'addressInfo': addressInfo,
                   'personID': nurseInfo.id,
                   'hospitalName': hospitalName,
                   'hospitalAddress': hospitalAddress,
                   'department': department,
                   'licenseNumber': licenseNumber,
                   'nurse': True}
        return render(request, 'userprofile/Adminprofile.html', context)

    elif user_model.groups.filter(name='Admin').exists():
        adminInfo = Admin.objects.get(personID=person_model)

        phoneNumber = adminInfo.personID.phoneNumber
        birthday = adminInfo.personID.birthday
        # # Grab the address
        # street = patientInfo.addressID.street
        # city = patientInfo.addressID.city
        # state = patientInfo.addressID.state
        # zip = str(patientInfo.addressID.zip)
        # # Add all the info together
        # addressInfo = street + ' \n' \
        #               + city + ' , ' + state + ' ' + zip

        hospitalName = adminInfo.hospitalID.name
        hospitalAddress = adminInfo.hospitalID.address

        context = {'fullName': fullName,
                   'email': email,
                   'phoneNumber': phoneNumber,
                   'birthday': birthday,
                   # 'addressInfo': addressInfo,
                   'personID': adminInfo.id,
                   'hospitalName': hospitalName,
                   'hospitalAddress': hospitalAddress,
                   'admin': True}
        return render(request, 'userprofile/Adminprofile.html', context)

    elif user_model.groups.filter(name='Root').exists():
        rootInfo = Root.objects.get(personID=person_model)

        phoneNumber = rootInfo.personID.phoneNumber
        birthday = rootInfo.personID.birthday
        # # Grab the address
        # street = patientInfo.addressID.street
        # city = patientInfo.addressID.city
        # state = patientInfo.addressID.state
        # zip = str(patientInfo.addressID.zip)
        # # Add all the info together
        # addressInfo = street + ' \n' \
        #               + city + ' , ' + state + ' ' + zip

        context = {'fullName': fullName,
                   'email': email,
                   'phoneNumber': phoneNumber,
                   'birthday': birthday,
                   # 'addressInfo': addressInfo,
                   'personID': rootInfo.id,
                   'root': True}
        return render(request, 'userprofile/Adminprofile.html', context)


@login_required
@group_required('Admin', 'Root')
def viewAllPersonnel(request):
    if request.user.groups.filter(name='Root').exists():
        doctors = Doctor.objects.all()
        nurses = Nurse.objects.all()
        administrators = Admin.objects.all()

        context = {'doctors': doctors, 'nurses': nurses, 'admins': administrators}
        return render(request, 'userprofile/viewPersonnel.html', context)

    else:
        user_model = User.objects.get_by_natural_key(request.user.username)
        person_model = Person.objects.get(user=user_model)
        admin_model = Admin.objects.get(personID=person_model)

        doctors = Doctor.objects.all().filter(hospitalID=admin_model.hospitalID)
        nurses = Nurse.objects.all().filter(hospitalID=admin_model.hospitalID)
        administrators = Admin.objects.all().filter(hospitalID=admin_model.hospitalID)

        context = {'doctors': doctors, 'nurses': nurses, 'admins': administrators}

        return render(request, 'userprofile/viewPersonnel.html', context)


@login_required
@group_required('Patient', 'Admin', 'Root')
def updateProf(request, **kwargs):
    """
    @function: updateProf
    @description: Update the changes made a to user profile to the database.
    """
    # Current user
    current_user = request.user
    # Grab all of the model instances necessary
    user_model = User.objects.get_by_natural_key(current_user.username)
    person_model = Person.objects.get(user=user_model)
    patient_model = Patient.objects.get(personID=person_model.id)
    insurance_model = Insurance.objects.get(id=patient_model.insuranceID.id)
    address_model = Address.objects.get(id=patient_model.addressID.id)
    emergency_model = Cemergencycontact.objects.get(id=patient_model.emergencyContactID.id)

    if request.method == 'POST':

        # Create all necessary forms
        userForm = UserForm(request.POST, instance=current_user)
        personForm = PersonRegistrationForm(request.POST, instance=person_model)
        insuranceForm = InsuranceForm(request.POST, instance=insurance_model)
        addressForm = AddressForm(request.POST, instance=address_model)
        emergencyContForm = EmergencyContactForm(request.POST, emergency_model)

        # Validate forms
        if (userForm.is_valid() and personForm.is_valid()) and insuranceForm.is_valid() \
                and (addressForm.is_valid() and emergencyContForm.is_valid()):

            # Save the user form.
            userForm.save()

            birthday = personForm.cleaned_data['birthday']
            phoneNumber = personForm.cleaned_data['phoneNumber']

            # use the user updates to update the person object.
            user_model = User.objects.get(username=current_user.username)
            Cperson.objects.filter(user=current_user).update(user=user_model,
                                                             birthday=birthday,
                                                             phoneNumber=phoneNumber)

            insuranceName = insuranceForm.cleaned_data['name']
            policyNumber = insuranceForm.cleaned_data['policyNumber']

            # update all insurance, address, and emergency contact
            # information if necessary.
            insurance_model.name = insuranceName
            insurance_model.policyNumber = policyNumber
            insurance_model.personID = person_model
            insurance_model.save()

            street = addressForm.cleaned_data['street']
            zipCode = addressForm.cleaned_data['zip']
            city = addressForm.cleaned_data['city']
            state = addressForm.cleaned_data['state']

            address_model.street = street
            address_model.zip = zipCode
            address_model.city = city
            address_model.state = state
            address_model.save()

            emerFirstName = emergencyContForm.cleaned_data['firstName']
            emerLastName = emergencyContForm.cleaned_data['lastName']
            emergencyNumber = emergencyContForm.cleaned_data['emergencyNumber']

            emergency_model.firstName = emerFirstName
            emergency_model.lastName = emerLastName
            emergency_model.emergencyNumber = emergencyNumber
            emergency_model.save()

            # send all updates to the patient
            patient_model.addressID = address_model
            patient_model.insuranceID = insurance_model
            patient_model.personID = person_model

            patient_model.emergencyContactID = emergency_model

            patient_model.save()

            logPerson = Person.objects.get(
                User.objects.get_by_natural_key(request.user.username))
            Logger.createLog('Updated',logPerson,patient_model.personID,None)

            return HttpResponseRedirect(reverse('profile:viewProfile'))
        else:
            print(userForm.errors, personForm.errors, emergencyContForm.errors, addressForm.errors,
                  insuranceForm.errors)

    # Otherwise pre-fill all of the forms
    else:
        userForm = UserForm(instance=current_user)
        personForm = PersonRegistrationForm(instance=person_model)
        insuranceForm = InsuranceForm(instance=insurance_model)
        addressForm = AddressForm(instance=address_model)
        emergencyContForm = EmergencyContactForm(instance=emergency_model)

    context = {'user_form': userForm, 'patientRegistration': personForm,
               'addressForm': addressForm, 'insuranceForm': insuranceForm,
               'emergencyForm': emergencyContForm, 'patientID': patient_model.id}

    # Return all form information to the page
    return render(request, 'userprofile/updateProfile.html', context)


@login_required
@group_required('Doctor', 'Admin', 'Root')
def updateDoctor(request, **kwargs):
    """
    @function: updateProf
    @description: Update the changes made a to user profile to the database.
    """
    docID = kwargs.get('pk')
    # Grab all of the model instances necessary
    doctor_model = Doctor.objects.get(id=docID)
    person_model = Person.objects.get(id=doctor_model.personID.id)
    user_model = User.objects.get_by_natural_key(person_model.user)

    if request.method == 'POST':
        # Create all necessary forms
        userForm = UserForm(request.POST, instance=user_model)
        personForm = PersonRegistrationForm(request.POST, instance=person_model)
        doctorForm = updateDoctorForm(request.POST, instance=doctor_model)

        # addressForm = AddressForm(request.POST)

        # Validate forms
        if (userForm.is_valid() and personForm.is_valid() and doctorForm.is_valid()
            # and addressForm.is_valid()
            ):

            # Save the user form.
            userForm.save()

            # Use the user updates  to update the person object.
            user_model = User.objects.get_by_natural_key(user_model.username)
            birthday = personForm.cleaned_data['birthday']
            phoneNumber = personForm.cleaned_data['phoneNumber']
            Person.objects.filter(user=person_model.user).update(user=user_model,
                                                                 birthday=birthday,
                                                                 phoneNumber=phoneNumber)

            doctor_model.personID = person_model
            doctor_model.save()

            logPerson = Person.objects.get(user=request.user)
            Logger.createLog('Updated',logPerson,person_model,doctor_model.hospitalID)

            currentUser = User.objects.get_by_natural_key(request.user.username)
            if currentUser == user_model:
                return HttpResponseRedirect(reverse('profile:viewProfile'))
            else:
                return HttpResponseRedirect(reverse('profile:viewAllPersonnel'))

        else:
            print(userForm.errors, personForm.errors, doctorForm.errors)

    # Otherwise pre-fill all of the forms
    else:
        userForm = UserForm(instance=user_model)
        personForm = PersonRegistrationForm(instance=person_model)
        doctorForm = updateDoctorForm(instance=doctor_model)

    context = {'user_form': userForm, 'personForm': personForm, 'employeeUpdate': doctorForm,
               'docID': doctor_model.id, 'user': user_model}

    # Return all form information to the page
    return render(request, 'userprofile/updateDoctor.html', context)


@login_required
@group_required('Nurse', 'Admin', 'Root')
def updateNurse(request, **kwargs):
    """
    @function: updateProf
    @description: Update the changes made a to user profile to the database.
    """
    nurID = kwargs.get('pk')
    # Grab all of the model instances necessary
    nurse_model = Nurse.objects.get(id=nurID)
    person_model = Person.objects.get(id=nurse_model.personID.id)
    user_model = User.objects.get_by_natural_key(person_model.user)

    if request.method == 'POST':
        # Create all necessary forms
        userForm = UserForm(request.POST, instance=user_model)
        personForm = PersonRegistrationForm(request.POST, instance=person_model)
        nurseForm = updateNurseForm(request.POST, instance=nurse_model)
        # Validate forms
        if (userForm.is_valid() and personForm.is_valid() and nurseForm.is_valid()
            # and addressForm.is_valid()
            ):

            # Save the user form.
            userForm.save()

            # Use the user updates  to update the person object.
            user_model = User.objects.get_by_natural_key(user_model.username)
            birthday = personForm.cleaned_data['birthday']
            phoneNumber = personForm.cleaned_data['phoneNumber']
            Person.objects.filter(user=person_model.user).update(user=user_model,
                                                                 birthday=birthday,
                                                                 phoneNumber=phoneNumber)

            nurse_model.personID = person_model
            nurse_model.save()

            currentUser = User.objects.get_by_natural_key(request.user.username)
            logPerson = Person.objects.get(user=request.user)
            
            Logger.createLog('Updated',logPerson,person_model,nurse_model.hospitalID)
            if currentUser == user_model:
                return HttpResponseRedirect(reverse('profile:viewProfile'))
            else:
                return HttpResponseRedirect(reverse('profile:viewAllPersonnel'))

        else:
            print(userForm.errors, personForm.errors, nurseForm.errors)

    # Otherwise pre-fill all of the forms
    else:
        userForm = UserForm(instance=user_model)
        personForm = PersonRegistrationForm(instance=person_model)
        nurseForm = updateNurseForm(instance=nurse_model)

    context = {'user_form': userForm, 'personForm': personForm, 'employeeUpdate': nurseForm,
               'nurID': nurse_model.id, 'user': user_model}

    # Return all form information to the page
    return render(request, 'userprofile/updateNurse.html', context)


@login_required
@group_required('Admin', 'Root')
def updateAdmin(request, **kwargs):
    """
    @function: updateProf
    @description: Update the changes made a to user profile to the database.
    """
    admID = kwargs.get('pk')
    # Grab all of the model instances necessary
    admin_model = Admin.objects.get(id=admID)
    person_model = Person.objects.get(id=admin_model.personID.id)
    user_model = User.objects.get_by_natural_key(person_model.user)

    if request.method == 'POST':
        # Create all necessary forms
        userForm = UserForm(request.POST, instance=user_model)
        personForm = PersonRegistrationForm(request.POST, instance=person_model)
        employeeForm = updateAdminForm(request.POST, instance=admin_model)
        # Validate forms
        if (userForm.is_valid() and personForm.is_valid()
            # and addressForm.is_valid()
            ):
            # Save the user form.
            userForm.save()

            # Use the user updates  to update the person object.
            user_model = User.objects.get_by_natural_key(user_model.username)
            birthday = personForm.cleaned_data['birthday']
            phoneNumber = personForm.cleaned_data['phoneNumber']
            Person.objects.filter(user=person_model.user).update(user=user_model,
                                                                 birthday=birthday,
                                                                 phoneNumber=phoneNumber)

            admin_model.personID = person_model
            admin_model.save()

            logPerson = Person.objects.get(user=request.user)
            Logger.createLog('Updated',logPerson,person_model,admin_model.hospitalID)

            currentUser = User.objects.all().filter(id=request.user.id)

            if currentUser == user_model:
                return HttpResponseRedirect(reverse('profile:viewProfile'))
            else:
                return HttpResponseRedirect(reverse('profile:viewAllPersonnel'))

        else:
            print(userForm.errors, personForm.errors)

    # Otherwise pre-fill all of the forms
    else:
        userForm = UserForm(instance=user_model)
        personForm = PersonRegistrationForm(instance=person_model)
        employeeForm = updateAdminForm(instance=admin_model)

    context = {'user_form': userForm, 'personForm': personForm,
               'admID': admin_model.id, 'user': user_model}

    # Return all form information to the page
    return render(request, 'userprofile/updateAdmin.html', context)


@login_required
@group_required('Root')
def updateRoot(request, **kwargs):
    """
    @function: updateProf
    @description: Update the changes made a to user profile to the database.
    """
    rootID = kwargs.get('pk')
    # Grab all of the model instances necessary
    root_model = Root.objects.get(id=rootID)
    person_model = Person.objects.get(id=root_model.personID.id)
    user_model = User.objects.get_by_natural_key(person_model.user)

    if request.method == 'POST':
        # Create all necessary forms
        userForm = UserForm(request.POST, instance=user_model)
        personForm = PersonRegistrationForm(request.POST, instance=person_model)
        employeeForm = updateAdminForm(request.POST, instance=root_model)
        # Validate forms
        if (userForm.is_valid() and personForm.is_valid()):
            # Save the user form.
            userForm.save()

            # Use the user updates  to update the person object.
            user_model = User.objects.get_by_natural_key(user_model.username)
            birthday = personForm.cleaned_data['birthday']
            phoneNumber = personForm.cleaned_data['phoneNumber']
            Person.objects.filter(user=person_model.user).update(user=user_model,
                                                                 birthday=birthday,
                                                                 phoneNumber=phoneNumber)

            root_model.personID = person_model
            root_model.save()

            return HttpResponseRedirect(reverse('profile:viewProfile'))

        else:
            pass

    # Otherwise pre-fill all of the forms
    else:
        userForm = UserForm(instance=user_model)
        personForm = PersonRegistrationForm(instance=person_model)
        employeeForm = updateAdminForm(instance=root_model)

    context = {'user_form': userForm, 'personForm': personForm,
               'rootID': root_model.id, 'user': user_model}

    # Return all form information to the page
    return render(request, 'userprofile/updateRoot.html', context)


@login_required
@group_required('Admin', 'Root')
def deleteDoc(request, **kwargs):
    """
    @function: deleteAppointment
    @description: Removes/Cancels an appointment for a user
    """
    personnelID = kwargs.get('pk')
    doctorModel = get_object_or_404(Doctor, id=personnelID)
    if request.method == 'POST':
        form = DeleteDoctor(request.POST, instance=doctorModel)
        if form.is_valid():
            ##add logger

            User.objects.get(username=doctorModel.personID.user.username).delete()
            return HttpResponseRedirect(reverse('profile:viewAllPersonnel'))
    else:
        form = DeleteDoctor(instance=doctorModel)
    template_vars = {'form': form,
                     'personnelID': personnelID,
                     'personnel': doctorModel,
                     'isDoctor': True,
                     'isNurse': False,
                     'isAdmin': False
                     }
    return render(request, 'userprofile/deleteDoctor.html', template_vars)


@login_required
@group_required('Admin', 'Root')
def deleteNurse(request, **kwargs):
    personnelID = kwargs.get('pk')
    nurseModel = get_object_or_404(Nurse, id=personnelID)
    if request.method == 'POST':
        form = DeleteNurse(request.POST, instance=nurseModel)
        if form.is_valid():
            logPerson = Person.objects.get(
                User.objects.get_by_natural_key(request.user.username))
            Logger.objects.create(type='Deleted', user1=logPerson, user2=nurseModel.personID)

            User.objects.get(username=nurseModel.personID.user.username).delete()
            # Only have to delete use because doing so deletes linked information
            # Specifically: Person, Nurse
            return HttpResponseRedirect(reverse('profile:viewAllPersonnel'))
    else:
        form = DeleteNurse(instance=nurseModel)
    template_vars = {'form': form,
                     'personnelID': personnelID,
                     'personnel': nurseModel,
                     }
    return render(request, 'userprofile/deleteNurse.html', template_vars)


@login_required
@group_required('Admin', 'Root')
def deleteAdmin(request, **kwargs):
    personnelID = kwargs.get('pk')
    adminModel = get_object_or_404(Admin, id=personnelID)
    if request.method == 'POST':
        form = DeleteAdmin(request.POST, instance=adminModel)
        if form.is_valid():
            logPerson = Person.objects.get(
                User.objects.get_by_natural_key(request.user.username))
            Logger.objects.create(type='Deleted', user1=logPerson, user2=adminModel.personID)
            User.objects.get(username=adminModel.personID.user.username).delete()
            # Only have to delete use because doing so deletes linked information
            # Specifically: Person, Admin
            return HttpResponseRedirect(reverse('profile:viewAllPersonnel'))
    else:
        form = DeleteAdmin(instance=adminModel)
    template_vars = {'form': form,
                     'personnelID': personnelID,
                     'personnel': adminModel,
                     }
    return render(request, 'userprofile/deleteAdmin.html', template_vars)

@login_required
@group_required('Admin', 'Root')
def moveNurse(request, **kwargs):
    personnelID = kwargs.get('pk')
    nurseModel = get_object_or_404(Nurse,id=personnelID)
    currUser = request.user
    currPerson = Person.objects.get(user=currUser)

    if Admin.objects.filter(personID=currPerson).exists():

        adminModel = Admin.objects.get(personID=currPerson)

        if request.method == 'POST':
            form = MoveNurse(adminModel.hospitalID.id, request.POST,instance=nurseModel)

            if form.is_valid():
                #nurse = form.save(commit=False)

                if nurseModel.hospitalID != form.cleaned_data['hospitals']:
                    nurseModel.hospitalID = form.cleaned_data['hospitals']
                    nurseModel.save()
                    return HttpResponseRedirect(reverse('profile:viewAllPersonnel'))
                else:
                    return HttpResponseRedirect(reverse('profile:viewAllPersonnel'))

            else:
                print(form.errors)
        else:
            form = MoveNurse(adminModel.hospitalID.id,instance=nurseModel)

        context = {'nurse':nurseModel,'admin':adminModel,'form':form}

        return render(request,'userprofile/moveNurse.html',context)
    elif Root.objects.filter(personID=currPerson).exists():
        rootModel = Root.objects.get(personID=currPerson)
        if request.method == 'POST':
            form = RootMoveNurseForm(request.POST,instance=nurseModel)

            if form.is_valid():
                #nurse = form.save(commit=False)

                if nurseModel.hospitalID != form.cleaned_data['destinationHosp']:
                    nurseModel.hospitalID = form.cleaned_data['destinationHosp']
                    nurseModel.save()
                    return HttpResponseRedirect(reverse('profile:viewAllPersonnel'))
                else:
                    return HttpResponseRedirect(reverse('profile:viewAllPersonnel'))

            else:
                print(form.errors)
        else:

            form = RootMoveNurseForm(initial={'personnel':nurseModel})

        context = {'nurse':nurseModel,'root':rootModel,'form':form}

        return render(request,'userprofile/moveNurse.html',context)

@login_required
@group_required('Admin', 'Root')
def moveDoctor(request, **kwargs):
    personnelID = kwargs.get('pk')
    doctorModel = get_object_or_404(Doctor,id=personnelID)
    currUser = request.user
    currPerson = Person.objects.get(user=currUser)

    if Admin.objects.filter(personID=currPerson).exists():

        adminModel = Admin.objects.get(personID=currPerson)

        if request.method == 'POST':
            form = MoveDoctor(adminModel.hospitalID.id, request.POST,instance=doctorModel)

            if form.is_valid():
                #nurse = form.save(commit=False)
                if doctorModel.hospitalID != form.cleaned_data['hospitals']:
                    doctorModel.hospitalID = form.cleaned_data['hospitals']
                    doctorModel.save()
                    return HttpResponseRedirect(reverse('profile:viewAllPersonnel'))
                else:
                    return HttpResponseRedirect(reverse('profile:viewAllPersonnel'))

            else:
                print(form.errors)
        else:
            form = MoveDoctor(adminModel.hospitalID.id,instance=doctorModel)

        context = {'doctor':doctorModel,'admin':adminModel,'form':form}

        return render(request,'userprofile/moveDoctor.html',context)
    elif Root.objects.filter(personID=currPerson).exists():
        rootModel = Root.objects.get(personID=currPerson)
        if request.method == 'POST':
            form = RootMoveDoctorForm(request.POST,instance=doctorModel)

            if form.is_valid():


                if doctorModel.hospitalID != form.cleaned_data['destinationHosp']:
                    doctorModel.hospitalID = form.cleaned_data['destinationHosp']
                    doctorModel.save()
                    return HttpResponseRedirect(reverse('profile:viewAllPersonnel'))
                else:
                    return HttpResponseRedirect(reverse('profile:viewAllPersonnel'))

            else:
                print(form.errors)
        else:
            form = RootMoveDoctorForm(initial={'personnel':doctorModel})

        context = {'doctor':doctorModel,'root':rootModel,'form':form}

        return render(request,'userprofile/moveDoctor.html',context)


def getPreferredHospitals(request,pk):
    currPatient = Patient.objects.get(id=pk)
    print(currPatient)
    if request.method == 'POST':
        form = PreferredHospitalForm(request.POST)

        if form.is_valid():

            hospitalOne = form.cleaned_data["hospital"]
            currPatient.preferredHospital = hospitalOne
            print("here",currPatient.preferredHospital)
            currPatient.save()
            return HttpResponseRedirect(reverse("profile:viewProfile"))
        else:
            print(form.errors)
    else:
        form = PreferredHospitalForm()

        #print(form)
    context = {'form':form,'patient':currPatient}
    return render(request,'userprofile/preferredHospital.html',context)

def updatePreferredHospitals(request,pk):
    currPatient = get_object_or_404(Patient,id=pk)
    if request.method == 'POST':
        form = PreferredHospitalForm(request.POST)

        if form.is_valid():
            hospitalOne = form.cleaned_data["hospital"]
            currPatient.preferredHospital = hospitalOne
            currPatient.save()
            return HttpResponseRedirect(reverse("profile:viewProfile"))
        else:
            print(form.errors)
    else:
        form = PreferredHospitalForm(initial={'hospital':currPatient.preferredHospital})

    context = {'form':form,'patient':currPatient}
    return render(request,'userprofile/updatePreferredHospital.html',context)
