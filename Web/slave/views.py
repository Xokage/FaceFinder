from __future__ import unicode_literals
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
from .tables import PersonDeleteTable
from .tables import DataTable
from .tables import JobTable
from .tables import JobRunningTable
from .tables import PersonGraphTable
from .forms  import *
from .utils import find_weight
from .utils import draw_graph
from .utils import imgreference_directory_path
from .utils import download_directory_path

scrapyd_url = "http://localhost:6800/"

def index(request):
    return render_to_response(
        'index.html',
        {},
        context_instance=RequestContext(request)
    )

def data(request):
    if request.path[-1] == '/':
        return redirect(request.path[:-1])
    data_list = TwitterItem.objects.all()
    if request.method == "POST":
        form = DataFilterForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['person_name']:
                data_list = data_list.filter(people=Person.objects.get(Q(name__contains=form.cleaned_data['person_name']) | Q(lastname__contains=form.cleaned_data['person_name'])))
            if form.cleaned_data['account_name']:
                data_list = data_list.filter(account=form.cleaned_data['account_name'])
            if form.cleaned_data['min_occurrence']:
                data_list = data_list.filter(occurrence__gte=form.cleaned_data['min_occurrence'])
    else:
        form = DataFilterForm()


    table = DataTable(data_list)
    RequestConfig(request, paginate={"per_page": 25}).configure(table)
    return render(request,
        'data.html',
        {'table':table, 'form':form},
    )

def jobs(request):
    if request.path[-1] == '/':
        return redirect(request.path[:-1])
    response = urllib2.urlopen(scrapyd_url + "listjobs.json?project=FaceFinder")    #call api of scrapyd
    job_list = response
    job_list_json = json.load(job_list)
    if job_list_json['running']:
        table_running = JobRunningTable(job_list_json['running'])
        RequestConfig(request, paginate={"per_page": 25}).configure(table_running)
    else:
        table_running = None
    if job_list_json['finished']:
        table_finished = JobTable(job_list_json['finished'])
        RequestConfig(request, paginate={"per_page": 25}).configure(table_finished)
    else:
        table_finished = None
    if job_list_json['pending']:
        table_pending = JobTable(job_list_json['pending'])
        RequestConfig(request, paginate={"per_page": 25}).configure(table_pending)
    else:
        table_pending = None
    return render(request,
        'jobs.html',
        {'table_running':table_running,
        'table_finished':table_finished,
        'table_pending':table_pending},
    )



def addjob(request):
    if request.path[-1] == '/':
        return redirect(request.path[:-1])    
    response = ""
    if request.method == "POST":
        form = AddJobForm(request.POST)
        if form.is_valid():
            person = Person.objects.get(Q(name__contains=form.cleaned_data['name']) | Q(lastname__contains=form.cleaned_data['lastname']))
            if person:
                person_id = person.pk
                data = urllib.urlencode({'project':'FaceFinder', 'spider':'twitterspider', 'start_url':form.cleaned_data['twitter_url'],'image_dir':imgreference_directory_path(person), 'downloads_dir':download_directory_path(person), 'person_id':person_id})
            else:
                data = urllib.urlencode({'project':'FaceFinder', 'spider':'twitterspider', 'start_url':form.cleaned_data['twitter_url'],'image_dir':form.cleaned_data['image_directory'], 'downloads_dir':form.cleaned_data['downloads_directory']})
            req = urllib2.Request(scrapyd_url + "schedule.json", data)    #call api of scrapyd        
            result = urllib2.urlopen(req)
            response = result.read()
    else:
        form = AddJobForm()

    return render(request,
            'addjob.html',
            {'form' : form, 'response' : response},
    )




def people(request):
    if request.path[-1] == '/':
        return redirect(request.path[:-1])   
    data_list = Person.objects.all()
    table = PersonDeleteTable(data_list)
    RequestConfig(request, paginate={"per_page": 25}).configure(table)
    return render(request,
            'people.html',
            {'table':table},
    )


def addperson(request):
    if request.path[-1] == '/':
        return redirect(request.path[:-1])    
    if request.method == "POST":
        form = AddPersonForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/people')
    else:
        form = AddPersonForm()

    return render(request,
            'addperson.html',
            {'form' : form},
    )




def graphs(request):
    if request.path[-1] == '/':
        return redirect(request.path[:-1])  
    data_list = Person.objects.all()
    table = PersonGraphTable(data_list)
    RequestConfig(request, paginate={"per_page": 25}).configure(table)
    return render(request,
            'graphs.html',
            {'table':table},
    )



def concretegraph(request, person_id):
    people = Person.objects.all()
    main_person = Person.objects.get(id=person_id)
    if request.method == "POST":
        form = GraphMinOccurrenceForm(request.POST)
        if form.is_valid():
            min_occurrence = form.cleaned_data['min_occurrence']
            graph = []
            weights = []
            for person in people:
                if person != main_person:
                    weight = find_weight(main_person, person,min_occurrence)
                    if weight > 0:
                        graph.append((main_person,person))
                        weights.append(weight)      
            draw_graph(graph,main_person.id,labels=weights)      
    else:
        form =  GraphMinOccurrenceForm()


    context = {'form' : form,'person_name':main_person.name, 'person_image_url':main_person.main_picture.url, 'person_id':main_person.id}
    return render(request,
            'concretegraph.html',
            context
    )


def concreteperson(request, person_id):

    person = Person.objects.get(id=person_id)
    images = Picture.objects.filter(person=person)
    image_list = []
    for img in images:
        image_list.append((img.file.url, img.id))
    context = {'person_name':person.name, 'person_image_url':person.main_picture.url, 'person_id':person_id, 'image_list':image_list}
    return render(request,
            'concreteperson.html',
            context
    )


def upload_picture(request, person_id):
    """
    Photo upload / dropzone handler
    :param request:
    :return:
    """
    form = PhotoUploadForm(request.POST, request.FILES or None)
    person = Person.objects.get(id=person_id)
    if form.is_valid() and person:
        pic = request.FILES['file']
        picture = Picture()
        picture.file = pic
        picture.person = person
        picture.save()
        return HttpResponse('Imaxe subida correctamente.')
    return HttpResponseBadRequest("Formulario incorrecto.")

def delete_picture(request, picture_id):
    """
    Photo deletion handler
    :param request:
    :return:
    """
    try:
        picture = Picture.objects.get(id=picture_id)   
    except ObjectDoesNotExist:
        return HttpResponseBadRequest('Id incorrecta. <meta http-equiv="refresh" content="1;url={0}"> '.format(request.META['HTTP_REFERER']))
    if picture:
        picture.delete()
        return HttpResponse('Imaxe borrada correctamente. <meta http-equiv="refresh" content="1;url={0}"> '.format(request.META['HTTP_REFERER']))
    
    return HttpResponseBadRequest('Id incorrecta. <meta http-equiv="refresh" content="1;url={0}"> '.format(request.META['HTTP_REFERER']))

def canceljob(request, job_id):
    """
    Job cancelation handler
    :param request:
    :return:
    """
    data = urllib.urlencode({'project':'FaceFinder', 'job':job_id})
    req = urllib2.Request(scrapyd_url + "cancel.json", data)    #call api of scrapyd        
    result = urllib2.urlopen(req)
    response = result.read()

    if '"status": "ok' in response:
        return HttpResponse('Traballo cancelado correctamente. <meta http-equiv="refresh" content="1;url={0}"> '.format(request.META['HTTP_REFERER']))
    
    return HttpResponseBadRequest('O traballo non se puido cancelar. <meta http-equiv="refresh" content="1;url={0}"> '.format(request.META['HTTP_REFERER']))


def delete_person(request, person_id):
    """
    Person deletion handler
    :param request:
    :return:
    """
    try:
        person = Person.objects.get(id=person_id)   
    except ObjectDoesNotExist:
        return HttpResponseBadRequest('Id incorrecta. <meta http-equiv="refresh" content="1;url={0}"> '.format(request.META['HTTP_REFERER']))
    if person:
        person.delete()
        return HttpResponse('Persoa borrada correctamente. <meta http-equiv="refresh" content="1;url={0}"> '.format(request.META['HTTP_REFERER']))
    
    return HttpResponseBadRequest('Id incorrecta. <meta http-equiv="refresh" content="1;url={0}"> '.format(request.META['HTTP_REFERER']))


