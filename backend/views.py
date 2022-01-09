import base64
import json
from io import BytesIO

from dateutil import parser
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.files import File
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt

from backend.models import Workspace, Admin, Member, Board, List, Card, Comment, Attachment


def add_headers(res, req):
    res['Access-Control-Allow-Origin'] = req.headers['Origin']
    res['Access-Control-Expose-Headers'] = '*'
    res['Access-Control-Allow-Credentials'] = 'true'
    res[
        'Access-Control-Allow-Headers'] = 'access-control-allow-origin, access-control-expose-headers, access-control-allow-credentials, content-type'
    return res


@csrf_exempt
def sign_in(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        res_data = {}

        res = HttpResponse(content_type="application/json; charset=UTF-8")
        res = add_headers(res, request)

        email = data['email']
        password = data['password']
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            res_data['email'] = ""
        else:
            res_data['email'] = "Email or password is incorrect"

        res.write(json.dumps(res_data))
        return res

    res = HttpResponse()
    res = add_headers(res, request)
    return res


@csrf_exempt
def sign_up(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        res_data = {}

        email = data['email']
        password = data['password']

        res = HttpResponse(content_type="application/json; charset=UTF-8")
        res = add_headers(res, request)

        if not User.objects.filter(username=email).exists():
            user = User.objects.create_user(email, email, password)
            user.save()
            login(request, user)
            res_data['email'] = ''
        else:
            res_data['email'] = 'User already exists'

        res.write(json.dumps(res_data))
        return res

    res = HttpResponse()
    res = add_headers(res, request)
    return res


@csrf_exempt
def get_workspace(request):
    if request.method == 'POST':
        res_data = {}

        res = HttpResponse(content_type="application/json; charset=UTF-8")
        res = add_headers(res, request)

        w_admin = Admin.objects.filter(user__username=request.user.username).values_list('workspace__name',
                                                                                         'workspace__pk')
        w_guest = Member.objects.filter(user__username=request.user.username).values_list('workspace__name',
                                                                                          'workspace__pk')

        res_data['admin'] = []
        res_data['admin_id'] = []
        for w in w_admin:
            res_data['admin'].append(w[0])
            res_data['admin_id'].append(str(w[1]))

        res_data['guest'] = []
        res_data['guest_id'] = []
        for w in w_guest:
            res_data['guest'].append(w[0])
            res_data['guest_id'].append(str(w[1]))

        res.write(json.dumps(res_data))
        return res

    res = HttpResponse()
    res = add_headers(res, request)
    return res


@csrf_exempt
def add_workspace(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))

        res = HttpResponse(content_type="application/json; charset=UTF-8")
        res = add_headers(res, request)

        new_workspace = Workspace(name=data['name'])
        admin = Admin(user=request.user, workspace=new_workspace)
        new_workspace.save()
        admin.save()

        return res

    res = HttpResponse()
    res = add_headers(res, request)
    return res


@csrf_exempt
def delete_workspace(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))

        res = HttpResponse(content_type="application/json; charset=UTF-8")
        res = add_headers(res, request)

        Admin.objects.get(
            user__username=request.user.username,
            workspace__pk=data['workspace_id']
        ).delete()

        return res

    res = HttpResponse()
    res = add_headers(res, request)
    return res


@csrf_exempt
def rename_workspace(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))

        res = HttpResponse(content_type="application/json; charset=UTF-8")
        res = add_headers(res, request)

        workspace = Admin.objects.get(
            user__username=request.user.username,
            workspace__pk=data['workspace_id']
        ).workspace

        workspace.name = data['new_name']
        workspace.save()

        return res

    res = HttpResponse()
    res = add_headers(res, request)
    return res


@csrf_exempt
def get_workspace_members(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        res_data = {}

        res = HttpResponse(content_type="application/json; charset=UTF-8")
        res = add_headers(res, request)

        members = []
        try:
            members.append(
                Admin.objects.get(workspace__pk=data['workspace_id']).user.username
            )
        except:
            pass

        members += Member.objects.filter(workspace__pk=data['workspace_id']).values_list('user__username')

        res_data['members'] = []
        for m in members:
            res_data['members'].append(m)

        res.write(json.dumps(res_data))
        return res

    res = HttpResponse()
    res = add_headers(res, request)
    return res


@csrf_exempt
def get_boards(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        res_data = {}

        res = HttpResponse(content_type="application/json; charset=UTF-8")
        res = add_headers(res, request)

        try:
            boards = Board.objects.filter(workspace__pk=data['workspace_id']).values_list('pk', 'name')
        except:
            boards = []
            pass

        res_data['boards'] = []
        res_data['boards_id'] = []
        for b in boards:
            res_data['boards'].append(b[1])
            res_data['boards_id'].append(str(b[0]))

        res.write(json.dumps(res_data))
        return res

    res = HttpResponse()
    res = add_headers(res, request)
    return res


@csrf_exempt
def add_board(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        res_data = {}

        res = HttpResponse(content_type="application/json; charset=UTF-8")
        res = add_headers(res, request)

        workspace = Workspace.objects.get(pk=data["workspace_id"])
        if Admin.objects.get(user=request.user, workspace=workspace):
            Board(
                workspace=workspace,
                name=data["name"]
            ).save()

        res.write(json.dumps(res_data))
        return res

    res = HttpResponse()
    res = add_headers(res, request)
    return res


@csrf_exempt
def delete_board(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        res_data = {}

        res = HttpResponse(content_type="application/json; charset=UTF-8")
        res = add_headers(res, request)

        Board.objects.get(
            pk=data['board_id']
        ).delete()

        res.write(json.dumps(res_data))
        return res

    res = HttpResponse()
    res = add_headers(res, request)
    return res


@csrf_exempt
def rename_board(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        res_data = {}

        res = HttpResponse(content_type="application/json; charset=UTF-8")
        res = add_headers(res, request)

        board = Board.objects.get(
            pk=data['board_id']
        )
        board.name = data['new_name']
        board.save()

        res.write(json.dumps(res_data))
        return res

    res = HttpResponse()
    res = add_headers(res, request)
    return res


@csrf_exempt
def get_lists(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        res_data = {}

        res = HttpResponse(content_type="application/json; charset=UTF-8")
        res = add_headers(res, request)

        try:
            lists = List.objects.filter(board__pk=data['board_id']).values_list('pk', 'name')
        except:
            lists = []

        res_data['lists'] = []
        res_data['lists_id'] = []
        res_data['cards'] = []
        res_data['cards_id'] = []
        for il, l in enumerate(lists):
            res_data['lists'].append(l[1])
            res_data['lists_id'].append(str(l[0]))

            res_data['cards'].append([])
            res_data['cards_id'].append([])
            cards = Card.objects.filter(list__pk=l[0]).values_list('pk', 'name')
            for c in cards:
                res_data['cards'][il].append(c[1])
                res_data['cards_id'][il].append(str(c[0]))

        res.write(json.dumps(res_data))
        return res

    res = HttpResponse()
    res = add_headers(res, request)
    return res


@csrf_exempt
def add_list(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        res_data = {}

        res = HttpResponse(content_type="application/json; charset=UTF-8")
        res = add_headers(res, request)

        List(
            name=data['name'],
            board=Board.objects.get(pk=data['board_id'])
        ).save()

        res.write(json.dumps(res_data))
        return res

    res = HttpResponse()
    res = add_headers(res, request)
    return res


@csrf_exempt
def delete_list(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        res_data = {}

        res = HttpResponse(content_type="application/json; charset=UTF-8")
        res = add_headers(res, request)

        List.objects.get(
            pk=data['list_id']
        ).delete()

        res.write(json.dumps(res_data))
        return res

    res = HttpResponse()
    res = add_headers(res, request)
    return res


@csrf_exempt
def rename_list(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        res_data = {}

        res = HttpResponse(content_type="application/json; charset=UTF-8")
        res = add_headers(res, request)

        list = List.objects.get(
            pk=data['list_id']
        )
        list.name = data['new_name']
        list.save()

        res.write(json.dumps(res_data))
        return res

    res = HttpResponse()
    res = add_headers(res, request)
    return res


@csrf_exempt
def add_card(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        res_data = {}

        res = HttpResponse(content_type="application/json; charset=UTF-8")
        res = add_headers(res, request)

        Card(
            name=data['name'],
            list=List.objects.get(pk=data['list_id']),
        ).save()

        res.write(json.dumps(res_data))
        return res

    res = HttpResponse()
    res = add_headers(res, request)
    return res


@csrf_exempt
def delete_card(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        res_data = {}

        res = HttpResponse(content_type="application/json; charset=UTF-8")
        res = add_headers(res, request)

        Card.objects.get(
            pk=data['card_id']
        ).delete()

        res.write(json.dumps(res_data))
        return res

    res = HttpResponse()
    res = add_headers(res, request)
    return res


@csrf_exempt
def rename_card(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        res_data = {}

        res = HttpResponse(content_type="application/json; charset=UTF-8")
        res = add_headers(res, request)

        card = Card.objects.get(
            pk=data['card_id']
        )
        card.name = data['new_name']
        card.save()

        res.write(json.dumps(res_data))
        return res

    res = HttpResponse()
    res = add_headers(res, request)
    return res


@csrf_exempt
def get_card(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        res_data = {}

        res = HttpResponse(content_type="application/json; charset=UTF-8")
        res = add_headers(res, request)

        card = Card.objects.get(
            pk=data['card_id']
        )
        comments = Comment.objects.filter(
            card_id=data['card_id']
        )
        attachments = Attachment.objects.filter(
            card_id=data['card_id']
        )

        res_data['comments'] = [[c.user.email, c.text, str(c.id)] for c in comments]
        res_data['description'] = card.description
        res_data['attachments'] = [[a.name, str(a.id)] for a in attachments]

        if card.date is None:
            res_data['date'] = ""
        else:
            res_data['date'] = str(card.date)

        res.write(json.dumps(res_data))
        return res

    res = HttpResponse()
    res = add_headers(res, request)
    return res


@csrf_exempt
def redescribe_card(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        res_data = {}

        res = HttpResponse(content_type="application/json; charset=UTF-8")
        res = add_headers(res, request)

        card = Card.objects.get(
            pk=data['card_id']
        )
        card.description = data['new_description']
        card.save()

        res.write(json.dumps(res_data))
        return res

    res = HttpResponse()
    res = add_headers(res, request)
    return res


@csrf_exempt
def add_comment(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        res_data = {}

        res = HttpResponse(content_type="application/json; charset=UTF-8")
        res = add_headers(res, request)

        Comment(
            text=data['text'],
            card=Card.objects.get(pk=data['card_id']),
            user=request.user
        ).save()

        res.write(json.dumps(res_data))
        return res

    res = HttpResponse()
    res = add_headers(res, request)
    return res


@csrf_exempt
def delete_comment(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        res_data = {}

        res = HttpResponse(content_type="application/json; charset=UTF-8")
        res = add_headers(res, request)

        Comment.objects.get(
            pk=data['comment_id']
        ).delete()

        res.write(json.dumps(res_data))
        return res

    res = HttpResponse()
    res = add_headers(res, request)
    return res


@csrf_exempt
def set_date(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        res_data = {}

        res = HttpResponse(content_type="application/json; charset=UTF-8")
        res = add_headers(res, request)

        card = Card.objects.get(
            pk=data['card_id']
        )
        if data['datetime'] != "":
            card.date = parser.parse(data['datetime'])
        else:
            card.date = None
        card.save()

        res.write(json.dumps(res_data))
        return res

    res = HttpResponse()
    res = add_headers(res, request)
    return res


@csrf_exempt
def add_attachment(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        res_data = {}

        res = HttpResponse(content_type="application/json; charset=UTF-8")
        res = add_headers(res, request)

        Attachment(
            name=data['name'],
            card_id=data['card_id'],
            file=File(BytesIO(base64.b64decode(data['file'])), name=data['name']),
        ).save()

        res.write(json.dumps(res_data))
        return res

    res = HttpResponse()
    res = add_headers(res, request)
    return res


@csrf_exempt
def delete_attachment(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        res_data = {}

        res = HttpResponse(content_type="application/json; charset=UTF-8")
        res = add_headers(res, request)

        Attachment(
            pk=data['attachment_id'],
        ).delete()

        res.write(json.dumps(res_data))
        return res

    res = HttpResponse()
    res = add_headers(res, request)
    return res
