from django import forms
from speeches.models import Footnote

class FootnoteForm(forms.ModelForm):
    
    class Meta:
        model = Footnote
        # exclude = ('author', 'index')