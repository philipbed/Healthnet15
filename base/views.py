from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
import logging

logger = logging.getLogger(__name__) 


# Create your views here.
def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""

    def in_groups(u):
        if u.is_authenticated():
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False

    return user_passes_test(in_groups)


def landingPage(request):
    logger.info(str("Landing Page accessed"))
    return render(request, 'index.html', {})


def redirectLanding(request):
    return redirect(reverse('base:landing'), permanent=True)
