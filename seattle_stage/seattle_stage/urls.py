"""seattle_stage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.views.static import serve as dj_static_serve

import theater.views

urlpatterns = [
    #url(r'^admin/', admin.site.urls),
    url(r'^$', theater.views.index, name="root_index"),
    #url(r'^admin/', include('registration.urls')),
    url(r'^stage/', include('theater.urls')),
    url(r'^registration/', include('registration.urls')),
    url(r'^accounts/', include('registration.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if not settings.DEBUG:
  static_url = '/'.join([p for p in settings.STATIC_URL.split('/') if not p == ''])
  static_url = ''.join([r'^', static_url, r'/(?P<path>.*)$'])
  urlpatterns += [
      url(static_url,
        dj_static_serve,
        {'document_root': settings.STATIC_ROOT})
      ]
