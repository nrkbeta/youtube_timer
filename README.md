# YouTube Tea Timer
A simple way to setup publishing of videos in the future.

Used by The Norwegian Broadcasting Corporation to postpone airing of YouTube-videos until they've aired on the regular TV Channels.

## Requirements
- youtube_timer (…of course)
- django > 1.0
- [gdata](http://code.google.com/p/gdata-python-client/)
- [YouTube Developer Key](code.google.com/apis/youtube/dashboard/gwt/index.html)

## Setup

- add `youtube_timer` to your INSTALLED_APPS
- you need to set the following in your settings-file:
    - YOUTUBE_USERNAME : your YouTube-username
    - YOUTUBE_EMAIL : your Google Account email
    - YOUTUBE_PASSWORD : your Google Account password
    - YOUTUBE\_APP_ID : doesn't really matter that much, just use 'youtube-tea-timer'
    - YOUTUBE\_APP_LABEL : Use the same name as you used when signing up for the [developer key](code.google.com/apis/youtube/dashboard/gwt/index.html)
    - YOUTUBE\_DEVELOPER_KEY : Your developer key

- add `(r'^your_endpoint/', include('youtube_timer.urls'))` to your urls.py
- run `syncdb`

## Usage
Simple: Once setup, go to the URL where you've included `youtube_timer`, and login. From here it's simple to create a new timer.

## Management command
There's a management command that's useful in a cron setting. It publishes all jobs that are over their time limit.
We run a cron job every minute like this:
    
    * * * * * /path/to/app/youtube_timer/cron.sh

…where `cron.sh` is a simple wrapper like this (we use this because of our weird env, you might get away with running it directly):

    #!/usr/local/bin/bash
    DJANGO_SETTINGS_MODULE='project.settings'
    export DJANGO_SETTINGS_MODULE

    PYTHONPATH=/my/special/path/to/libs
    export PYTHONPATH

    /usr/local/bin/python /my/special/path/to/libs/project/manage.py run_youtube_timer
    