from django.conf.urls.defaults import *
from django.views.generic import date_based

from speeches.models import Speech

speech_archive_dict = {
    'queryset': Speech.objects.live(),
    'date_field': 'date'
}

urlpatterns = patterns('',
    url(r'^$',
        date_based.archive_index,
        speech_archive_dict,
        name="speeches_archive_index"
        ),
        
    url(r'^(?P<year>\d{4})/(?P<month>[a-zA-Z]{3})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$',
        date_based.object_detail,
        speech_archive_dict,
        name="speeches_speech_detail"
        ),
)