import datetime

from django.http import *
from django.template import Context, RequestContext, loader 
from django.shortcuts import render_to_response
from django.utils.encoding import force_unicode
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

from youtube_timer.models import YouTubeEntry
from youtube_timer.utils import publish_entries, is_published

def logout(request):
    """
    Simple wrapper around django's auth logout with own template.
    """
    from django.contrib.auth import logout
    logout(request)
    return render_to_response('youtube_timer/login.html', {'logged_out': True})

@login_required
def overview(request):
    entries = YouTubeEntry.objects.all().order_by('-id')[:20]
    return render_to_response('youtube_timer/main.html', {'entry_list': entries})

@login_required
def delete(request):
    entry = YouTubeEntry.objects.get(id=request.GET.get('video_id'))
    entry.delete()
    return HttpResponse('%s deleted.' % request.GET.get('video_id'))
    

@login_required
def add_timer(request):
    data = request.POST
    entry = YouTubeEntry()
    entry.youtube_id = data.get('youtube_id')
    entry.published = False
    entry.processed = False
    day,month,year = data.get('date').split('.')
    hour,minute = data.get('time').split(':')
    entry.pub_date = datetime.date(int(year), int(month), int(day))
    entry.pub_time = datetime.time(int(hour), int(minute))
    entry.save()
    return render_to_response('youtube_timer/entry_include.html', {'entry': entry})

@login_required
def force_publish(request):
    video_id = request.GET.get('video_id')
    entry = YouTubeEntry.objects.get(id=video_id)
    published = publish_entries([entry])
    entry.processed = True
    entry.save()
    return render_to_response('youtube_timer/publish_status.html', {'entry': entry})

@login_required
def force_unpublish(request):
    video_id = request.GET.get('video_id')
    entry = YouTubeEntry.objects.get(id=video_id)
    unpublished = publish_entries([entry], True)
    entry.processed = True
    entry.save()
    return render_to_response('youtube_timer/publish_status.html', {'entry': entry})