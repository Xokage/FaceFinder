# -*- coding: utf-8 -*-
#################################################################################
#   Facefinder: Crawl pictures based on known faces and extract information.    #
#   Copyright (C) 2016 Xoán Antelo Castro                                       #
#                                                                               #
#   This program is free software: you can redistribute it and/or modify        #
#   it under the terms of the GNU General Public License as published by        #
#   the Free Software Foundation, either version 3 of the License, or           #
#   (at your option) any later version.                                         #
#                                                                               #
#   This program is distributed in the hope that it will be useful,             #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of              #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
#   GNU General Public License for more details.                                #
#                                                                               #
#   You should have received a copy of the GNU General Public License           #
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.       #
#################################################################################
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
    # ex: /canceljob
    url(r'^canceljob/(?P<job_id>[0-9a-f]+)$', views.canceljob, name='canceljob'),
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
    # ex: /delete_picture/1
    url(r'^delete_picture/(?P<picture_id>[0-9]+)$', views.delete_picture, name='delete_picture'),
    # ex: /delete_picture/1
    url(r'^delete_person/(?P<person_id>[0-9]+)$', views.delete_person, name='delete_person'),
]
