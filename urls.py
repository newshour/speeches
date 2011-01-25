from django.conf.urls.defaults import *
from django.views.generic import date_based, list_detail

from speeches import views
from speeches.models import Speech

speech_archive_dict = {
    'queryset': Speech.objects.live(),
    'paginate_by': 10
}

urlpatterns = patterns('',
    url(r'^api/', include('speeches.api.urls')),
    
    url(r'^$',
        views.speech_index,
        name="speeches_archive_index"
        ),
        
    url(r'(?P<object_id>\d+)/annotate/$',
        views.annotate_speech,
        name="speeches_speech_annotate"
        ),
    
    url(r'^(?P<object_id>\d+)/add/$',
        views.add_footnote,
        name="speeches_footnote_add"
        ),
        
    url(r'^(?P<object_id>\d+)/(?P<slug>[-\w]+)/$',
        views.speech_detail,
        name="speeches_speech_detail"
        ),
    
    url(r'(?P<object_id>\d+)/$',
        views.speech_detail,
        name="speeches_speech_detail_simple"
        ),
)
