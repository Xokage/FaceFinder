from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # ex: /data
    url(r'^data/?$', views.data, name='data'),
    # ex: /jobs
    url(r'^jobs/?$', views.jobs, name='jobs'),
    # ex: /addjob    
    url(r'^addjob/?$', views.addjob, name='addjob'),
]
