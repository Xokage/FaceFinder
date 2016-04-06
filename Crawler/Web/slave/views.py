from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.shortcuts import redirect

from django_tables2   import RequestConfig
import urllib2
import urllib
import json

from .models import TwitterItem
from .tables import DataTable
from .tables import JobTable
from .forms import AddJobForm


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
    table = DataTable(data_list)
    RequestConfig(request, paginate={"per_page": 25}).configure(table)
    return render(request,
        'data.html',
        {'table':table},
    )

def jobs(request):
    if request.path[-1] == '/':
        return redirect(request.path[:-1])
    if(request.GET.get('mybtn')):
        mypythoncode.mypythonfunction( int(request.GET.get('mytextbox')) )
    response = urllib2.urlopen(scrapyd_url + "listjobs.json?project=FaceFinder")    #call api of scrapyd
    job_list = response
    job_list_json = json.load(job_list)
    table_running = JobTable(job_list_json['running'])
    table_finished = JobTable(job_list_json['finished'])
    table_pending = JobTable(job_list_json['pending'])
    RequestConfig(request, paginate={"per_page": 25}).configure(table_running)
    RequestConfig(request, paginate={"per_page": 25}).configure(table_finished)
    RequestConfig(request, paginate={"per_page": 25}).configure(table_pending)
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
            data = urllib.urlencode({'project':'FaceFinder', 'spider':'twitterspider', 'start_url':form.cleaned_data['twitter_url'], 'image_dir':form.cleaned_data['image_directory'], 'downloads_dir':form.cleaned_data['downloads_directory']})
            req = urllib2.Request(scrapyd_url + "schedule.json", data)    #call api of scrapyd        
            result = urllib2.urlopen(req)
            response = result.read()
    else:
        form = AddJobForm()

    return render(request,
            'addjob.html',
            {'form' : form, 'response' : response},
    )
