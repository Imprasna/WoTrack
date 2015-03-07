from django.conf.urls import include, url
from django.contrib import admin
import apps.wordtrack.urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(apps.wordtrack.urls), name='wordtrack'),
]
