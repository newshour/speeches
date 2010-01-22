import datetime
import urlparse
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from markdown import markdown
from speeches import utils

# managers

class SpeechManager(models.Manager):
    def live(self):
        return self.filter(status__exact=self.model.LIVE_STATUS)

class FootnoteManager(models.Manager):
    from django.utils import simplejson
    def json(self):
        pass

# models

def get_default_note_type():
    try:
        return FootnoteType.objects.all()[0]
    except IndexError: # no types
        return None


class Speech(models.Model):
    "A speech with a date, speaker, description and transcript"
    DRAFT_STATUS = 1
    LIVE_STATUS = 2
    HIDDEN_STATUS = 3
    STATUS_CHOICES = (
        (DRAFT_STATUS, 'Draft'),
        (LIVE_STATUS, 'Live'),
        (HIDDEN_STATUS, 'Hidden'),
    )
    
    # metadata
    added_by = models.ForeignKey(User)
    date = models.DateTimeField(default=datetime.datetime.now)
    speaker = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=DRAFT_STATUS)
    
    # text
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique_for_date='date')
    transcript = models.TextField()
    transcript_html = models.TextField(blank=True, editable=False)
    
    objects = SpeechManager()
    
    class Meta:
        get_latest_by = "date"
        ordering = ('-date',)
        verbose_name_plural = "Speeches"
        
    def __unicode__(self):
        return self.title
    
    def save(self):
        self.transcript_html = markdown(self.transcript)
        self.transcript_html = utils.enumerate_paras(self.transcript_html)
        super(Speech, self).save()
    
    @models.permalink
    def get_absolute_url(self):
        return ("speeches_speech_detail", None, {'object_id': self.id, 'slug': self.slug})
    

class FootnoteType(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    
    class Meta:
        ordering = ('name',)
    
    def __unicode__(self):
        return self.name
    
    @property
    def icon(self):
        url = urlparse.urljoin(settings.MEDIA_URL, '/img/speeches/icons/%s.png')
        return url % self.slug


class Footnote(models.Model):
    "A footnote attached to a speech"
    speech = models.ForeignKey(Speech, related_name="footnotes")
    author = models.ForeignKey(User)
    note_type = models.ForeignKey(FootnoteType, default=get_default_note_type)
    index = models.IntegerField()
    text = models.TextField("Note")
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        get_latest_by = "created"
        ordering = ('index', 'created')
    
    def __unicode__(self):
        return u"%s: %s..." % (self.author, self.text[:30])
    
    def get_absolute_url(self):
        return u"%s#p%s" % (self.speech.get_absolute_url(), self.index)
    
    def render(self):
        from django.template.loader import render_to_string
        return render_to_string(
            ['speeches/footnote_%s.html' % self.note_type.slug, 'speeches/footnote_comment.html'],
            {'footnote': self}
        )


