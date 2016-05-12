from django import template
from django.contrib.auth.models import User

register = template.Library()


@register.filter(name="isDoctor")
def isDoctor(request):
    return request.user.groups.filter(name='Doctor').exists()


@register.filter(name="isNurse")
def isNurse(request):
    return request.user.groups.filter(name='Nurse').exists()


@register.filter(name="isAdmin")
def isAdmin(request):
    return request.user.groups.filter(name='Admin').exists()


@register.filter(name="isRoot")
def isRoot(request):
    return request.user.groups.filter(name='Root').exists()


@register.filter(name="isPatient")
def isPatient(request):
    return request.user.groups.filter(name='Patient').exists()


@register.filter(name="currUser")
def currentUser(request, user):
    currentUser = User.objects.get_by_natural_key(request.user.username)
    return currentUser == user


@register.filter(name="rowSpan")
def rowSpan(item):
    return len(item)+1
