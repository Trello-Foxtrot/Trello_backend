from django.http import HttpResponse

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from backend.models import User


@csrf_exempt
def login(request):
    user = User()
    user.email = request.POST.get('email')
    user.password = request.POST.get('password')

    res = HttpResponse()
    res['Access-Control-Allow-Origin'] = '*'
    res['Access-Control-Expose-Headers'] = '*'
    if User.objects.filter(email=user.email).filter(password=user.password):
        res['email'] = ''
    else:
        res['email'] = "Email or password is incorrect"

    return res


@csrf_exempt
def sign_up(request):
    user = User()
    user.email = request.POST.get('email')
    user.password = request.POST.get('password')

    res = HttpResponse()
    res['Access-Control-Allow-Origin'] = '*'
    res['Access-Control-Expose-Headers'] = '*'
    if not User.objects.filter(email=user.email):
        user.save()
        res['email'] = ''
    else:
        res['email'] = 'User already exists'

    return res

