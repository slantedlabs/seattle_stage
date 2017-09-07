from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^$', views.admin_home, name='admin_home'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^password_change/$', auth_views.password_change,
        name='password_change'),
    url(r'^password_chage/done/$', views.password_change_done, 
        name='password_change_done'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^email_change/$', views.email_change, name='email_change'),
    ]

