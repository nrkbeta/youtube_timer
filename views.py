"""
"THE BEER-WARE LICENSE" (Revision 42):
---------------------------------------
<henriklied@gmail.com> wrote this file. As long as you retain this notice you
can do whatever you want with this stuff. If we meet some day, and you think
this stuff is worth it, you can buy me a beer in return. Henrik Lied

"""
import datetime

from django.http import *
from django.template import Context, RequestContext, loader 
from django.shortcuts import render_to_response
from django.utils.encoding import force_unicode
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

from youtube_timer.models import YouTubeEntry
from youtube_timer.utils import publish_entries

def logout(request):
    """
    Simple wrapper around django's auth logout with own template.
    """
    from django.contrib.auth import logout
    logout(request)
    return render_to_response('youtube_timer/login.html', {'logged_out': True})

@login_required
def overview(request):
    """
    Shows the last 20 YouTubeEntry instances on the frontpage.
    """
    entries = YouTubeEntry.objects.all().order_by('-id')[:20]
    return render_to_response('youtube_timer/main.html', {'entry_list': entries})

@login_required
def delete(request):
    """
    AJAX view to delete a YouTubeEntry instance.
    Takes only request as argument, but request.GET needs to have a 'video_id' param.
    """
    entry = YouTubeEntry.objects.get(id=request.GET.get('video_id'))
    entry.delete()
    return HttpResponse('%s deleted.' % request.GET.get('video_id'))
    

@login_required
def add_timer(request):
    """
    AJAX view to add a timer. Should really map this to a django.form,
    but first iterations always suck. :-)
    """
    data = request.POST
    entry = YouTubeEntry()
    entry.name = data.get('name', None)
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
    """
    Force publishing of a video.
    """
    video_id = request.GET.get('video_id')
    entry = YouTubeEntry.objects.get(id=video_id)
    published = publish_entries([entry])
    entry.processed = True
    entry.save()
    return render_to_response('youtube_timer/publish_status.html', {'entry': entry})

@login_required
def force_unpublish(request):
    """
    Remove "public" status from a video.
    """
    video_id = request.GET.get('video_id')
    entry = YouTubeEntry.objects.get(id=video_id)
    unpublished = publish_entries([entry], reverse=True)
    entry.processed = True
    entry.save()
    return render_to_response('youtube_timer/publish_status.html', {'entry': entry})