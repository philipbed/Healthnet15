from django.shortcuts import redirect


# Create your views here.
def redirectLanding(request):
     return redirect("http://127.0.0.1:8000/healthnet/home/", permanent=True)

def redirectAdmin(request):
    return redirect('http://127.0.0.1:8000/healthnet/admin/', permanent=True)