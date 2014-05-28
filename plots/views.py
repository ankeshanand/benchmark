# Create your views here.
import json
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils import simplejson
from django.http import HttpResponse, Http404
from .models import BenchmarkLogs, MachineInfo
import data


def rawdata(request, plotname):
    """
    Based on the ajax request from the template, it calls data.py to fetch the appropriate data.
    It returns a JSON dump of the dictionary that is returned from data.py
    """
    if request.is_ajax():
        try:
            data_dict = {}
            data_dict = getattr(data, plotname).__call__()
            print data_dict
            return HttpResponse(simplejson.dumps(data_dict), content_type="application/json")
        except AttributeError:
            raise 404
    raise 404


def draw(request, plotname):
    """
    The draw view is responsible for drawing the chart. It renders a template chart.html which sends ajax request for the JSON data.
    It also provides the template the name of the plot to draw via the <name_dict> dictionary.
    """
    name_dict = {'plotname': plotname}
    return render_to_response("chart.html", name_dict, context_instance=RequestContext(request))
