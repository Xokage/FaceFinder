from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.shortcuts import redirect

from .models import TwitterItem

def index(request):
    return render_to_response(
        'index.html',
        {},
        context_instance=RequestContext(request)
    )

def data(request):
    if request.path[-1] == '/':
        return redirect(request.path[:-1])
    data_list = TwitterItem.objects.all().order_by('-occurrence')
    paginator = Paginator(data_list, 5) #show 25 data per page

    page = request.GET.get('page')
    try:
        some_data_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        some_data_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        some_data_list = paginator.page(paginator.num_pages)

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
