from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render_to_response
from django.template import RequestContext

from .models import Person

def index(request):
    return render_to_response(
        'index.html',
        {},
        context_instance=RequestContext(request)
    )

def image(request, image_id):
    return HttpResponse("Estas buscando a foto %s." % image_id)

def person(request, person_id):
    return HttpResponse("Estas buscando a persoa %s." % person_id)

def people(request):
    some_people_list = Person.objects.order_by('name')[:5]
    context = {
        'some_people_list': some_people_list,
    }
    return render_to_response(
        'index.html',
        context,
        context_instance=RequestContext(request)
    )

def jobs(request):
    return render_to_response(
        'index.html',
        {},
        context_instance=RequestContext(request)
    )

