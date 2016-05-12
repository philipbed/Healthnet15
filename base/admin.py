from django.contrib import admin
from .models import *


class AdminPerson(admin.ModelAdmin):
    list_display = ('ssn', 'user', 'birthday', 'phoneNumber')


admin.site.register(Person, AdminPerson)


class AdminDoctor(admin.ModelAdmin):
    list_display = ('personID', 'licenseNumber', 'specialty')


admin.site.register(Doctor, AdminDoctor)


class AdminAddress(admin.ModelAdmin):
    list_display = ('street', 'city', 'state', 'zip')


admin.site.register(Address, AdminAddress)


class AdminPatient(admin.ModelAdmin):
    list_display = ('personID', 'addressID', 'insuranceID',
                    'emergencyContactID')


admin.site.register(Patient, AdminPatient)


class AdminNurse(admin.ModelAdmin):
    list_display = ('personID', 'license_number', 'department', 'hospitalID')


admin.site.register(Nurse, AdminNurse)


class AdminAdmin(admin.ModelAdmin):
    list_display = ('personID', 'hospitalID')


admin.site.register(Admin, AdminAdmin)


class AdminAppointment(admin.ModelAdmin):
    list_display = ('aptDate', 'aptTime', 'doctorID', 'patientID')
    
class AdminExtendedStay(admin.ModelAdmin):
    list_display = ('appointmentID', 'endDate', 'endTime')    


admin.site.register(Appointment, AdminAppointment)

admin.site.register(ExtendedStay, AdminExtendedStay)


class AdminInsurance(admin.ModelAdmin):
    list_display = ('name', 'addressID', 'policyNumber')


admin.site.register(Insurance, AdminInsurance)


class AdminHospital(admin.ModelAdmin):
    list_display = ('name', 'address')


admin.site.register(Hospital, AdminHospital)


class AdminRoot(admin.ModelAdmin):
    pass


admin.site.register(Root, AdminRoot)


class AdminEmergency(admin.ModelAdmin):
    list_display = ('personID', 'firstName', 'lastName', 'emergencyNumber')


admin.site.register(EmergencyContact, AdminEmergency)

admin.site.register(MedicalHistory)


class AdminLogger(admin.ModelAdmin):
    list_display = ('type', 'timestamp', 'user1', 'user2', 'appt', 'medHistory', 'testResults', 'hospital1',
                    'hospital2', 'extra')


admin.site.register(Logger, AdminLogger)


class AdminTestResults(admin.ModelAdmin):
    list_display = ('results', 'doctor', 'patient', 'comments')


admin.site.register(testResults, AdminTestResults)
