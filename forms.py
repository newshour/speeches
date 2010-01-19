from django import forms
from speech.models import Footnote

class FootnoteForm(forms.ModelForm):
    
    class Meta:
        model = Footnote
        exclude = ('author', 'index')