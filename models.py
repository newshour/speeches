import datetime
import urlparse
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from backends.s3 import S3Storage
from imagekit.models import ImageModel, CROP_HORZ_CHOICES, CROP_VERT_CHOICES
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
    
    def live(self):
        return self.filter(public=True)

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
        return ("speeches_speech_detail", None, {'object_id': self.pk, 'slug': self.slug})
    
    def users(self):
        u_list = [f.author.pk for f in self.footnotes.all()]
        return User.objects.filter(pk__in=u_list)


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
    public = models.BooleanField(default=False)
    
    objects = FootnoteManager()
    
    class Meta:
        get_latest_by = "created"
        ordering = ('index', '-created')
    
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


class GuestProfile(models.Model):
    user = models.OneToOneField(User, related_name="profile")
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    title = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    image_url = models.URLField(max_length=255, blank=True)
    
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        get_latest_by = "date_added"
        ordering = ('last_name', 'first_name')
        
    def __unicode__(self):
        return self.user.get_full_name()
    
    def save(self):
        self.user.first_name, self.user.last_name = self.first_name, self.last_name
        self.user.save() # denormalized for easier editing
        super(GuestProfile, self).save()

    def admin_thumbnail_view(self):
        return self.image.admin_thumbnail_view()
    admin_thumbnail_view.short_description = "Thumbnail"
    admin_thumbnail_view.allow_tags = True

    def get_full_name(self):
        return u"%s %s" % (self.first_name, self.last_name)


class GuestProfileImage(ImageModel):
    guest = models.OneToOneField(GuestProfile, related_name="image")
    image = models.ImageField(upload_to='photos/speeches/guests', storage=S3Storage())
    crop_vert = models.IntegerField("Crop Vertical", choices=CROP_VERT_CHOICES, default=1)
    crop_horz = models.IntegerField("Crop Horizontal", choices=CROP_HORZ_CHOICES, default=1)

    class Meta:
        ordering = ('guest',)

    class IKOptions:
        spec_module = "photos.specs"
        cache_dir = ""
        image_field = "image"
        admin_thumbnail_spec = "thumbnail"
        crop_horz_field = "crop_horz"
        crop_vert_field = "crop_vert"

    def __unicode__(self):
        return unicode(self.guest)

