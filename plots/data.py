__author__ = 'ankesh'
from .models import BenchmarkLogs, MachineInfo
from django.db.models import Sum, Avg


def avgVGRvsProcessorFamily():
    """
    Returns the aggregated data for Average VGR vs processor Family plot in the form of a dictionary.
    """
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
        approx_vgr_dict = MachineInfo.objects.filter(vendor_id=processor).aggregate(Avg('benchmark__approx_vgr'))
        data_dict['values'].append(approx_vgr_dict['benchmark__approx_vgr__avg'])
    return data_dict


def avgVGRvsOSType():
    """
    Returns the aggregated data for Average VGR vs OS Type plot in the form of a dictionary.
    """
    data_dict = {'chart_title': "Average VGR Rating vs Operating System Type",
                 'chart_type': "bar",
                 'yAxis_title_text': "Average VGR Rating",
                 'xAxis_title_text': "Operating System Type",
                 'categories': [],
                 'values': []}
    distinct_categories_dict = MachineInfo.objects.values('ostype').distinct()
    for category in distinct_categories_dict:
        data_dict['categories'].append(category['ostype'])
    for system in data_dict['categories']:
        approx_vgr_dict = MachineInfo.objects.filter(ostype=system).aggregate(Avg('benchmark__approx_vgr'))
        data_dict['values'].append(approx_vgr_dict['benchmark__approx_vgr__avg'])
    return data_dict


def avgVGRvsNCores():
    """
    Returns the aggregated data for Average VGR vs Number of CPUs plot in the form of a dictionary.
    """
    data_dict = {'chart_title': "Average VGR Rating vs Number of Cores",
                 'chart_type': "bar",
                 'yAxis_title_text': "Average VGR Rating",
                 'xAxis_title_text': "Number of CPUs",
                 'categories': [],
                 'values': []}
    distinct_number_dict = MachineInfo.objects.values('cores').distinct()
    for number in distinct_number_dict:
        data_dict['categories'].append(number['cores'])
    for number in data_dict['categories']:
        approx_vgr_dict = MachineInfo.objects.filter(cores=number).aggregate(Avg('benchmark__approx_vgr'))
        data_dict['values'].append(approx_vgr_dict['benchmark__approx_vgr__avg'])
    return data_dict


def logVGRvsProcessorFamily():
    """
    Returns the aggregated data for Logarithmic VGR vs Processor Family plot in the form of a dictionary.
    """
    data_dict = {'chart_title': "Logarithmic VGR Rating vs Processor Family",
                 'chart_type': "bar",
                 'xAxis_title_text': "Processor Family",
                 'yAxis_title_text': "Logarithmic VGR Rating",
                 'categories': [],
                 'values': []}

    distinct_categories_dict = MachineInfo.objects.values('vendor_id').distinct()
    for category in distinct_categories_dict:
        data_dict['categories'].append(category['vendor_id'])
    for processor in data_dict['categories']:
        log_vgr_dict = MachineInfo.objects.filter(vendor_id=processor).aggregate(Avg('benchmark__log_vgr'))
        data_dict['values'].append(log_vgr_dict['benchmark__log_vgr__avg'])
    return data_dict


def logVGRvsOSType():
    """
    Returns the aggregated data for Logarithmic VGR vs OS Type plot in the form of a dictionary.
    """
    data_dict = {'chart_title': "Average VGR Rating vs Operating System Type",
                 'chart_type': "bar",
                 'yAxis_title_text': "Average VGR Rating",
                 'xAxis_title_text': "Operating System Type",
                 'categories': [],
                 'values': []}
    distinct_categories_dict = MachineInfo.objects.values('ostype').distinct()
    for category in distinct_categories_dict:
        data_dict['categories'].append(category['ostype'])
    for system in data_dict['categories']:
        log_vgr_dict = MachineInfo.objects.filter(ostype=system).aggregate(Avg('benchmark__log_vgr'))
        data_dict['values'].append(log_vgr_dict['benchmark__log_vgr__avg'])
    return data_dict


def logVGRvsNCores():
    """
    Returns the aggregated data for Logarithmic VGR vs Number of CPUs plot in the form of a dictionary.
    """
    data_dict = {'chart_title': "Logarithmic VGR Rating vs Number of Cores",
                 'chart_type': "bar",
                 'yAxis_title_text': "Logarithmic VGR Rating",
                 'xAxis_title_text': "Number of CPUs",
                 'categories': [],
                 'values': []}
    distinct_number_dict = MachineInfo.objects.values('cores').distinct()
    for number in distinct_number_dict:
        data_dict['categories'].append(number['cores'])
    for number in data_dict['categories']:
        log_vgr_dict = MachineInfo.objects.filter(cores=number).aggregate(Avg('benchmark__log_vgr'))
        data_dict['values'].append(log_vgr_dict['benchmark__log_vgr__avg'])
    return data_dict


def runningTimevsProcessorFamily():
    """
    Returns the aggregated data for Running Time vs processor Family plot in the form of a dictionary.
    """
    data_dict = {'chart_title': "Running Time vs Processor Family",
                 'chart_type': "bar",
                 'xAxis_title_text': "Processor Family",
                 'yAxis_title_text': "Running Time",
                 'categories': [],
                 'values': []}

    distinct_categories_dict = MachineInfo.objects.values('vendor_id').distinct()
    for category in distinct_categories_dict:
        data_dict['categories'].append(category['vendor_id'])
    for processor in data_dict['categories']:
        running_time_dict = MachineInfo.objects.filter(vendor_id=processor).aggregate(Avg('benchmark__running_time_vgr'))
        data_dict['values'].append(running_time_dict['benchmark__running_time__avg'])
    return data_dict

