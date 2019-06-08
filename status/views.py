import json

from django.conf import settings
from django.shortcuts import render
from rest_framework import status, views
from rest_framework.response import Response

# Create your views here.


class Status(views.APIView):
    def get(self, request):
        with open(settings.BASE_DIR + "/status/people_db.json", 'r') as jf:
            people_db = json.load(jf)
        return Response(people_db)

    def post(self, request, format=None):
        query_person = request.data.pop('name_to_search')
        with open(settings.BASE_DIR + "/status/people_db.json", "r") as jf:
            people_db = json.load(jf)
            for i in range(len(people_db)):
                if people_db[i]["name"] == query_person:
                    people_db[i]["checked_in"] = True
        with open(settings.BASE_DIR + "/status/people_db.json", "w") as jf:
            json.dump(people_db, jf)
        return Response(status=status.HTTP_200_OK)
