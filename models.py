from django.db import models
import datetime


class YouTubeManager(models.Manager):
    """
    Three methods:
        - for_publishing
            returns entries which are over their time limit for being published,
            and that hasn't already been processed.
        - published
            returns all published YouTubeEntry's
        - postponed
            returns all 'processed' YouTubeEntry's
    """
        
    def for_publishing(self):
        now = datetime.datetime.now()
        now_date = datetime.date(now.year, now.month, now.day)
        now_time = datetime.time(now.hour, now.minute)
        return self.get_query_set().filter(pub_date=now_date, pub_time__lt=now_time, published=False, processed=False)
    
    def published(self):
        return self.get_query_set().filter(published=True)
    
    def postponed(self):
        return self.get_query_set().filter(processed=True)


class YouTubeEntry(models.Model):
    """
    Holds the data regarding a YouTube video.
    The 'processed' boolean can be used for manually overriding a publish.
    """
    youtube_id = models.CharField(blank=True, max_length=255)
    pub_date = models.DateField()
    pub_time = models.TimeField()
    published = models.BooleanField(default=False)
    processed = models.BooleanField(default=False)
    
    objects = YouTubeManager()
    
    def __unicode__(self):
        return self.youtube_id    
    
    def save(self):
        if not self.id:
            self.processed = False
        super(YouTubeEntry, self).save()