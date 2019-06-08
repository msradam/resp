from django.shortcuts import render
from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
# Create your views here.


class Status(views.APIView):
    def get(self, request, format=None):
        people = {'name': 'Ava'}
        return Response(people)
