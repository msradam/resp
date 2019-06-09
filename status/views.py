import json

from django.conf import settings
from django.shortcuts import render
from rest_framework import status, views
from rest_framework.response import Response
from .illness_risk_predictor import *
# Create your views here.
from joblib import dump, load
model_anxiety = load("illness_model_anxiety.joblib")
model_ptsd = load("illness_model_ptsd.joblib")
model_depression = load("illness_model_depression.joblib")


class Status(views.APIView):
    def get(self, request):
        with open(settings.BASE_DIR + "/status/people_db.json", 'r') as jf:
            people_db = json.load(jf)
            for person in list(people_db.keys()):
                new_data = [people_db[person]['Wellbeing']
                            ['q5'], people_db[person]['Wellbeing']['q6']]
                people_db[person]['Individual']['Anxiety Risk'] = check_illness_risks(
                    new_data, model_anxiety)
                people_db[person]['Individual']['PTSD Risk'] = check_illness_risks(
                    new_data, model_ptsd)
                people_db[person]['Individual']['Depression Risk'] = check_illness_risks(
                    new_data, model_depression)
        return Response(people_db)

    def post(self, request, format=None):
        query_person = request.data.pop('name_to_search')
        with open(settings.BASE_DIR + "/status/people_db.json", "r") as jf:
            people_db = json.load(jf)
            people_db[query_person]['Individual']['checked_in'] = True
        with open(settings.BASE_DIR + "/status/people_db.json", "w") as jf:
            json.dump(people_db, jf)
        return Response(status=status.HTTP_200_OK)
