import datetime
from django.contrib.auth.models import User
from django.db import models

from markdown import markdown
from speeches import utils

# managers

class SpeechManager(models.Manager):
    def live(self):
        return self.filter(status__exact=self.model.LIVE_STATUS)

# models

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
    

class Footnote(models.Model):
    "A footnote attached to a speech"
    speech = models.ForeignKey(Speech, related_name="footnotes")
    author = models.ForeignKey(User)
    index = models.IntegerField(default=-1)
    text = models.TextField("Note")
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        get_latest_by = "created"
        ordering = ('index', '-created')
    
    def __unicode__(self):
        return u"%s: %s..." % (self.author, self.text[:30])
    
    def get_absolute_url(self):
        return u"%s#p%s" % (self.speech.get_absolute_url(), self.index)
