from services.views import List
from django.conf.urls import url

app_name = 'services'

urlpatterns = [
    url(r'^list/$', List.as_view(), name="list"),
]
