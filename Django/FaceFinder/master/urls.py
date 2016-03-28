from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # ex: /image/5/
    url(r'^image/(?P<image_id>[0-9]+)/$', views.image, name='image'),
    # ex: /person/3/
    url(r'^person/(?P<person_id>[0-9]+)/$', views.person, name='person'),
    # ex: /people/
    url(r'^people/$', views.people, name='people'),
    # ex: /jobs/
    url(r'^jobs/$', views.jobs, name='jobs'),
]
