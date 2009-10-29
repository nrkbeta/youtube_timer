"""
"THE BEER-WARE LICENSE" (Revision 42):
---------------------------------------
<henriklied@gmail.com> wrote this file on behalf of NRK (NORSK RIKSKRINGKASTING AS). 
As long as you retain this notice you can do whatever you want with this stuff. 
If we meet some day, and you think this stuff is worth it, you can buy me a beer in return. 

Henrik Lied

"""
from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
    help = "Run this as a cronjob to publish YouTube-videos at certain times."

    def handle_noargs(self, **options):
        from youtube_timer.utils import publish_entries
        
        entries = publish_entries()
        if not entries:
            return
        return 'Could not publish these videos (look them up in the db): %s' % (', '.join(entries))