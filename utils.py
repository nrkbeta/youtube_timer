import datetime
import gdata
from gdata.youtube.service import YouTubeService


from youtube_timer.models import YouTubeEntry
from django.conf import settings

USERNAME = getattr(settings, 'YOUTUBE_USERNAME', 'your-username-here (not email)')

def youtube_login():
    """
    Authenticate against YouTube. Returns a YouTubeService object
    """
    yt_service = YouTubeService()
    yt_service.email = getattr(settings, 'YOUTUBE_EMAIL', 'your-email-here@gmail.com')
    yt_service.password = getattr(settings, 'YOUTUBE_PASSWORD', 'your password')
    yt_service.source = getattr(settings, 'YOUTUBE_APP_LABEL', 'YouTube Tea Timer')
    yt_service.client_id = getattr(settings, 'YOUTUBE_APP_ID', 'youtube-tea-timer')
    yt_service.developer_key = getattr(settings, 'YOUTUBE_DEVELOPER_KEY', 'devkey')
    yt_service.ProgrammaticLogin()
    return yt_service


YOUTUBE = youtube_login()

def monkeypatch_videoentry(entry):
    """
    The YouTubeVideoEntry class doesn't include the rel=['edit'] link in its
    instance.links, so we have to monkeypatch it in here.
    """
    video_id = entry.id.text.split('/')[-1]
    edit_link = gdata.atom.Link()
    edit_link.rel = 'edit'
    edit_link.href = 'http://gdata.youtube.com/feeds/api/users/%s/uploads/%s' % (USERNAME, video_id)
    entry.link.append(edit_link)
    return entry
    

def publish_entries(entries=None, reverse=False):
    errors = []
    if not entries:
        entries = YouTubeEntry.objects.for_publishing()
    for entry in entries:
        try:
            item = YOUTUBE.GetYouTubeVideoEntry(video_id=entry.youtube_id)
            item = monkeypatch_videoentry(item)
            if reverse:
                item.media.private = gdata.media.Private()
            else:
                item.media.private = None
            YOUTUBE.UpdateVideoEntry(item)
            
            if reverse:
                entry.published = False
            else:
                entry.published = True
            entry.save()
        except:
            errors.append(entry.id)
        
    return errors