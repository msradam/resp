from django.shortcuts import render
from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from django.conf import settings
import json
# Create your views here.


class Fill(views.APIView):

    def post(self, request):
        req_dict = dict(request.data)
        with open(settings.BASE_DIR + "/status/people_db.json", "r") as jf:
            people_db = json.load(jf)
            people_db.append(req_dict)
        with open(settings.BASE_DIR + "/status/people_db.json", "w") as jf:
            json.dump(people_db, jf)
        return Response(status=status.HTTP_200_OK)

    def get(self, request, format=None):
        with open(settings.BASE_DIR + "/status/people_db.json", "r") as jf:
            people_db = json.load(jf)
        return Response(people_db)
