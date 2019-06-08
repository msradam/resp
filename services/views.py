from django.shortcuts import render
from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from django.http import JsonResponse
# Create your views here.
import json
from django.conf import settings


class List(views.APIView):
    def post(self, request):

        lat = request.data.pop("lat")
        lon = request.data.pop("lon")
        with open(settings.BASE_DIR + "/services/services_db.json", 'r') as jf:
            services_db = json.load(jf)
            services_db["lat"] = lat
            services_db["lon"] = lon
        with open(settings.BASE_DIR + "/services/services_db.json", 'w') as jf:
            json.dump(services_db, jf)
        return Response(status=status.HTTP_200_OK)

    def get(self, request):
        with open(settings.BASE_DIR + "/services/services_db.json") as jf:
            services_db = json.load(jf)
        return Response(services_db)
