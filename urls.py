"""
"THE BEER-WARE LICENSE" (Revision 42):
---------------------------------------
<henriklied@gmail.com> wrote this file on behalf of NRK (NORSK RIKSKRINGKASTING AS). 
As long as you retain this notice you can do whatever you want with this stuff. 
If we meet some day, and you think this stuff is worth it, you can buy me a beer in return. 

Henrik Lied

"""
from django.conf.urls.defaults import *

urlpatterns = patterns('youtube_timer.views',

    url(r'^$',
        view='overview',
        name='youtube_timer_overview'),
    
    url(r'^logout/$',
        view='logout',
        name='youtube_timer_logout'),
        
    url(r'^add_timer/$',
        view='add_timer',
        name='youtube_timer_add'),
    
    url(r'^delete/$',
        view='delete',
        name='youtube_timer_delete'),
    
    url(r'^force_publish/$',
        view='force_publish',
        name='youtube_timer_force_publish'),

    url(r'^force_unpublish/$',
        view='force_unpublish',
        name='youtube_timer_force_unpublish'),
    

)

