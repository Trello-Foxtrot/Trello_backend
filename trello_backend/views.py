from django.shortcuts import render
import json

# Create your views here.

from django.http import JsonResponse


def login(request):
    jsonReqData = json.loads(request.body)
    jsonRes = JsonResponse(jsonReqData)
    jsonRes["Access-Control-Allow-Origin"] = "*"
    return jsonRes
