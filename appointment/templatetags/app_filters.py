from django import template

register = template.Library()

@register.filter(name="isPatient")
def isPatient(request):
    return request.user.groups.filter(name='Patient').exists()

@register.filter(name="isDoctor")
def isDoctor(request):
    return request.user.groups.filter(name='Doctor').exists()

@register.filter(name="isNurse")
def isNurse(request):
    return request.user.groups.filter(name='Nurse').exists()

@register.filter(name="isAdmin")
def isAdmin(request):
    if request.user.groups.filter(name='Admin').exists():
        return True
    elif request.user.is_staff:
        return True
    else:
        return False

@register.filter(name="isRoot")
def isRoot(request):
    return request.user.groups.filter(name='Root').exists()