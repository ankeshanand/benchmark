__author__ = 'ankesh'
from .models import BenchmarkLogs, MachineInfo
from django.db.models import Sum, Avg


def avgVGRvsProcessor():
    data_dict = {'chart_title': "Average VGR Rating vs Processor Family",
                 'chart_type': "bar",
                 'xAxis_title_text': "Processor Family",
                 'yAxis_title_text': "Average VGR Rating",
                 'categories': [],
                 'values': []}

    distinct_categories_dict = MachineInfo.objects.values('vendor_id').distinct()
    for category in distinct_categories_dict:
        data_dict['categories'].append(category['vendor_id'])
    for processor in data_dict['categories']:
        approx_vgr_dict =  MachineInfo.objects.filter(vendor_id=processor).aggregate(Avg('benchmark__approx_vgr'))
        data_dict['values'].append(approx_vgr_dict['benchmark__approx_vgr__avg'])
    return data_dict

#if __name__ == "main":
#   avgVGRvsProcessor()
