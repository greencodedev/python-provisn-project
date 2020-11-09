from django.conf.urls import url
from django.urls import path, include
from django.views.generic import TemplateView

from . import views
#from django.conf.urls import url
#from . import receivers

### Well this explains itself i think
### path(uri, view method, name (e.g. grabbing urls));

urlpatterns = [

    path('', views.frontpage, name='frontpage'),
    path('terms/', views.frontpage_terms, name='frontpage_terms'),
    path('privacy/', views.frontpage_privacy, name='frontpage_privacy'),
    url(r'^robots\.txt$', TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),
]