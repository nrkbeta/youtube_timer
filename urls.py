from django.conf.urls.defaults import *

urlpatterns = patterns('youtube_timer.views',

    url(r'^$',
        view='overview',
        name='youtube_timer_overview'),
    
    url(r'^login/$',
        view='login',
        name="youtube_timer_login"),
    
    url(r'^add_timer/$',
        view='add_timer',
        name='youtube_timer_add'),
    
    url(r'^force_publish/$',
        view='force_publish',
        name='youtube_timer_force_publish'),

    url(r'^force_unpublish/$',
        view='force_unpublish',
        name='youtube_timer_force_unpublish'),
    

)

