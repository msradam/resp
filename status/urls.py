from status.views import Status
from django.conf.urls import url

app_name = 'status'

urlpatterns = [
    url(r'^status/$', Status.as_view(), name="status"),
]
