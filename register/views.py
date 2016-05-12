"""
    Application: HealthNet
    File: /patientRegistration/views.py
    Authors:
        - Nathan Stevens
        - Phillip Bedward
        - Daniel Herzig
        - George Herde
        - Samuel Launt

    Description:
        - This file contains the view controller functionality for
          a Patient Registering and Signing up as a User
"""
from .forms import *
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from base.models import Logger, Admin, Patient, Person
from base.views import group_required


@login_required
@group_required('Admin', 'Root')
def createAdmin(request):
    if request.user.groups.filter(name='Root').exists():
        if request.method == 'POST':
            userForm = UserForm(request.POST)
            personForm = PersonRegistrationForm(request.POST)
            addressForm = AddressForm(request.POST)
            adminForm = AdminRootForm(request.POST)

            if (userForm.is_valid() and personForm.is_valid() and addressForm.is_valid() and adminForm.is_valid()):
                user = userForm.save()
                user.set_password(user.password)
                user.save()
                Group.objects.get(name='Admin').user_set.add(user)

                person = personForm.save(commit=False)
                person.user = user
                person.save()

                address = addressForm.save(commit=False)
                address.save()

                adm = adminForm.save(commit=False)
                adm.personID = person
                adm.addressID = address
                adm.save()

                logPerson = Person.objects.get(user=
                                               User.objects.get_by_natural_key(request.user.username))
                Logger.createLog('Created', logPerson, adm.personID, adm.hospitalID)
                return HttpResponseRedirect(reverse('profile:userLogin'))

            else:

                print(userForm.errors, personForm.errors, addressForm.errors, adminForm.errors)
        else:
            userForm = UserForm()
            personForm = PersonRegistrationForm()
            addressForm = AddressForm()
            adminForm = AdminRootForm()
        return render(request, 'register/createAdmin.html',
                      {'user_form': userForm, 'adminRegistration': personForm,
                       'addressForm': addressForm, 'adminForm': adminForm})
        # If the registering user is an admin for a hospital
    else:
        adminModel = get_object_or_404(Admin, personID=Person.objects
                                       .get(user=User.objects
                                            .get_by_natural_key(request.user)))
        hospitalID = adminModel.hospitalID
        if request.method == 'POST':
            userForm = UserForm(request.POST)
            personForm = PersonRegistrationForm(request.POST)
            addressForm = AddressForm(request.POST)
            adminForm = AdminForm(request.POST)

            if (userForm.is_valid() and personForm.is_valid() and addressForm.is_valid() and adminForm.is_valid()):
                user = userForm.save()
                user.set_password(user.password)
                user.save()
                Group.objects.get(name='Admin').user_set.add(user)

                person = personForm.save(commit=False)
                person.user = user
                person.save()

                address = addressForm.save(commit=False)
                address.save()

                adm = adminForm.save(commit=False)
                adm.personID = person
                adm.hospitalID = hospitalID
                adm.addressID = address
                adm.save()

                logPerson = Person.objects.get(user=
                                               User.objects.get_by_natural_key(request.user.username))
                Logger.createLog('Created', logPerson, adm.personID, adm.hospitalID)
                return HttpResponseRedirect(reverse('profile:userLogin'))

            else:

                print(userForm.errors, personForm.errors, addressForm.errors, adminForm.errors)
        else:
            userForm = UserForm()
            personForm = PersonRegistrationForm()
            addressForm = AddressForm()
            adminForm = AdminForm()
        return render(request, 'register/createAdmin.html',
                      {'user_form': userForm, 'adminRegistration': personForm,
                       'addressForm': addressForm, 'adminForm': adminForm})


@login_required
@group_required('Admin', 'Root')
def createDoctor(request, **kwargs):
    if request.user.groups.filter(name='Root').exists():
        if request.method == 'POST':
            userForm = UserForm(request.POST)
            personForm = PersonRegistrationForm(request.POST)
            addressForm = AddressForm(request.POST)
            doctorForm = DoctorRootForm(request.POST)

            if (userForm.is_valid() and personForm.is_valid() and addressForm.is_valid() and doctorForm.is_valid()):
                user = userForm.save()
                user.set_password(user.password)
                user.save()
                Group.objects.get(name='Doctor').user_set.add(user)

                person = personForm.save(commit=False)
                person.user = user
                person.save()

                address = addressForm.save(commit=False)
                address.save()

                doc = doctorForm.save(commit=False)
                doc.personID = person
                doc.patientID = None
                doc.addressID = address
                doc.save()

                logPerson = Person.objects.get(user=
                                               User.objects.get_by_natural_key(request.user.username))
                Logger.createLog('Created', logPerson, doc.personID, doc.hospitalID)
                return HttpResponseRedirect(reverse('profile:userLogin'))

            else:

                print(userForm.errors, personForm.errors, addressForm.errors, doctorForm.errors)
        else:
            userForm = UserForm()
            personForm = PersonRegistrationForm()
            addressForm = AddressForm()
            doctorForm = DoctorRootForm()
        return render(request, 'register/createDoctor.html',
                      {'user_form': userForm, 'doctorRegistration': personForm,
                       'addressForm': addressForm, 'doctorForm': doctorForm})
    # If the registering user is an admin for a hospital
    else:
        adminModel = get_object_or_404(Admin, personID=Person.objects
                                       .get(user=User.objects
                                            .get_by_natural_key(request.user)))
        hospitalID = adminModel.hospitalID
        if request.method == 'POST':
            userForm = UserForm(request.POST)
            personForm = PersonRegistrationForm(request.POST)
            addressForm = AddressForm(request.POST)
            doctorForm = DoctorForm(request.POST)

            if (userForm.is_valid() and personForm.is_valid() and addressForm.is_valid() and doctorForm.is_valid()):
                user = userForm.save()
                user.set_password(user.password)
                user.save()
                Group.objects.get(name='Doctor').user_set.add(user)

                person = personForm.save(commit=False)
                person.user = user
                person.save()

                address = addressForm.save(commit=False)
                address.save()

                doc = doctorForm.save(commit=False)
                doc.personID = person
                doc.hospitalID = hospitalID
                doc.patientID = None
                doc.addressID = address
                doc.save()

                logPerson = Person.objects.get(user=
                                               User.objects.get_by_natural_key(request.user.username))
                Logger.createLog('Created', logPerson, doc.personID, doc.hospitalID)
                return HttpResponseRedirect(reverse('profile:userLogin'))

            else:

                print(userForm.errors, personForm.errors, addressForm.errors, doctorForm.errors)
        else:
            userForm = UserForm()
            personForm = PersonRegistrationForm()
            addressForm = AddressForm()
            doctorForm = DoctorForm()
        return render(request, 'register/createDoctor.html',
                      {'user_form': userForm, 'doctorRegistration': personForm,
                       'addressForm': addressForm, 'doctorForm': doctorForm})


@login_required
@group_required('Admin', 'Root')
def createNurse(request, **kwargs):
    if request.user.groups.filter(name='Root').exists():
        if request.method == 'POST':
            userForm = UserForm(request.POST)
            personForm = PersonRegistrationForm(request.POST)
            addressForm = AddressForm(request.POST)
            nurseForm = NurseRootForm(request.POST)

            if (userForm.is_valid() and personForm.is_valid() and addressForm.is_valid() and nurseForm.is_valid()):
                user = userForm.save()
                user.set_password(user.password)

                user.save()
                Group.objects.get(name='Nurse').user_set.add(user)

                person = personForm.save(commit=False)
                person.user = user
                person.save()

                address = addressForm.save(commit=False)
                address.save()

                nurse = nurseForm.save(commit=False)
                nurse.personID = person
                nurse.addressID = address
                nurse.save()

                logPerson = Person.objects.get(user=
                                               User.objects.get_by_natural_key(request.user.username))
                Logger.createLog('Created', logPerson, nurse.personID, nurse.hospitalID)
                return HttpResponseRedirect(reverse('profile:userLogin'))

            else:
                pass
        else:
            userForm = UserForm()
            personForm = PersonRegistrationForm()
            addressForm = AddressForm()
            nurseForm = NurseRootForm()
        return render(request, 'register/createNurse.html',
                      {'user_form': userForm, 'nurseRegistration': personForm,
                       'addressForm': addressForm, 'nurseForm': nurseForm})

    # If the registering user is an admin for a hospital
    else:
        adminModel = get_object_or_404(Admin, personID=Person.objects
                                       .get(user=User.objects
                                            .get_by_natural_key(request.user)))
        hospitalID = adminModel.hospitalID
        if request.method == 'POST':
            userForm = UserForm(request.POST)
            personForm = PersonRegistrationForm(request.POST)
            nurseForm = NurseForm(request.POST)
            addressForm = AddressForm(request.POST)

            if (userForm.is_valid() and personForm.is_valid() and addressForm.is_valid()):
                user = userForm.save()
                user.set_password(user.password)

                user.save()
                Group.objects.get(name='Nurse').user_set.add(user)

                person = personForm.save(commit=False)
                person.user = user
                person.save()

                address = addressForm.save(commit=False)
                address.save()

                nurse = nurseForm.save(commit=False)
                nurse.personID = person
                nurse.hospitalID = hospitalID
                nurse.addressID = address
                nurse.save()

                logPerson = Person.objects.get(user=
                                               User.objects.get_by_natural_key(request.user.username))
                Logger.objects.create(type='Created', user1=logPerson, user2=nurse.personID)
                Logger.createLog('Created', logPerson, nurse.personID, nurse.hospitalID)
                return HttpResponseRedirect(reverse('base:landing'))

            else:
                pass

        else:
            userForm = UserForm()
            personForm = PersonRegistrationForm()
            addressForm = AddressForm()
            nurseForm = NurseForm()
        return render(request, 'register/createNurse.html',
                      {'user_form': userForm, 'nurseRegistration': personForm,
                       'addressForm': addressForm, 'nurseForm': nurseForm})


def createPatient(request):
    """
    @function: createPatient
    @description:
                - Registers a Patient
                - Patient creates a User Account during Registration
                - Patient inserts Address information via AddressForm
                - Patient inserts Insurance information via InsuranceForm
                - Patient inserts Emergency Contact via EmergencyContactForm
    @param: request - a request made by a user
    """
    # Set registered variable
    registered = False

    # If the request is a POST type
    if request.method == 'POST':
        # Create forms instance for users and patients
        userForm = UserForm(request.POST)
        personForm = PersonRegistrationForm(request.POST)
        insuranceForm = InsuranceForm(request.POST)
        addressForm = AddressForm(request.POST)
        emergencyContForm = EmergencyContactForm(request.POST)


        # Check if the form is valid
        if (userForm.is_valid() and personForm.is_valid()) and (insuranceForm.is_valid() and addressForm.is_valid()) \
                and (emergencyContForm.is_valid()):
            # First save user form and set password
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            Group.objects.get(name='Patient').user_set.add(user)

            # Create a person
            person = personForm.save(commit=False)
            person.user = user
            person.save()

            # Save the address
            address = addressForm.save(commit=False)
            address.save()

            # Save insurance info
            insurance = insuranceForm.save(commit=False)
            insurance.addressID = address
            insurance.save()

            # Save emergency contact info
            emergencyForm = emergencyContForm.save(commit=False)
            forms = getFormTuple(person, address, insurance)
            objects = getObjectTuple(EmergencyContact, emergencyForm, Person, Patient)
            checkContact(forms, objects)

            # Set registered variable
            registered = True
            registerAttempt = True
            Logger.createLog("Registered", person)

        else:
            registerAttempt = True

            print(userForm.errors, personForm.errors, insuranceForm.errors, addressForm.errors,
                  emergencyContForm.errors)
    # If the request is not of POST type
    else:
        userForm = UserForm()
        personForm = PersonRegistrationForm()
        insuranceForm = InsuranceForm()
        addressForm = AddressForm()
        emergencyContForm = EmergencyContactForm()
        registerAttempt = True

    context = {'user_form': userForm, 'patientRegistration': personForm,
               'addressForm': addressForm, 'insuranceForm': insuranceForm,
               'emergencyForm': emergencyContForm, 'registered': registered,
               'registerAttempt': registerAttempt}
    return render(request, 'register/createPatient.html', context)


def getFormTuple(form1, form2, form3):
    """
    @function: getFormTuple
    @description: returns a collection of forms.
    @param: form1 - first form to return
    @param: form2 - second form to return
    @param: form3 - third form to return
    @return - returns a tuple of parameter forms
    """
    return form1, form2, form3


def getObjectTuple(obj1, obj2, obj3, obj4):
    """
    @function: getObjectTuple
    @description: returns a collection of objects
    @param obj1 - first object to be returned
    @param obj2 - second object to be returned
    @param obj3 - third object to be returned
    @param obj4 - fourth object to be returned
    @return - returns a tuple of all the object parameters
    """
    return obj1, obj2, obj3, obj4


def checkContact(formTuple, objTuple):
    """
    @function: checkContact
    @description: This function is the flow for entering an emergency contact.
                  An Emergency contact is a Person, who a Patient enters as the
                  person who an in case of an emergency is contacted.
    @param: formTuple - collection of forms
    @param: objTuple - collection of objects.
    """
    person, address, insurance = formTuple
    emergencyContact, emergencyForm, personModel, patient = objTuple
    # Boolean value if Emergency Contact already exists
    emergencyPhoneNumber = emergencyForm.emergencyNumber
    contactExists = EmergencyContact.objects.filter(firstName=emergencyForm.firstName,
                                                    lastName=emergencyForm.lastName,
                                                    emergencyNumber=emergencyPhoneNumber).exists()
    # Boolean value of User exists

    userExists = User.objects.filter(first_name=emergencyForm.firstName,
                                     last_name=emergencyForm.lastName).exists()
    # If the Emergency Contact is already in the model
    if contactExists:
        # Create a contact from the emergencyForm
        contact = EmergencyContact.objects.get(firstName=emergencyForm.firstName,
                                               lastName=emergencyForm.lastName,
                                               emergencyNumber=emergencyPhoneNumber)

        # creates the patient object, with the emergency contact
        Patient.objects.create(personID=person,
                               addressID=address,
                               insuranceID=insurance,
                               emergencyContactID=contact)

    # if the user exists but the contact does not
    elif userExists:
        # Boolean value if the Emergency contact exists as a Person
        userModel = User.objects.get(first_name=emergencyForm.firstName,
                                     last_name=emergencyForm.lastName)
        personExists = Person.objects.filter(user=userModel, phoneNumber=emergencyPhoneNumber).exists()
        # if person with emergency contact info exists
        if personExists:
            # create personInstance with emergency info
            personInstance = Person.objects.get(user=userModel,
                                                phoneNumber=emergencyPhoneNumber)

            # patient is created with Person info as Emergency contact
            emergencyForm.personID = personInstance
            emergencyForm.save()
            Patient.objects.create(personID=person,
                                   addressID=address,
                                   insuranceID=insurance,
                                   emergencyContactID=emergencyForm)
        else:
            pass
    # New Emergency Contact, and inserts all new information
    else:
        emergencyForm.save()
        Patient.objects.create(personID=person,
                               addressID=address,
                               insuranceID=insurance,
                               emergencyContactID=emergencyForm)
