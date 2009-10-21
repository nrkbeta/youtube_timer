import datetime

from django.http import *
from django.template import Context, RequestContext, loader 
from django.shortcuts import render_to_response
from django.utils.encoding import force_unicode
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse

from youtube_timer.models import YouTubeEntry
from youtube_timer.utils import publish_entries, is_published

def overview(request):
    entries = YouTubeEntry.objects.all().order_by('-id')[:20]
    return render_to_response('youtube_timer/main.html', {'entry_list': entries})

def add_timer(request):
    data = request.POST
    entry = YouTubeEntry()
    entry.youtube_id = data.get('youtube_id')
    entry.published = is_published(data.get('youtube_id'))
    day,month,year = data.get('date').split('.')
    hour,minute = data.get('time').split(':')
    entry.pub_date = datetime.date(int(year), int(month), int(day))
    entry.pub_time = datetime.time(int(hour), int(minute))
    entry.save()
    return render_to_response('youtube_timer/entry_include.html', {'entry': entry})

def force_publish(request):
    video_id = request.GET.get('video_id')
    entry = YouTubeEntry.objects.get(id=video_id)
    published = publish_entries([entry])
    entry.processed = True
    entry.save()
    return render_to_response('youtube_timer/publish_status.html', {'entry': entry})

def force_unpublish(request):
    video_id = request.GET.get('video_id')
    entry = YouTubeEntry.objects.get(id=video_id)
    unpublished = publish_entries([entry], True)
    entry.processed = True
    entry.save()
    return render_to_response('youtube_timer/publish_status.html', {'entry': entry})