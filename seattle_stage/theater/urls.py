from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

app_name = 'theater'
urlpatterns = [
    url(r'^$', views.event_index, name='index'),

    # admin dashboard
    url(r'^admin/$', views.admin_dashboard, name='admin_dashboard'),

    # index pages
    url(r'^suggestions/$', views.suggestions, name='suggestions'),
    url(r'^scene/$', views.scene, name='scene'),

    # calender/day views
    url(r'^events/$',
      views.event_month, name='events_month'),
    url(r'^ajax/events/$',
      views.ajax_update_event_month, name='ajax_events_month'),
    url(r'^events/week/$',
      views.event_week, name='events_week'),
    url(r'^events/day/$',
      views.event_day, name='events_day'),
    url(r'^events/(?P<event_pk>[0-9]+)/$',
      views.event_detail, name='event_detail'),
    url(r'^events/new/$',
      views.event_new, name='event_new'),
    url(r'^events/(?P<event_pk>[0-9]+)/edit/$',
      views.event_edit, name='event_edit'),
    url(r'^events/(?P<event_pk>[0-9]+)/delete/$',
      views.event_delete, name='event_delete'),

    # venues
    url(r'^venues/$',
      views.venue_index, name='venue_index'),
    url(r'^venues/(?P<venue_pk>[0-9]+)/$',
      views.venue_detail, name='venue_detail'),
    url(r'^venues/new/$',
      views.venue_new, name='venue_new'),
    url(r'^venues/(?P<venue_pk>[0-9]+)/edit/$',
      views.venue_edit, name='venue_edit'),
    url(r'^venues/(?P<venue_pk>[0-9]+)/delete/$',
      views.venue_delete, name='venue_delete'),

    # companies
    url(r'^companies/$',
      views.company_index, name='company_index'),
    url(r'^companies/(?P<company_pk>[0-9]+)/$',
      views.company_detail, name='company_detail'),
    url(r'^companies/new/$',
      views.company_new, name='company_new'),
    url(r'^companies/(?P<company_pk>[0-9]+)/edit/$',
      views.company_edit, name='company_edit'),
    url(r'^companies/(?P<company_pk>[0-9]+)/delete/$',
      views.company_delete, name='company_delete'),

    # admin stuff
    url(r'^admin/login/$', auth_views.login, name='admin_login'),
    ]
