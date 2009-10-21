from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
    help = "Run this as a cronjob to publish YouTube-videos at certain times."

    def handle_noargs(self, **options):
        from youtube_timer.utils import publish_entries
        from youtube_timer.models import YouTubeEntry
        entries = publish_entries(YouTubeEntry.objects.for_publishing())
        if not entries:
            return 'Done, all published'
        return 'Could not publish these videos (look them up in the db): %s' % (', '.join(entries))