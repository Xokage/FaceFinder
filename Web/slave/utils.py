
import os
from django.utils.safestring import mark_safe
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.shortcuts import redirect
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

from django_tables2   import RequestConfig
from django.conf import settings
import urllib2
import urllib
import json
import networkx as nx
import os
import uuid
import errno

from brpy import init_brpy

import matplotlib.pyplot as plt

from django.utils.safestring import mark_safe
from .models import TwitterItem
from .models import Person
from .models import Picture
from .tables import PersonTable
from .tables import DataTable
from .tables import JobTable
from .tables import PersonGraphTable
from .forms  import *

import networkx as nx
import matplotlib.pyplot as plt

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




def find_weight(main_person, rel_person):
    mcomparision_list = []
    mtmpl_list = []
    rcomparision_list = []
    rtmpl_list = []
    pass_score = 0.5
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
    for root, dirs, files in os.walk(downloads_dir, topdown=False):
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
               node_size=1600, node_color='blue', node_alpha=0.3,
               node_text_size=12,
               edge_color='blue', edge_alpha=0.3, edge_tickness=1,
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

    # draw graph
    nx.draw_networkx_nodes(G,graph_pos,node_size=node_size, 
                           alpha=node_alpha, node_color=node_color)
    nx.draw_networkx_edges(G,graph_pos,width=edge_tickness,
                           alpha=edge_alpha,edge_color=edge_color)
    nx.draw_networkx_labels(G, graph_pos,font_size=node_text_size,
                            font_family=text_font)

    if labels is None:
        labels = range(len(graph))

    edge_labels = dict(zip(graph, labels))
    nx.draw_networkx_edge_labels(G, graph_pos, edge_labels=edge_labels, 
                                 label_pos=edge_text_pos)

    # save graph
    plt.savefig(os.path.join(settings.MEDIA_ROOT,"graph_{0}.png".format(person_id)))
    plt.clf()
