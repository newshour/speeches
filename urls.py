from django.conf.urls.defaults import *
from django.views.generic import date_based, list_detail

from speeches import views
from speeches.models import Speech

speech_archive_dict = {
    'queryset': Speech.objects.live(),
    'paginate_by': 10
}

urlpatterns = patterns('',
    url(r'^$',
        list_detail.object_list,
        speech_archive_dict,
        name="speeches_archive_index"
        ),
        
    url(r'^(?P<object_id>\d+)/(?P<slug>[-\w]*)/$',
        views.speech_detail,
        name="speeches_speech_detail"
        ),
)