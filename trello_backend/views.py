from django.shortcuts import render
import json

# Create your views here.

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def login(request):
    jsonReqData = json.loads(request.body)
    jsonRes = JsonResponse(jsonReqData)
    jsonRes["Access-Control-Allow-Origin"] = "*"
    return jsonRes
