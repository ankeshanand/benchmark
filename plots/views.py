# Create your views here.

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils import simplejson
from django.http import HttpResponse, Http404
from .models import BenchmarkLogs, MachineInfo

def rawdata(request, type):
    #if type == "AvgVGRvsProcessor":
    return

def draw(request, type):
    type_dict = {'type': type}
    return render_to_response("chart.html", type_dict, context_instance=RequestContext(request))
