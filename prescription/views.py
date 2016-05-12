from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from .forms import *
from base.views import group_required
from base.models import *


# Create your views here.
@login_required
@group_required('Doctor')
def createPrescription(request, patient=None):
    user = User.objects.get(username=request.user.username)
    person = Person.objects.get(user=user)
    doctor = Doctor.objects.get(personID=person)

    print(Prescription.objects.all())
    prescriptionSuccess = False
    if request.method == 'POST':
        preForm = PrescriptionForm(request.POST)
        medForm = MedicationForm(request.POST)
        prescrip = apps.get_model('base', 'Prescription')

        # If both forms are valid
        if (preForm.is_valid() and medForm.is_valid()):
            # Grab the cleaned data from the form
            # Medication form first
            name = medForm.cleaned_data['name']
            descrip = medForm.cleaned_data['description']

            # Create a medication object
            med = Medication(name=name, description=descrip)
            med.save()
            Logger.createLog('Created',person,str(prescrip),doctor.hospitalID)
            pat = preForm.cleaned_data['patient']
            amount = preForm.cleaned_data['amount']
            refill = preForm.cleaned_data['refill']

            Prescription.objects.create(medication=med, patientID=pat, amount=amount,
                                        refill=refill, doctorID=doctor)

            prescriptionSuccess = True
            # prescription = preForm.save(commit=False)
            # # prescription.doctor = doctor
            # prescription.save()

            # medication = medForm.save(commit=False)
            # medication.save()
            # Todo add system logger event
    else:
        preForm = PrescriptionForm()
        medForm = MedicationForm()

        # If a patient is passed in
        if patient is not None:
            # Fill the form 
            preForm.fields['patient'].initial = patient

            # # Set the doctor field
            # preForm.fields['doctor'].initial = doctor

            # Hide the doctor field
            # preForm.fields['doctor'].widget = forms.HiddenInput()

    context = {'prescriptionForm': preForm,
               'medicationForm': medForm,
               'prescriptionSuccess': prescriptionSuccess}
    return render(request, 'prescription/write.html', context)


@login_required
@group_required('Patient', 'Nurse', 'Doctor')
def viewPrescriptions(request):
    user_model = User.objects.get_by_natural_key(request.user.username)
    person_model = Person.objects.get(user=user_model)

    # Create a context
    context = {
        'prescriptions': None
    }

    # If a patient is viewing
    if Patient.objects.filter(personID=person_model).exists():
        patient_model = Patient.objects.get(personID=person_model)

        # Grab the prescriptions
        prescriptions = Prescription.objects.all().filter(patientID=patient_model.id).order_by(
            'patientID__personID__user__first_name')
        context['prescriptions'] = prescriptions
    # If a doctor is viewing
    elif Doctor.objects.filter(personID=person_model).exists():
        doctor_model = Doctor.objects.get(personID=person_model)

        patients = gatherPatientList(user_model)
        prescriptions = Prescription.objects.all().filter(doctorID=doctor_model.id).order_by(
            'patientID__personID__user__first_name')
        context['prescriptions'] = prescriptions
    # If a nurse is viewing
    elif Nurse.objects.filter(personID=person_model).exists():
        nurse_model = Nurse.objects.get(personID=person_model)

        patients = gatherPatientList(user_model)
        prescriptions = []

        for p in patients:
            # Grab each patient's prescriptions
            prescriptionObjects = Prescription.objects.all().filter(patientID=p.id)
            # Add them to the list
            prescriptions.extend(prescriptionObjects)

        context['prescriptions'] = prescriptions

    return render(request, 'prescription/view.html', context)


@login_required()
@group_required('Doctor')
def deletePrescription(request, **kwargs):
    prescriptionID = kwargs.get('pk')
    prescription_model = get_object_or_404(Prescription, id=prescriptionID)
    # If a post method
    if request.method == 'POST':
        form = DeletePrescription(request.POST, instance=prescription_model)
        if form.is_valid():
            prescription_model.delete()
            return HttpResponseRedirect(reverse('prescription:view'))
    else:
        form = DeletePrescription(instance=prescription_model)
        context = {'form': form,
                   'prescriptionID': prescriptionID,
                   'prescription_model': prescription_model, }
    return render(request, 'prescription/view.html', context)


def gatherPatientList(requestUser):
    person_model = Person.objects.get(user=requestUser)
    if Nurse.objects.filter(personID=person_model).exists():
        nursePerson = Nurse.objects.all().get(personID=person_model)
        # Grab the nurse's hospital ID
        hospital_id = nursePerson.hospitalID
        # Grab patients with that hospital ID
        patients = Patient.objects.all().filter(hospitalID=hospital_id)

    elif Admin.objects.filter(personID=person_model).exists():
        adminPerson = Admin.objects.all().get(personID=person_model)
        hospital_id = adminPerson.hospitalID
        patients = Patient.objects.all().filter(hospitalID=hospital_id)

    elif Doctor.objects.filter(personID=person_model).exists():
        patients = Patient.objects.all()

    elif Root.objects.filter(personID=person_model).exists():
        patients = Patient.objects.all()

    else:
        patients = []
    return patients
