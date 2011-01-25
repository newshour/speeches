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
        'author_info',
        ('note_type', 
            ('name', 'slug'),
        ),
        # ('author', 
            #(
            #    'profile', (
            #        'first_name',
            #        'last_name',
            #        'bio',
            #    ),
        #    ),
        # ),
    )
    
    def read(self, request, speech_id):
        try:
            speech = Speech.objects.live().get(pk=speech_id)
        except Speech.DoesNotExist:
            return rc.DOES_NOT_EXIST
        
        return speech.footnotes.live().select_related()
    
    @staticmethod
    def author_info(footnote):
        try:
            a = footnote.author.profile
            return {
                'first_name': a.first_name,
                'last_name' : a.last_name,
                'full_name' : a.user.get_full_name(),
                'id'        : a.id,
                'title'     : a.title,
                'bio'       : a.bio,
                'thumbnail' : a.image.thumbnail.url
            }
        except:
            a = footnote.author
            return {
                'first_name': a.first_name,
                'last_name' : a.last_name,
                'full_name' : a.get_full_name()
            }