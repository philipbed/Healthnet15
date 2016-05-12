from django.shortcuts import render
from .forms import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from base.models import Doctor, Patient, Person, testResults, Logger
from django.shortcuts import render, get_object_or_404
from base.views import group_required
# Create your views here.
@login_required
@group_required('Doctor')
def uploadResults( request ):
    currUser = request.user
    currPerson = Person.objects.get(user=currUser)
    currDoctor = Doctor.objects.get(personID=currPerson)

    if request.method == 'POST':
        form = TestUploadForm(request.POST,request.FILES)

        if form.is_valid():

            # resultFile = form.cleaned_data['results']
            # patient = form.cleaned_data['patient']
            # comments = form.cleaned_data['comments']
            # testResults.objects.create(results=resultFile,doctor=currDoctor,
            #                            patient=patient,comments=comments)

            testResult = form.save(commit=False)
            #testResults.objects.create(results=form.results,comments=form.comments)
            testResult.doctor = currDoctor
            testResult.save()
            Logger.createLog('Created',currUser,testResult,currDoctor.hospitalID)
            return HttpResponseRedirect(reverse("results:viewTestResults"))
        else:
            print(form.errors)
    else:
        form = TestUploadForm()
    context = {'doctor':currDoctor,'form':form}

    return render( request,'testResults/uploadResults.html',context )

@login_required
@group_required('Doctor','Patient')
def viewAllResults( request ):
    allResults = testResults.objects.all()
    currUser = request.user
    currPerson = Person.objects.get(user=currUser)
    if Patient.objects.filter(personID=currPerson).exists():
        currPatient = Patient.objects.get(personID=currPerson)

        # Grab the appts
        results = testResults.objects.all().filter(patient=currPatient)
        publishedResults = list( filter ( lambda x: x.published == True,results ) )
        context = {'results':publishedResults}
        return render(request, 'testResults/patientResults.html', context)

    elif Doctor.objects.filter(personID=currPerson).exists():
        currDoctor = Doctor.objects.get(personID=currPerson)

        # Grab the appts
        results = testResults.objects.filter(doctor=currDoctor)

        context = {'results':results}
        return render(request, 'testResults/results.html', context)

@login_required
@group_required('Patient')
def viewComments(request,pk):
    resultModel = get_object_or_404(testResults,id=pk)
    context = {'comments':resultModel.comments}
    return render(request,'testResults/viewComments.html',context)

@login_required
@group_required('Doctor')
def updateResults(request,pk):
    resultModel = get_object_or_404(testResults,id=pk)

    if request.method == 'POST':
        form = UpdateTestResultForm(request.POST,request.FILES,instance=resultModel)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("results:viewTestResults"))
        else:
            print(form.errors)
    else:
        form = UpdateTestResultForm(instance=resultModel)
    context = {'form':form,'id':resultModel.id}
    return render(request,'testResults/update.html',context)