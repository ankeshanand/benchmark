__author__ = 'ankesh'
from .models import BenchmarkLogs, MachineInfo
from django.db.models import Sum, Avg


def avgVGRvsProcessor():
    print "In the def, bitch"
    data_dict = {'chart_title': "Average VGR Rating vs Processor Family",
                 'chart_type': "bar",
                 'xAxis_title_text': "Processor Family",
                 'yAxis_title_text': "Average VGR Rating",
                 'categories': [],
                 'series': []}

    distinct_categories_dict = MachineInfo.objects.values('vendor_id').distinct()
    for category in distinct_categories_dict:
        data_dict['categories'].append(category['vendor_id'])
    for processor in data_dict['categories']:
        approx_vgr_dict =  MachineInfo.objects.filter(vendor_id=processor).aggregate(Avg('benchmark__approx_vgr'))
        data_dict['series'].append({'data': approx_vgr_dict['benchmark__approx_vgr__avg']})
        print "poop"
    return data_dict

#if __name__ == "main":
#   avgVGRvsProcessor()
