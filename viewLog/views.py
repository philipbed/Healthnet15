from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
import os
from base.views import group_required
from base.models import Person, Logger, Root, Admin, Appointment, Doctor, ExtendedStay
from django.contrib.auth.models import User
from time import strptime
import datetime

from .forms import *


# Create your views here.
@login_required
@group_required('Admin', 'Root')
def listLog(request, **kwargs):
    """
    @function: listLog
    @description: Functionality for viewing the system log
    """
    user_model = User.objects.get_by_natural_key(request.user.username)
    person_model = Person.objects.get(user=user_model)

    if Root.objects.filter(personID=person_model).exists():
        startDate = kwargs.get('startDay')
        if startDate != None:
            start = datetime.datetime(int(str(startDate)[:4]), int(str(startDate)[4:6]),
                                      int(str(startDate)[6:]))
        else:
            start = datetime.datetime.today() - datetime.timedelta(weeks=100)

        endDate = kwargs.get('endDay')
        if endDate != None:
            end = datetime.datetime(int(str(endDate)[:4]), int(str(endDate)[4:6]),
                                    int(str(endDate)[6:]))
        else:
            end = datetime.datetime.today()

        log = Logger.objects.all().filter(timestamp__range=[start, end + datetime.timedelta(days=1)])

        order = kwargs.get('reverseTime')
        if order == None or int(order).__eq__(0):
            log = log.order_by('timestamp')
        elif int(order).__eq__(1):
            log = log.order_by('-timestamp')

        context = {'log': log}
        return render(request, 'viewLog/view.html', context)

    elif Admin.objects.filter(personID=person_model).exists():
        startDate = kwargs.get('startDay')
        if startDate != None:
            start = datetime.datetime(int(str(startDate)[:4]), int(str(startDate)[4:6]),
                                      int(str(startDate)[6:]))
        else:
            start = datetime.datetime.today() - datetime.timedelta(weeks=100)

        endDate = kwargs.get('endDay')
        if endDate != None:
            end = datetime.datetime(int(str(endDate)[:4]), int(str(endDate)[4:6]),
                                    int(str(endDate)[6:]))
        else:
            end = datetime.datetime.today()

        adminModel = Admin.objects.get(personID=person_model)
        log = Logger.objects.all().filter(hospital1=adminModel.hospitalID,
                                          timestamp__range=[start, end + datetime.timedelta(days=1)]) | \
              Logger.objects.all().filter(hospital2=adminModel.hospitalID,
                                          timestamp__range=[start, end + datetime.timedelta(days=1)])

        order = kwargs.get('reverseTime')
        if order == None or int(order).__eq__(0):
            log = log.order_by('timestamp')
        elif int(order).__eq__(1):
            log = log.order_by('-timestamp')

        context = {'log': log}
        return render(request, 'viewLog/view.html', context)

    else:
        return render(request, 'viewLog/view.html', {})


@login_required
@group_required('Admin', 'Root')
def filterLog(request, **kwargs):
    if request.method == 'POST':
        logFilterForm = logFilter(request.POST)

        if (logFilterForm.is_valid()):
            start = logFilterForm.cleaned_data['startDate']
            end = logFilterForm.cleaned_data['endDate']
            order = logFilterForm.cleaned_data['ascending']
            return redirect(reverse('systemLog:log', kwargs={"startDay": start, 'reverseTime': order, "endDay": end}))
        else:
            pass
    else:
        logFilterForm = logFilter()

    context = {'filterForm': logFilterForm}
    return render(request, 'viewLog/filter.html', context)


@login_required
@group_required('Admin', 'Root')
def stats(request, **kwargs):
    user_model = User.objects.get_by_natural_key(request.user.username)
    person_model = Person.objects.get(user=user_model)
    if kwargs.get('startDay') == None:
        start = datetime.datetime.today() - datetime.timedelta(weeks=100)
    else:
        start = datetime.datetime(int(str(kwargs.get('startDay'))[:4]), int(str(kwargs.get('startDay'))[4:6]),
                                  int(str(kwargs.get('startDay'))[6:]))
    if kwargs.get('endDay') == None:
        end = datetime.datetime.today()
    else:
        end = datetime.datetime(int(str(kwargs.get('endDay'))[:4]), int(str(kwargs.get('endDay'))[4:6]),
                                int(str(kwargs.get('endDay'))[6:]))

    if Root.objects.filter(personID=person_model).exists():
        if kwargs.get('hospital') == None:
            hospital = None
        else:
            hospital = Hospital.objects.get(pk=kwargs.get('hospital'))
    elif Admin.objects.filter(personID=person_model).exists():
        adminModel = Admin.objects.get(personID=person_model)
        hospital = adminModel.hospitalID
    else:
        hospital = None

    context = {'hospital': hospital,
               'startDay': datetime.date(year=start.year, month=start.month, day=start.day),
               'endDay': datetime.date(year=end.year, month=end.month, day=end.day),
               'visits': getVisits(start, end, hospital),
               'averageVisit': getAverageVisit(start, end, hospital),
               'averageStay': getAverageStay(start, end, hospital)}
    return render(request, 'viewLog/stats.html', context)


@login_required
@group_required('Admin', 'Root')
def filterStats(request, **kwargs):
    if request.method == 'POST':
        filterForm = statFilter(request.POST, hospital_filter=setHospitalFilter(request))

        if filterForm.is_valid():
            start = filterForm.cleaned_data['startDate']
            end = filterForm.cleaned_data['endDate']
            hospital = filterForm.cleaned_data['hospital']
            if hospital is not None:
                hospital = str(filterForm.cleaned_data['hospital'].id)
                return redirect(
                    reverse('systemLog:stats', kwargs={"startDay": start, "endDay": end, "hospital": hospital}))
            else:
                return redirect(reverse('systemLog:stats', kwargs={"startDay": start, "endDay": end}))
        else:
            context = {'filterForm': filterForm,
                       'stats': True}

    else:
        filterForm = statFilter(hospital_filter=setHospitalFilter(request))

        context = {'filterForm': filterForm,
                   'stats': True}
    return render(request, 'viewLog/filter.html', context)


def setHospitalFilter(request):
    if request.user.groups.filter(name='Root').exists():
        return None
    else:
        userModel = User.objects.get_by_natural_key(request.user.username)
        personModel = Person.objects.get(user=userModel)
        adminModel = Admin.objects.get(personID=personModel)
        return adminModel.hospitalID


def getVisits(date1, date2, hop):
    """
    The number of patients visiting the hospital
    if hop is null it calculates the stat system wide
    """
    count = 0
    for visit in Appointment.objects.all():
        doc = Doctor.objects.get(id=visit.doctorID.id)
        if doc.hospitalID == hop or hop == None:
            if visit.aptDate >= datetime.date(year=date1.year, month=date1.month,
                                              day=date1.day) and visit.aptDate <= datetime.date(year=date2.year,
                                                                                                month=date2.month,
                                                                                                day=date2.day):
                if ExtendedStay.objects.filter(appointmentID=visit.id).exists():
                    stay = ExtendedStay.objects.get(appointmentID=visit.id)
                    count += (stay.endDate - visit.aptDate).days
                else:
                    count += 1
    return count


def getAverageVisit(date1, date2, hop):
    """
    The average number of visits per patient
    if hop is null it calculates the stat system wide
    """
    count = 0
    ppl = set()
    for visit in Appointment.objects.all():
        doc = Doctor.objects.get(id=visit.doctorID.id)
        if doc.hospitalID == hop or hop == None:
            if visit.aptDate >= datetime.date(year=date1.year, month=date1.month,
                                              day=date1.day) and visit.aptDate <= datetime.date(year=date2.year,
                                                                                                month=date2.month,
                                                                                                day=date2.day):
                ppl.add(visit.patientID)
                if ExtendedStay.objects.filter(appointmentID=visit.id).exists():
                    stay = ExtendedStay.objects.get(appointmentID=visit.id)
                    count += (stay.endDate - visit.aptDate).days
                else:
                    count += 1
    personCount = len(ppl)
    if int(personCount).__eq__(0):
        return 0
    else:
        return count / len(ppl)


def getAverageStay(date1, date2, hop):
    """
    The average number of days a patient stays at a hospital (from admission to discharge)
    if hop is None it calculates the stat system wide
    """
    count = 0
    num = 0
    for visit in Appointment.objects.all():
        doc = Doctor.objects.get(id=visit.doctorID.id)
        if doc.hospitalID == hop or hop == None:
            if visit.aptDate >= datetime.date(year=date1.year, month=date1.month,
                                              day=date1.day) and visit.aptDate <= datetime.date(year=date2.year,
                                                                                                month=date2.month,
                                                                                                day=date2.day):
                if ExtendedStay.objects.filter(appointmentID=visit.id).exists():
                    stay = ExtendedStay.objects.get(appointmentID=visit.id)
                    count += (stay.endDate - visit.aptDate).days
                    num += 1
    if num == 0:
        return 0
    else:
        return count / num
