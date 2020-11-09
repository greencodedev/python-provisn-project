"""plutus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.views.generic import RedirectView
#from machina import urls as machina_urls
from django.conf.urls.static import static


admin.site.site_header = 'Provisn Administration'
admin.site.site_title = 'Provisn Administration'

urlpatterns = [
    path('grappelli/', include('grappelli.urls')), # grappelli URLS
    path('cpanel/', admin.site.urls),
    path('cpanel/doc/', include('django.contrib.admindocs.urls')),
    path('member/', include('userdashboard.urls')),
    path('', include('frontpage.urls')),
    path('', include('django.contrib.auth.urls')),
    url(r'^accounts/login/$', RedirectView.as_view(pattern_name='login', permanent=False)),
    path('cryptapi/', include('cryptapi.urls')),
    url(r'^accounts/passwordreset/', include('password_reset.urls')),
    #path('forum/', include(machina_urls)),
    path('calendar/', include('Calendar.urls')),

#    url(r'^member/', include('django_private_chat.urls')),

    # In case unwanted redirections occur to /user/* uncomment and update the following line
    #path('user/*/', RedirectView.as_view(pattern_name='user_area')),
]

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .settings import DEBUG
if DEBUG == True:
    urlpatterns += staticfiles_urlpatterns()

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import plutus.settings as settings
if settings.DEBUG == True:
    urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
