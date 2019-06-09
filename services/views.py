# Create your views here.
import json

from django.conf import settings
from django.shortcuts import render
from rest_framework import status, views
from rest_framework.response import Response

from .resources import *


class List(views.APIView):
    def post(self, request):
        lat = float(request.data.pop("lat"))
        lon = float(request.data.pop("lon"))
        country = request.data.pop("country")
        with open(settings.BASE_DIR + "/services/services_db.json", 'r') as jf:
            services_db = json.load(jf)
            services_db.append(
                {
                    "lat": lat,
                    "lon": lon,
                    "country": country,
                    "nearest_hospitals": find_nearest_hospitals(country, lat, lon)
                })
        with open(settings.BASE_DIR + "/services/services_db.json", 'w') as jf:
            json.dump(services_db, jf)
        return Response(status=status.HTTP_200_OK)

    def get(self, request):
        with open(settings.BASE_DIR + "/services/services_db.json") as jf:
            services_db = json.load(jf)
        if request.data:
            lat = float(request.data.pop("lat"))
            lon = float(request.data.pop("lat"))
            country = request.data.pop("country")
            final_response = []
            for entry in services_db:
                if entry["lat"] == lat and entry["lon"] == lon and entry["country"] == country:
                    final_response.append(entry)
            return Response(final_response)
        else:
            return Response(services_db)
