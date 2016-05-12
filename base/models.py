"""
    Application: HealthNet
    File: models.py
    Authors:
        - Nathan Stevens
        - Philip Bedward
        - Daniel Herzig
        - George Herde
        - Samuel Launt

    Description:
        - This file contains all the class definitions for each
          model within the HealthNet application
"""
from django.conf import settings
from django.db import models
from django.db import signals
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _  # import ugettext as an underscore
import datetime

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class Person(models.Model):
    """
    @class: Person
    @description: A person, who has registered to use the HealthNet
                  application.  A Person may be a Doctor, Nurse, or
                  Patient.
    @Primary Key: SSN - the person's Social Security Number
    @Relationships:
                - Person can be a Patient, Doctor, or Nurse
    """
    id = models.AutoField(primary_key=True)
    ssn = models.PositiveIntegerField()
    user = models.OneToOneField(User)
    # Make a name field with a max_length of 100 characters
    birthday = models.DateField()
    phoneNumber = models.PositiveIntegerField()

    def __str__(self):
        """
        @description: returns a string for First and Last name
        """
        return '%s %s' % (self.user.first_name, self.user.last_name)

    def get_absolute_url(self):
        return reverse('person-detail', kwargs={'pk': self.pk})


class Doctor(models.Model):
    """
    @class: Doctor
    @description: A Doctor has specific permissions within the HealthNet
                  application.
    @Primary Key: id - auto-generated
    @Relationships:
                - personID - the Doctor is a Patient
                - patientID - A Doctor has many patients
    """
    id = models.AutoField(primary_key=True)
    licenseNumber = models.PositiveIntegerField()
    specialty = models.CharField(max_length=200, blank=True)
    hospitalID = models.ForeignKey('Hospital', to_field='id')
    personID = models.ForeignKey('Person', to_field='id')
    patients = models.ManyToManyField('Patient', blank=True)
    addressID = models.ForeignKey('Address', to_field='id')

    def __str__(self):
        return '%s' % (self.personID.__str__())


class Nurse(models.Model):
    """
    @class: Nurse
    @description: A Nurse, has specific permissions within the HealthNet
                  application.  Nurse is a person.
    @Primary Key: Id, auto-generated.
    @Relationships:
                - personID - A Nurse is a Person
                - hospitalID - A Nurse has a Hospital
    """
    id = models.AutoField(primary_key=True)
    license_number = models.PositiveIntegerField()
    department = models.CharField(max_length=300)
    personID = models.ForeignKey('Person', to_field='id')
    hospitalID = models.ForeignKey('Hospital', to_field='id')
    addressID = models.ForeignKey('Address', to_field='id')

    def __str__(self):
        return '%s' % (self.personID.__str__())


class Patient(models.Model):
    """
    @class: Patient
    @description: A Patient, is one of the most active actors within the
                  HealthNet application.  A Patient is a Person.
    @Primary Key: Id, auto-generated.
    @Relationships:
                - personID - A Patient is a Person
                - addressID - A Patient has an Address
                - insuranceID - A Patient has Insurance
                - emergencyContactID - A Patient has an Emergency Contact
    """
    id = models.AutoField(primary_key=True)
    personID = models.ForeignKey('Person', to_field='id')
    addressID = models.ForeignKey('Address', to_field='id')
    insuranceID = models.ForeignKey('Insurance', to_field='id')
    emergencyContactID = models.ForeignKey('EmergencyContact', to_field='id')
    hospitalID = models.ForeignKey('Hospital', to_field='id', null=True, blank=True, related_name='hospitalID')
    medicalID = models.ForeignKey('MedicalHistory', to_field='id', null=True, blank=True)
    preferredHospital = models.ForeignKey('Hospital', to_field='id', null=True, blank=True,
                                          related_name='preferredHospital')

    """
        @description: returns a string of the Patient's id
    """

    def __str__(self):
        return '%s' % (self.personID.__str__())


class Root(models.Model):
    """
    @class: Root
    @description: A Root user has the highest level permissions within
                  the application.
    @Primary Key: id - auto-generated
    """
    id = models.AutoField(primary_key=True)
    personID = models.ForeignKey('Person', to_field='id')


class Admin(models.Model):
    """
    @class: Admin
    @description: Admin role for application, has high level permissions
    @Primary Key: Id, auto-generated.
    @Relationships:
                - hospitalID - the Admin works at a Hospital
                - personID - Admin is a Person
    """
    id = models.AutoField(primary_key=True)
    hospitalID = models.ForeignKey('Hospital', to_field='id')
    personID = models.ForeignKey('Person', to_field='id')
    # addressID = models.ForeignKey('Address', to_field='id')


class Appointment(models.Model):
    """
    @class: Appointment
    @description: A Patient, and Doctor have an appointment with each other
    @Primary Key: Id, auto-generated.
    @Relationships:
                - doctorID - An Appointment has a Doctor
                - patientID - An Appointment has a Patient
    """
    id = models.AutoField(primary_key=True)
    doctorID = models.ForeignKey('Doctor', to_field='id')
    patientID = models.ForeignKey('Patient', to_field='id')
    aptDate = models.DateField()
    aptTime = models.TimeField()

    reason = models.CharField(max_length=300)

    def getPatient(self):
        return self.patientID

    def getHospital(self):
        return self.doctorID.hospitalID

    """
        @description: returns a string for an Appointment
    """

    def __str__(self):
        return 'Doctor: %s Patient: %s Date: %s Time: %s Reason %s' \
               % (self.doctorID, self.patientID, self.aptDate, self.aptTime, self.reason)


class ExtendedStay(models.Model):
    id = models.AutoField(primary_key=True)
    appointmentID = models.ForeignKey('Appointment', to_field='id')
    endDate = models.DateField()
    endTime = models.TimeField()

    def getPatient(self):
        return self.appointmentID.patientID

    def __str__(self):
        return "Patient: %s, admitted until %s at %s" % (self.getPatient(), self.endDate, self.endTime)


class Address(models.Model):
    """
    @class: Address
    @description: A Person and Hospital have an address where they reside
    @Primary Key: Id, auto-generated.
    @Relationships:
    """
    id = models.AutoField(primary_key=True)
    street = models.CharField(max_length=200)
    zip = models.PositiveIntegerField()
    # Todo: This is dropping '0's off the front of the value EX: 02043 -> 2043
    # Do we change this to a CharField to prevent the loss of values?
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)

    """
        @description: returns a string value of an address
    """

    def __str__(self):
        return '%s %s, %s %s' % (self.street, self.city, self.state, self.zip,)


class Insurance(models.Model):
    """
    @class: Insurance
    @description: An insurance company with policy number of a client to have
                  insurance coverage
    @Primary Key: Id, auto-generated
    @Relationships:
                - addressID - Insurance has an Address.
    """
    id = models.AutoField(primary_key=True)
    addressID = models.ForeignKey(Address, to_field='id')
    name = models.CharField(max_length=100)
    policyNumber = models.PositiveIntegerField()

    def __str__(self):
        return 'Company: %s Policy Number: %i' % (self.name, self.policyNumber)


class Hospital(models.Model):
    """
    @class: Hospital
    @description: Where a Doctor, Nurse, and Admin work.  A patient
                  receives healthcare at a Hospital
    @Primary Key: Id, auto-generated
    @Relationships:
                - addressID - Insurance has an Address.
                - doctorID - Hospital has many Doctors
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.ForeignKey('Address', to_field='id', null=True)
    # MANY TO MANY RELATIONSHIP: HOSPITAL TO DOCTOR
    # A hospital has doctors
    # doctorID = models.ManyToManyField(Doctor)
    # Add nurse field
    # nurseID = models.ManyToManyField(Nurse)
    # patients = models.ManyToManyField(Patient)


    def __str__(self):
        """
        @description: Returns a string of the Hospital's name
        """
        return '%s' % (self.name)


class EmergencyContact(models.Model):
    """
    @class: EmergencyContact
    @description: When a Patient registers they must list an EmergencyContact
                  in case of an Emergency.
    @Primary Key: Id, auto-generated
    @Relationships:
                - personID - An EmergencyContact is a Person
    """
    id = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    emergencyNumber = models.PositiveIntegerField()
    personID = models.ForeignKey('Person', to_field='id', default=None, null=True)

    """
        description: Returns a String of an EmergencyContact
    """

    def __str__(self):
        return 'Emergency: %s %s' % (self.firstName, self.lastName)


class MessageManager(models.Manager):
    def inbox_for(self, user):
        """
        Returns all messages that were received by the given user
        and are not marked as deleted
        """
        return self.filter(
            recipient=user,
            recipient_deleted_at__isnull=True,
        )

    def outbox_for(self, user):
        """
        Returns all messages that were sent by the given user and are not
        marked as deleted.
        """
        return self.filter(
            sender=user,
            sender_deleted_at__isnull=True,
        )

    def trash_for(self, user):
        """
        Returns all messages that were either received or sent by the given
        user and are marked as deleted.
        """
        return self.filter(
            recipient=user,
            recipient_deleted_at__isnull=False,
        ) | self.filter(
            sender=user,
            sender_deleted_at__isnull=False,
        )


class Message(models.Model):
    """
    A private message from user to user
    """
    subject = models.CharField(_("Subject"), max_length=120)
    body = models.CharField(_("Body"), max_length=500)
    sender = models.ForeignKey('Person', to_field='id', related_name='sent_messages', verbose_name=_("Sender"))
    recipient = models.ForeignKey('Person', to_field='id', related_name='received_messages', null=True, blank=True,
                                  verbose_name=_("Recipient"))
    parent_msg = models.ForeignKey('self', related_name='next_messages', null=True, blank=True,
                                   verbose_name=_("Parent message"))
    sent_at = models.DateTimeField(_("sent at"), null=True, blank=True)
    read_at = models.DateTimeField(_("read at"), null=True, blank=True)
    replied_at = models.DateTimeField(_("replied at"), null=True, blank=True)
    sender_deleted_at = models.DateTimeField(_("Sender deleted at"), null=True, blank=True)
    recipient_deleted_at = models.DateTimeField(_("Recipient deleted at"), null=True, blank=True)

    objects = MessageManager()

    def new(self):
        """returns whether the recipient has read the message or not"""
        if self.read_at is not None:
            return False
        return True

    def replied(self):
        """returns whether the recipient has written a reply to this message"""
        if self.replied_at is not None:
            return True
        return False

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return ('messages:view', [self.id])

    get_absolute_url = models.permalink(get_absolute_url)

    def save(self, **kwargs):
        if not self.id:
            self.sent_at = timezone.now()
        super(Message, self).save(**kwargs)

    class Meta:
        ordering = ['-sent_at']
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")


def inbox_count_for(user):
    """
    returns the number of unread messages for the given user but does not
    mark them seen
    """
    return Message.objects.filter(recipient=user, read_at__isnull=True, recipient_deleted_at__isnull=True).count()


# fallback for email notification if django-notification could not be found
# if "notification" not in settings.INSTALLED_APPS and getattr(settings, 'DJANGO_MESSAGES_NOTIFY', True):
#     from django_messages.utils import new_message_email
#     signals.post_save.connect(new_message_email, sender=Message)

class MedicalHistory(models.Model):
    id = models.AutoField(primary_key=True)
    # Basic
    histWeight = models.IntegerField()
    histHeight = models.IntegerField()
    histAge = models.IntegerField()

    # Systems
    histCancer = models.BooleanField()
    histAlcoholism = models.BooleanField()
    histUlcers = models.BooleanField()
    histCholesterol = models.BooleanField()
    histAsthma = models.BooleanField()
    histHeartTrouble = models.BooleanField()
    histKidneyDisease = models.BooleanField()
    histSickleCellAnemia = models.BooleanField()
    histTuberculosis = models.BooleanField()
    histHiv = models.BooleanField()
    histEmphysema = models.BooleanField()
    histHighBloodPressure = models.BooleanField()
    histBleedingDisorder = models.BooleanField()
    histLiverDisorder = models.BooleanField()
    histBirthDefects = models.BooleanField()
    histStroke = models.BooleanField()
    histArthritis = models.BooleanField()
    histDiabetes = models.BooleanField()
    histHeartAttack = models.BooleanField()
    histGout = models.BooleanField()
    histSystems = models.TextField(blank=True)  # Explain field
    histSystemsOther = models.TextField(blank=True)
    # Surgery
    histSurgeryTonsils = models.BooleanField()
    histSurgeryBreast = models.BooleanField()
    histSurgeryAppendix = models.BooleanField()
    histSurgeryUterus = models.BooleanField()
    histSurgeryGallBladder = models.BooleanField()
    histSurgeryOvaries = models.BooleanField()
    histSurgeryStomach = models.BooleanField()
    histSurgeryProstate = models.BooleanField()
    histSurgerySmallIntestine = models.BooleanField()
    histSurgeryColon = models.BooleanField()
    histSurgeryThyroid = models.BooleanField()
    histSurgeryKidney = models.BooleanField()
    histSurgeryHernia = models.BooleanField()
    histSurgeryHeart = models.BooleanField()
    histSurgeryPacemaker = models.BooleanField()
    histSurgeryJointReplace = models.BooleanField()
    histSurgeryExtremities = models.BooleanField()
    histSurgeryOther = models.TextField(blank=True)
    # Allergies
    histAllergyPenicillin = models.BooleanField()
    histAllergySulfa = models.BooleanField()
    histAllergyMetal = models.BooleanField()
    histAllergyNone = models.BooleanField()
    histAllergyOther = models.TextField(blank=True)
    histAllergyFoodOther = models.TextField(blank=True)
    # Medication
    histMedicationOther = models.TextField(blank=True)
    # Conditions
    histConditionShortBreath = models.BooleanField()
    histConditionChestPain = models.BooleanField()
    histConditionWeightLoss = models.BooleanField()
    histConditionConstipation = models.BooleanField()
    histConditionFever = models.BooleanField()
    histConditionVision = models.BooleanField()
    histConditionHeadache = models.BooleanField()
    histConditionUrination = models.BooleanField()
    histConditionNumbness = models.BooleanField()
    # Tobacco
    histTobaccoCigarettes = models.BooleanField()
    histTobaccoFrequency = models.IntegerField(blank=True)
    histTobaccoDuration = models.IntegerField(blank=True)
    histTobaccoOther = models.TextField(blank=True)
    # Alcohol
    histAlcoholBeer = models.IntegerField()
    histAlcoholShots = models.IntegerField()
    histDrugOther = models.TextField(blank=True)
    # Family
    histFamilyCancer = models.BooleanField()
    histFamilyDiabetes = models.BooleanField()
    histFamilyRheumatoidArthritis = models.BooleanField()
    histFamilyArthritis = models.BooleanField()
    histFamilyGout = models.BooleanField()
    histFamilyBleeding = models.BooleanField()
    histFamilySickleCellAnemia = models.BooleanField()
    histFamilyHeartDisease = models.BooleanField()
    histFamilyOther = models.TextField(blank=True)
    # Social
    histRelationship = models.TextField()
    histWork = models.TextField()
    histWorkExplain = models.TextField(blank=True)
    # Primary Care
    histPrimaryName = models.TextField()
    histPrimaryNumber = models.IntegerField()  # Cell phone field validation


class Prescription(models.Model):
    id = models.AutoField(primary_key=True)
    medication = models.ForeignKey('Medication', to_field='id')
    amount = models.IntegerField(default=0)
    refill = models.IntegerField(default=0)
    patientID = models.ForeignKey('Patient', to_field='id')
    doctorID = models.ForeignKey('Doctor', to_field='id')
    timestamp = models.DateTimeField(auto_now_add=True)

    """
        @description: returns a string value of an prescription
    """

    def __str__(self):
        return 'Doctor: %s Patient: %s, Medication: %s Amount: %i Refills: %i' % (self.doctorID, self.patientID,
                                                                                  self.medication, self.amount,
                                                                                  self.refill,)


class Medication(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return 'Name: %s Description: %s' % (self.name, self.description,)


class testResults(models.Model):
    id = models.AutoField(primary_key=True)
    results = models.FileField(upload_to='files', null=True)
    doctor = models.ForeignKey('Doctor', to_field='id', related_name='+')
    patient = models.ForeignKey('Patient', to_field='id', related_name='+')
    comments = models.TextField()
    published = models.BooleanField(default=False)


class Logger(models.Model):
    """
    Logger Types:
    1:"Logged in":       User logged in
    2: "Logged out":      User logged out
    3: "Standard error":  Any error message
    4: "Registered":      A patient created a patient
    5: "Created":         Created anything, admin, nurse, doctor, test, etc
    6: "Updated":         Anything was updated, admin, nurse, doctor, med
    7: "Removed":         Removed an appointment (canceled) by person
    8: "Message":         User sent message
    9: "Released test":   A doctor released test results
    10: "Admitted":        Patient is admitted to hospital
    11: "Released":        Patient is released from hospital
    12: "Transferred":     Patient was transferred from hospital<-lol spelling
    13: "Viewed":          patient information was viewed
    """
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=300)
    timestamp = models.DateTimeField(auto_now_add=True)
    user1 = models.ForeignKey('Person', to_field='id', related_name='+', null=True, blank=True)
    user2 = models.ForeignKey('Person', to_field='id', related_name='+', null=True, blank=True)
    appt = models.ForeignKey('Appointment', to_field='id', related_name='+', null=True, blank=True)
    medHistory = models.ForeignKey('MedicalHistory', to_field='id', related_name='+', null=True, blank=True)
    testResults = models.ForeignKey('testResults', to_field='id', related_name='+', null=True, blank=True)
    hospital1 = models.ForeignKey('Hospital', to_field='id', related_name='+', null=True, blank=True)
    hospital2 = models.ForeignKey('Hospital', to_field='id', related_name='+', null=True, blank=True)
    extra = models.TextField(null=True, blank=True)
    #pre = models.ForeignKey('Prescription', to_field='id', related_name='+', null=True, blank=True)

    """
    There are 3 uses for this
    1: Logger.createLog(type, user1)
    2: Logger.createLog(type, user1, misc, hop)
    3: Logger.createLog(type, user1, user2, hop1, hop2)
    """

    @staticmethod
    def createLog(*args):
        if len(args) == 2:
            log = Logger()
            log.type = args[0]
            log.timestamp = datetime.datetime.now()
            log.user1 = args[1]
            log.save()
        elif len(args) == 4:
            if args[0] == "Standard error":
                log = Logger()
                log.type = args[0]
                log.timestamp = datetime.datetime.now()
                log.user1 = args[1]
                log.extra = args[2]
                log.save()
            elif args[0] == "Created" or args[0] == "Updated":
                if isinstance(args[2], Person):
                    log = Logger()
                    log.type = args[0]
                    log.timestamp = datetime.datetime.now()
                    log.user1 = args[1]
                    log.user2 = args[2]
                    log.hospital1 = args[3]
                    log.save()
                elif type(args[2]) == Appointment:
                    log = Logger()
                    log.type = args[0]
                    log.timestamp = datetime.datetime.now()
                    log.user1 = args[1]
                    log.appt = args[2]
                    log.hospital1 = args[3]
                    log.save()
                elif type(args[2]) == Prescription:
                    log = Logger()
                    log.type = args[0]
                    log.timestamp = datetime.datetime.now()
                    log.user1 = args[1]
                    log.extra = args[2]
                    log.hospital1 = args[3]
                    log.save()                    
                elif type(args[2]) == testResults:
                    log = Logger()
                    log.type = args[0]
                    log.timestamp = datetime.datetime.now()
                    log.user1 = args[1]
                    log.testResults = args[2]
                    log.hospital1 = args[3]
                    log.save()
                elif type(args[2]) == MedicalHistory:
                    log = Logger()
                    log.type = args[0]
                    log.timestamp = datetime.datetime.now()
                    log.user1 = args[1]
                    log.MedicalHistory = args[2]
                    log.hospital1 = args[3]
                    log.save()                    

                elif type(args[2]) == Hospital:
                    log = Logger()
                    log.type = args[0]
                    log.timestamp = datetime.datetime.now()
                    log.user1 = args[1]
                    log.hospital1 = args[3]
                    log.save()

            elif args[0] == "Removed":
                log = Logger()
                log.type = args[0]
                log.timestamp = datetime.datetime.now()
                log.user1 = args[1]
                log.extra = args[2]
                log.hospital1 = args[3]
                log.save()

            elif args[0] == "Message":
                log = Logger()
                log.type = args[0]
                log.timestamp = datetime.datetime.now()
                log.user1 = args[1]
                log.user2 = args[2]
                log.save()
                print('in')
            elif args[0] == "Released test":
                log = Logger()
                log.type = args[0]
                log.timestamp = datetime.datetime.now()
                log.user1 = args[1]
                log.testResults = args[2]
                log.hospital1 = args[3]
                log.save()
            elif args[0] == "Viewed":
                log = Logger()
                log.type = args[0]
                log.timestamp = datetime.datetime.now()
                log.user1 = args[1]
                log.user2 = args[2]
                log.hospital1 = args[3]
                log.save()
            elif args[0] == "Admitted":
                log = Logger()
                log.type = args[0]
                log.timestamp = datetime.datetime.now()
                log.user1 = args[1]
                log.user2 = args[2]
                log.hospital1 = args[3]
                log.save()     
            elif args[0] == "Released":
                log = Logger()
                log.type = args[0]
                log.timestamp = datetime.datetime.now()
                log.user1 = args[1]
                log.user2 = args[2]
                log.hospital1 = args[3]
                log.save()                 
        elif len(args) == 5:
            log = Logger()
            log.type = args[0]
            log.timestamp = datetime.datetime.now()
            log.user1 = args[1]
            log.user2 = args[2]
            log.hospital1 = args[3]
            log.hospital1 = args[4]
            log.save()

    """
    gets the first statistic: The number of patients visiting the hospital
    if hop is null it calculates the stat system wide
    """

    @staticmethod
    def getVisits(date1, date2, hop):
        count = 0
        if hop is none:
            for visit in Appointment.object.all():
                if visit.aptDate >= date1 and visit.aptDate <= date2:
                    stay = ExtendedStay.object.get(appointmentID=visit.id)
                    if stay is not none:
                        count += stay.endDate - visit.aptDate
                    else:
                        count += 1

        else:
            for visit in Appointment.object.all():
                doc = Doctor.object.get(id=visit.doctorID)
                if doc.hospitalID == hop and visit.aptDate >= date1 and visit.aptDate <= date2:
                    stay = ExtendedStay.object.get(appointmentID=visit.id)
                    if stay is not none:
                        count += stay.endDate - visit.aptDate
                    else:
                        count += 1
        return count

    """
    get the second stat: The average number of visits per patient
    if hop is null it calculates the stat system wide 
    """

    @staticmethod
    def getAverageVisit(date1, date2, hop):
        count = 0
        ppl = set()
        if hop is none:
            for visit in Appointment.object.all():
                if visit.aptDate >= date1 and visit.aptDate <= date2:
                    stay = ExtendedStay.object.get(appointmentID=visit.id)
                    ppl.add(visit.patientID)
                    if stay is not none:
                        count += stay.endDate - visit.aptDate
                    else:
                        count += 1

        else:
            for visit in Appointment.object.all():
                doc = Doctor.object.get(id=visit.doctorID)
                if doc.hospitalID == hop and visit.aptDate >= date1 and visit.aptDate <= date2:
                    stay = ExtendedStay.object.get(appointmentID=visit.id)
                    ppl.add(visit.patientID)
                    if stay is not none:
                        count += stay.endDate - visit.aptDate
                    else:
                        count += 1

        return count / len(ppl)

    """
    get the second stat: The average number of days a patient stays at a hospital (from admission to discharge)
    if hop is null it calculates the stat system wide 
    """

    @staticmethod
    def getAverageStay(date1, date2, hop):
        count = 0
        num = 0
        if hop is none:
            for visit in Appointment.object.all():
                if visit.aptDate >= date1 and visit.aptDate <= date2:
                    stay = ExtendedStay.object.get(appointmentID=visit.id)
                    if stay is not none:
                        count += stay.endDate - visit.aptDate
                        num += 1


        else:
            for visit in Appointment.object.all():
                doc = Doctor.object.get(id=visit.doctorID)
                if doc.hospitalID == hop and visit.aptDate >= date1 and visit.aptDate <= date2:
                    stay = ExtendedStay.object.get(appointmentID=visit.id)
                    if stay is not none:
                        count += stay.endDate - visit.aptDate
                        num += 1

        return count / num
