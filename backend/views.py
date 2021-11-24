from django.http import HttpResponse

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from backend.models import User, Workspace, Admin, Member


@csrf_exempt
def login(request):
    user = User()
    user.email = request.POST.get('email')
    user.password = request.POST.get('password')

    res = HttpResponse()
    res['Access-Control-Allow-Origin'] = '*'
    res['Access-Control-Expose-Headers'] = '*'
    if User.objects.filter(email=user.email).filter(password=user.password):
        request.session['email'] = user.email
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
        request.session['email'] = user.email
        res['email'] = ''
    else:
        res['email'] = 'User already exists'

    return res


@csrf_exempt
def get_workspaces(request):
    res = HttpResponse()
    res['Access-Control-Allow-Origin'] = '*'
    res['Access-Control-Expose-Headers'] = '*'

    w_admin = Admin.objects.get(user__email=request.session['email']).values_list('workspace__name')
    w_guest = Member.objects.get(user__email=request.session['email']).values_list('workspace__name')
    print(w_admin)
    print(w_guest)
    res['admin'] = w_admin.workspace
    res['guest'] = w_guest.workspace

    return None
    # return res


@csrf_exempt
def add_workspace(request):
    new_workspace = Workspace(name=request.POST.get('name'))
    admin = Admin(user=User.objects.get(email=request.session['email']), workspace=new_workspace)

    new_workspace.save()
    admin.save()
    return None
    # return res
