from piston.handler import BaseHandler
from piston.utils import rc

from speeches.models import Speech, Footnote, GuestProfile

class SpeechHandler(BaseHandler):
    
    allowed_methods = ('GET',)
    exclude = ('added_by', 'status')
    model = Speech
    
    def read(self, request, **kwargs):
        if 'speech_id' in kwargs:
            try:
                return Speech.objects.live().get(pk=kwargs['speech_id'])
            except Speech.DoesNotExist:
                return rc.DOES_NOT_EXIST
        
        return Speech.objects.live()
    
    def footnotes(self, speech):
        return speech.footnotes.live()


class FootnoteHandler(BaseHandler):
    
    allowed_methods = ('GET',)
    model = Footnote
    
    fields = (
        'index',
        'text',
        ('note_type', 
            ('name', 'slug'),
        ),
        ('author', 
            ('first_name', 'last_name'),
        ),
    )
    
    def read(self, request, speech_id):
        try:
            speech = Speech.objects.live().get(pk=speech_id)
        except Speech.DoesNotExist:
            return rc.DOES_NOT_EXIST
        
        return speech.footnotes.live().select_related()
        