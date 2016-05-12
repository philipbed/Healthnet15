"""
    Application: HealthNet
    File: hospital/views.py
    Authors:
        - Nathan Stevens
        - Phillip Bedward
        - Daniel Herzig
        - George Herde
        - Samuel Launt

    Description:
        - This file contains all the view for the hospital functionality
"""
from base.views import group_required
from base.models import Hospital, Logger, Person
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import UpdateView
from .forms import *


# Create your views here.
@login_required
def hospitalRedirect(request):
    return redirect(reverse('hospital:view'), permanent=True)


@login_required
@group_required('Root')
def createHospital(request):
    """
    @function: createHospital
    @description: This function handles a request for creating a hospital.

    """
    # Boolean for successful schedule
    creation_success = False
    if request.method == 'POST':
        hospitalForm = HospitalForm(request.POST)
        addressForm = AddressForm(request.POST)

        # Get the valid data from the form
        if (hospitalForm.is_valid() and addressForm.is_valid()):

            addr = addressForm.save()
            addr.save()

            hosp = hospitalForm.save()
            hosp.address = addr
            hosp.save()

            logUser = User.objects.get_by_natural_key(request.user)
            logPerson = Person.objects.get(user=logUser)
            Logger.createLog('Created',logPerson,hosp,hosp)
            Group.objects.create(name=str(hosp))
            return HttpResponseRedirect(reverse('hospital:view'))
        else:
            pass

    else:
        hospitalForm = HospitalForm()
        addressForm = AddressForm()

    context = {'hospitalForm': hospitalForm,
               'addressForm': addressForm,
               'creation_success': creation_success,
               }
    return render(request, 'hospital/create.html', context)


@login_required
@group_required('Root')
def viewHospitals(request):
    is_root = request.user.groups.filter(name='Root').exists()
    all_hospitals = Hospital.objects.all()
    context = {'all_hospitals': all_hospitals,
               'is_root': is_root}
    return render(request, 'hospital/view.html', context)


@login_required
@group_required('Root')
def deleteHospital(request, **kwargs):
    hospitalID = kwargs.get('pk')
    hospitalModel = Hospital.objects.get(id=hospitalID)
    if request.method == 'POST':
        form = DeleteHospital(request.POST, instance=hospitalModel)
        if form.is_valid():
            logUser = User.objects.get_by_natural_key(request.user)
            logPerson = Person.objects.get(user=logUser)
            Logger.createLog('Removed',logPerson,str(Hospital.objects.get(id=hospitalID)),None)
            Hospital.objects.get(id=hospitalID).delete()
            # Only have to delete use because doing so deletes linked information
            # Specifically: Address

            return HttpResponseRedirect(reverse('hospital:view'))
    else:
        form = DeleteHospital(instance=hospitalModel)

    context = {'form': form, 'hospitalID': hospitalID, 'hospital': hospitalModel}
    return render(request, 'hospital/delete.html', context)


class updateHospital(UpdateView):
    model = Hospital
    template_name_suffix = '_form'
    template_name = 'hospital/hospital_form.html'
    success_url = reverse_lazy('hospital:view')
    fields = ('name', 'address')

    # Todo figure out how to do the updated system log event for default view classes
    @method_decorator(login_required)
    @method_decorator(group_required('Root'))
    def dispatch(self, *args, **kwargs):
        return super(updateHospital, self).dispatch(*args, **kwargs)
