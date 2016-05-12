from django import template
from django.contrib.auth.models import User

register = template.Library()

@register.filter(name="urlTime")
def urlTime(request):
    return "http://127.0.0.1:8000/healthnet/system/log/timedown"

