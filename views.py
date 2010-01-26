from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from speeches.models import Speech, Footnote
from speeches.forms import FootnoteForm

from django.views.decorators.cache import never_cache

@never_cache
def speech_detail(request, object_id, slug=None):
    speech = get_object_or_404(Speech, pk__exact=object_id)
    if not request.user.is_staff and (speech.status != Speech.LIVE_STATUS):
        raise Http404
    if speech.slug != slug:
        return HttpResponseRedirect(speech.get_absolute_url())
        
    footnotes = speech.footnotes.live()
    guest_list = speech.users().filter(profile__isnull=False)
    return render_to_response('speeches/speech_detail.html',
                              {'speech': speech, 'footnotes': footnotes, 'guest_list': guest_list},
                              context_instance=RequestContext(request))


@login_required
def annotate_speech(request, object_id):
    speech = get_object_or_404(Speech, pk__exact=object_id)
    footnotes = speech.footnotes.all()
    guests = speech.users().filter(profile__isnull=False)
    return render_to_response('speeches/annotate_speech.html',
                              {'speech': speech, 'footnotes': footnotes, 'guests': guests},
                              context_instance=RequestContext(request))


@login_required
def add_footnote(request, object_id):
    if request.GET.has_key('popup'):
        template = "speeches/add_footnote_popup.html"
    else:
        template = "speeches/add_footnote.html"
    speech = get_object_or_404(Speech, pk__exact=object_id)
    index = request.GET.get('index', '0')
    footnotes = speech.footnotes.filter(index=index)
    if request.method == 'POST':
        form = FootnoteForm(data=request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            if not f.speech:
                f.speech = speech
            if not f.index:
                f.index = index
            
            f.author = request.user
            f.save()
            return HttpResponseRedirect(reverse('speeches_speech_annotate', args=(speech.pk,), kwargs={}))
        
    else:
        form = FootnoteForm(initial={
            'index': index,
            'author': request.user.pk,
            'speech': speech.pk}
        )
    
    return render_to_response(template,
                              {'speech': speech, 'form': form, 'footnotes': footnotes},
                              context_instance=RequestContext(request))
