from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from backend.models import User


def login(request):
    if request.method == 'POST':
        if request.POST.get('guest_email') and request.POST.get('guest_password'):
            user = User()
            email = request.POST.get('guest_email')
            password = request.POST.get('guest_password')
            user.email = request.POST.get('guest_email')
            user.password = request.POST.get('guest_password')
            print(email)
            print(password)
            user.save()

        return render(request, 'login_page.html')

    else:
        return render(request, 'login_page.html')