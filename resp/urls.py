from django.contrib import admin
from django.conf.urls import url, include

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^survey/', include('survey.urls')),
    url(r'^status/', include('status.urls')),
    url(r'^services/', include('services.urls')),
]
