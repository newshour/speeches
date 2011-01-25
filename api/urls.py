from django.conf.urls.defaults import *
from piston.resource import Resource
from speeches.api.handlers import SpeechHandler, FootnoteHandler

speech_resource = Resource(SpeechHandler)
footnote_resource = Resource(FootnoteHandler)

urlpatterns = patterns('',
    url(r'^(?P<speech_id>\d+)/?$', speech_resource),
    url(r'^(?P<speech_id>\d+)/footnotes/?$', footnote_resource),
)