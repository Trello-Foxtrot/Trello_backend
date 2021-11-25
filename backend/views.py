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
def get_workspace(request):
    # debug
    request.session['email'] = 'a'

    res = HttpResponse()
    res['Access-Control-Allow-Origin'] = '*'
    res['Access-Control-Expose-Headers'] = '*'

    w_admin = Admin.objects.filter(user__email=request.session['email']).values_list('workspace__name', 'workspace__pk')
    w_guest = Member.objects.filter(user__email=request.session['email']).values_list('workspace__name',
                                                                                      'workspace__pk')

    res['admin'] = ""
    res['admin_id'] = ""
    for w in w_admin:
        res['admin'] += w[0] + ','
        res['admin_id'] += str(w[1]) + ','

    res['guest'] = ""
    res['guest_id'] = ""
    for w in w_guest:
        res['guest'] += w[0] + ','
        res['guest_id'] += str(w[1]) + ','

    return res


@csrf_exempt
def add_workspace(request):
    # debug
    request.session['email'] = 'a'

    res = HttpResponse()
    res['Access-Control-Allow-Origin'] = '*'
    res['Access-Control-Expose-Headers'] = '*'

    new_workspace = Workspace(name=request.POST.get('name'))
    admin = Admin(user=User.objects.get(email=request.session['email']), workspace=new_workspace)
    new_workspace.save()
    admin.save()
    return res


@csrf_exempt
def delete_workspace(request):
    # debug
    request.session['email'] = 'a'

    res = HttpResponse()
    res['Access-Control-Allow-Origin'] = '*'
    res['Access-Control-Expose-Headers'] = '*'

    Admin.objects.get(
        user__email=request.session['email'],
        workspace__pk=request.POST.get('id')
    ).delete()

    return res


@csrf_exempt
def rename_workspace(request):
    # debug
    request.session['email'] = 'a'

    res = HttpResponse()
    res['Access-Control-Allow-Origin'] = '*'
    res['Access-Control-Expose-Headers'] = '*'

    workspace = Admin.objects.get(
        user__email=request.session['email'],
        workspace__pk=request.POST.get('id')
    ).workspace
    print(workspace)
    workspace.name = request.POST.get('new_name')
    workspace.save()
    print(workspace.name)
    return res


@csrf_exempt
def get_workspace_members(request):
    # debug
    request.session['email'] = 'a'

    res = HttpResponse()
    res['Access-Control-Allow-Origin'] = '*'
    res['Access-Control-Expose-Headers'] = '*'

    members = []
    try:
        members.append(
            Admin.objects.get(workspace__pk=request.POST.get('id')).user.email
        )
    except:
        pass

    members += Member.objects.filter(workspace__pk=request.POST.get('id')).values_list('user__email')

    res['members'] = ""
    for m in members:
        res['members'] += m + ','

    return res


@csrf_exempt
def get_workspace_boards(request):
    # debug
    request.session['email'] = 'a'

    res = HttpResponse()
    res['Access-Control-Allow-Origin'] = '*'
    res['Access-Control-Expose-Headers'] = '*'

    boards = []
    try:
        boards.append(
            Admin.objects.get(
                user__email=request.session['email'],
                workspace__pk=request.POST.get('id')
            ).board.name
        )
    except:
        pass

    boards += Member.objects.filter(
            user__email=request.session['email'],
            workspace__pk=request.POST.get('id')
        ).values_list('board__name')

    res['boards'] = ""
    for b in boards:
        res['boards'] += b + ','

    return res
