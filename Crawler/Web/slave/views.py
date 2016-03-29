from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render_to_response
from django.template import RequestContext

from .models import TwitterItem

def index(request):
    return render_to_response(
        'index.html',
        {},
        context_instance=RequestContext(request)
    )

def data(request):
    some_data_list = TwitterItem.objects.order_by('occurrence')[:5]
    context = {
        'some_data_list': some_data_list,
    }
    return render_to_response(
        'index.html',
        context,
        context_instance=RequestContext(request)
    )

def currentjob(request):
    return render_to_response(
        'index.html',
        {},
        context_instance=RequestContext(request)
    )
