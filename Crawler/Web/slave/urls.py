from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # ex: /data
    url(r'^data/$', views.data, name='data'),
    # ex: /currentjob
    url(r'^currentjob/$', views.currentjob, name='currentjob'),
]
