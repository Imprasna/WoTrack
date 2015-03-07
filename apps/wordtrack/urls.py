from django.conf.urls import url
from apps.wordtrack.views import WordTrackView

urlpatterns = [
    url(r'^$', WordTrackView.as_view(), name='home'),
]
