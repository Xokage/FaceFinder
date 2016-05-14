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

import os, json, uuid, errno
import networkx as nx
import matplotlib.pyplot as plt


from brpy import init_brpy

from django.conf import settings
from django.core.paginator import EmptyPage
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.template import loader
from django.utils.safestring import mark_safe

from .models import Picture
from .tables import PersonTable
from .forms  import *

def dir_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def download_directory_path(instance):
        return mark_safe(os.path.abspath(os.path.join(settings.MEDIA_ROOT,'downloads/{0}'.format(instance.name + " " + instance.lastname))))

def imgreference_directory_path(instance):
        return mark_safe(os.path.abspath(os.path.join(settings.MEDIA_ROOT,'pictures/{0}/reference_pictures/'.format(instance.name + " " + instance.lastname))))

def br_add_images(directories,template_list,image_list,br):
    while(directories): #Repeat until no more subdirectories found
        for root, dirs, files in os.walk(directories[0], topdown=False):
            for name in files:
                image = open(os.path.join(root, name)).read()
                tmpl = br.br_load_img(image, len(image))
                template_list.append(tmpl)
                query = br.br_enroll_template(tmpl) #append to class list of templates
                nquery = br.br_num_templates(tmpl)
                image_list.append((query,nquery))
        directories.pop(0)
        directories.extend(dirs)
        dirs = []




def find_weight(main_person, rel_person, min_score):
    mcomparision_list = []
    mtmpl_list = []
    rcomparision_list = []
    rtmpl_list = []
    pass_score = min_score
    weight = 0
    mimage_dir = imgreference_directory_path(main_person)
    rimage_dir = imgreference_directory_path(rel_person)
    downloads_dir = download_directory_path(main_person)

    br = init_brpy(br_loc='/usr/local/lib') #Default openbr lib location.
    br.br_initialize_default()
    br.br_set_property('algorithm','FaceRecognition') #Algorithm to compare faces
    br.br_set_property('enrollAll','false')

    #Be sure directories exists
    dir_exists(mimage_dir)
    dir_exists(rimage_dir)
    dir_exists(downloads_dir)

    #Add images to br
    directories = [mimage_dir]
    br_add_images(directories,mtmpl_list,mcomparision_list,br)

    #Add images to br
    directories = [rimage_dir]
    br_add_images(directories,rtmpl_list,rcomparision_list,br)

    #Compare images
    for root, _, files in os.walk(downloads_dir, topdown=False):
        for name in files:
            image = open(os.path.join(root, name)).read()
            tmpl = br.br_load_img(image, len(image))
            targets = br.br_enroll_template(tmpl)
            ntargets = br.br_num_templates(targets)
            # compare and collect scores

            # compare with all images
            scores = []
            for query, nquery in mcomparision_list:
                scoresmat = br.br_compare_template_lists(targets, query)
                for r in range(ntargets):
                    for c in range(nquery):
                        scores.append(br.br_get_matrix_output_at(scoresmat, r, c))

            if scores :
                scores.sort()
                maxscore = float("-inf")

                for score in scores:
                    if(score > maxscore):
                        maxscore = score
                #compare with pass score
                if maxscore >= pass_score:
                    #if match, check if other person is also in photo
                    scores = []

                    for query, nquery in rcomparision_list:
                        scoresmat = br.br_compare_template_lists(targets, query)
                        for r in range(ntargets):
                            for c in range(nquery):
                                scores.append(br.br_get_matrix_output_at(scoresmat, r, c))
                    if scores:
                        scores.sort()
                        maxscore = float("-inf")
                        for score in scores:
                            if(score > maxscore):
                                maxscore = score
                        #compare with pass score
                        if maxscore >= pass_score:
                            #Both are in photo, so we add weight
                            weight = weight + 1

    # clean up - no memory leaks
    br.br_free_template(tmpl)
    br.br_free_template_list(targets)

    return weight



def draw_graph(graph, person_id, labels=None, graph_layout='spring',
               node_size=600, node_color='blue', node_alpha=0.3,
               node_text_size=12,
               edge_color='red', edge_alpha=0.3, edge_thickness=1,
               edge_text_pos=0.3,
               text_font='sans-serif'):

    # create networkx graph
    G=nx.Graph()

    # add edges
    for edge in graph:
        G.add_edge(edge[0], edge[1])

    # these are different layouts for the network you may try
    # shell seems to work best
    if graph_layout == 'spring':
        graph_pos=nx.spring_layout(G)
    elif graph_layout == 'spectral':
        graph_pos=nx.spectral_layout(G)
    elif graph_layout == 'random':
        graph_pos=nx.random_layout(G)
    else:
        graph_pos=nx.shell_layout(G)

    edgewidth = edge_thickness
    if labels:
        edgewidth = []
        minlabel = min(labels)
        for label in labels:
            edgewidth.append(label - minlabel + 1)

    # draw graph
    NoN = nx.number_of_nodes(G)
    plt.figure(1,figsize=(10 + 1.2*NoN,10 + 1.2*NoN))
    nx.draw_networkx_nodes(G,graph_pos,node_size=node_size,
                           alpha=node_alpha, node_color=node_color, label='Persoas')
    nx.draw_networkx_edges(G,graph_pos,width=edgewidth,
                           alpha=edge_alpha,edge_color=edge_color, label='Num. fotos en comun')
    nx.draw_networkx_labels(G, graph_pos,font_size=node_text_size,
                            font_family=text_font)

    if labels is None:
        labels = range(len(graph))

    edge_labels = dict(zip(graph, labels))
    nx.draw_networkx_edge_labels(G, graph_pos, edge_labels=edge_labels,
                                 label_pos=edge_text_pos)

    #legend
    plt.legend(scatterpoints=1)
    filepath = os.path.join(settings.MEDIA_ROOT,"graph_{0}.png".format(person_id))
    #remove old graph
    try:
        os.remove(filepath)
    except OSError:
        pass

    # save graph
    plt.savefig(filepath)
    plt.clf()
