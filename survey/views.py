from django.shortcuts import render
from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
# Create your views here.


class Fill(views.APIView):
    def post(self, request):
        name = request.data.pop('person_name')
        return Response(status=status.HTTP_200_OK)
