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
    # ex: /people    
    url(r'^people/?$', views.people, name='people'),
    # ex: /graphs    
    url(r'^graphs/?$', views.graphs, name='graphs'),
    # ex: /graphs/1    
    url(r'^graphs/(?P<person_id>[0-9]+)$', views.concretegraph, name='concretegraph'),
    # ex: /addperson    
    url(r'^addperson/?$', views.addperson, name='addperson'),
    # ex: /person/1    
    url(r'^person/(?P<person_id>[0-9]+)$', views.concreteperson, name='concreteperson'),
    # ex: /upload_picture/1    
    url(r'^upload_picture/(?P<person_id>[0-9]+)$', views.upload_picture, name='upload_picture'),

]
