from survey.views import Fill
from django.conf.urls import url

app_name = 'survey'

urlpatterns = [
    url(r'^fill/$', Fill.as_view(), name="fill"),
]
