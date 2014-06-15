__author__ = 'ankesh'
from .models import BenchmarkLogs, MachineInfo, RtAverage, RtBldg391, RtM35, RtMoss, RtSphflake, RtStar, RtWorld
from django.db.models import Sum, Avg, get_model


def avgVGRvsProcessorFamily():
    """
    Returns the aggregated data for Average VGR vs processor Family plot in the form of a dictionary.
    """
    data_dict = {'chart_title': "Average VGR Rating vs Processor Family",
                 'chart_type': "bar",
                 'xaxis_title': "Processor Family",
                 'yaxis_title': "Average VGR Rating",
                 'categories': [],
                 'series_type': "single",
                 'values': []}

    distinct_categories_dict = MachineInfo.objects.values('vendor_id').distinct()
    for category in distinct_categories_dict:
        data_dict['categories'].append(category['vendor_id'])
    for processor in data_dict['categories']:
        approx_vgr_dict = MachineInfo.objects.filter(vendor_id=processor).aggregate(Avg('benchmark__approx_vgr'))
        value_pair = [processor, approx_vgr_dict['benchmark__approx_vgr__avg']]
        data_dict['values'].append(value_pair)
    return data_dict


def avgVGRvsOSType():
    """
    Returns the aggregated data for Average VGR vs OS Type plot in the form of a dictionary.
    """
    data_dict = {'chart_title': "Average VGR Rating vs Operating System Type",
                 'chart_type': "bar",
                 'yaxis_title': "Average VGR Rating",
                 'xaxis_title': "Operating System Type",
                 'categories': [],
                 'series_type': "single",
                 'values': []}
    distinct_categories_dict = MachineInfo.objects.values('ostype').distinct()
    for category in distinct_categories_dict:
        data_dict['categories'].append(category['ostype'])
    for os in data_dict['categories']:
        approx_vgr_dict = MachineInfo.objects.filter(ostype=os).aggregate(Avg('benchmark__approx_vgr'))
        value_pair = [os, approx_vgr_dict['benchmark__approx_vgr__avg']]
        data_dict['values'].append(value_pair)
    return data_dict


def avgVGRvsNCores():
    """
    Returns the aggregated data for Average VGR vs Number of CPUs plot in the form of a dictionary.
    """
    data_dict = {'chart_title': "Average VGR Rating vs Number of Cores",
                 'chart_type': "line",
                 'yaxis_title': "Average VGR Rating",
                 'xaxis_title': "Number of CPUs",
                 'categories': [],
                 'series_type': "single",
                 'values': []}
    distinct_number_dict = MachineInfo.objects.values('cores').distinct()
    for number in distinct_number_dict:
        data_dict['categories'].append(number['cores'])
    for number in data_dict['categories']:
        approx_vgr_dict = MachineInfo.objects.filter(cores=number).aggregate(Avg('benchmark__approx_vgr'))
        value_pair = [number, approx_vgr_dict['benchmark__approx_vgr__avg']]
        data_dict['values'].append(value_pair)
    return data_dict


def avgVGRvsNProcessors():
    """
    Returns the aggregated data for Average VGR vs Number of Processors plot in the form of a dictionary.
    """
    data_dict = {'chart_title': "Average VGR Rating vs Number of Processors",
                 'chart_type': "line",
                 'yaxis_title': "Average VGR Rating",
                 'xaxis_title': "Number of Processors",
                 'categories': [],
                 'series_type': "single",
                 'values': []}
    distinct_number_dict = MachineInfo.objects.values('processors').distinct()
    for number in distinct_number_dict:
        data_dict['categories'].append(number['processors'])
    for number in data_dict['categories']:
        approx_vgr_dict = MachineInfo.objects.filter(processors=number).aggregate(Avg('benchmark__approx_vgr'))
        value_pair = [number, approx_vgr_dict['benchmark__approx_vgr__avg']]
        data_dict['values'].append(value_pair)
    return data_dict



def logVGRvsProcessorFamily():
    """
    Returns the aggregated data for Logarithmic VGR vs Processor Family plot in the form of a dictionary.
    """
    data_dict = {'chart_title': "Logarithmic VGR Rating vs Processor Family",
                 'chart_type': "bar",
                 'xaxis_title': "Processor Family",
                 'yaxis_title': "Logarithmic VGR Rating",
                 'categories': [],
                 'series_type': "single",
                 'values': []}

    distinct_categories_dict = MachineInfo.objects.values('vendor_id').distinct()
    for category in distinct_categories_dict:
        data_dict['categories'].append(category['vendor_id'])
    for processor in data_dict['categories']:
        log_vgr_dict = MachineInfo.objects.filter(vendor_id=processor).aggregate(Avg('benchmark__log_vgr'))
        value_pair = [processor, log_vgr_dict['benchmark__approx_vgr__avg']]
        data_dict['values'].append(value_pair)
    return data_dict


def logVGRvsOSType():
    """
    Returns the aggregated data for Logarithmic VGR vs OS Type plot in the form of a dictionary.
    """
    data_dict = {'chart_title': "Average VGR Rating vs Operating System Type",
                 'chart_type': "bar",
                 'yaxis_title': "Average VGR Rating",
                 'xaxis_title': "Operating System Type",
                 'categories': [],
                 'series_type': "single",
                 'values': []}
    distinct_categories_dict = MachineInfo.objects.values('ostype').distinct()
    for category in distinct_categories_dict:
        data_dict['categories'].append(category['ostype'])
    for os in data_dict['categories']:
        log_vgr_dict = MachineInfo.objects.filter(ostype=os).aggregate(Avg('benchmark__log_vgr'))
        value_pair = [os, log_vgr_dict['benchmark__approx_vgr__avg']]
        data_dict['values'].append(value_pair)
    return data_dict


def logVGRvsNCores():
    """
    Returns the aggregated data for Logarithmic VGR vs Number of CPUs plot in the form of a dictionary.
    """
    data_dict = {'chart_title': "Logarithmic VGR Rating vs Number of Cores",
                 'chart_type': "bar",
                 'yaxis_title': "Logarithmic VGR Rating",
                 'xaxis_title': "Number of CPUs",
                 'categories': [],
                 'series_type': "single",
                 'values': []}
    distinct_number_dict = MachineInfo.objects.values('cores').distinct()
    for number in distinct_number_dict:
        data_dict['categories'].append(number['cores'])
    for number in data_dict['categories']:
        log_vgr_dict = MachineInfo.objects.filter(cores=number).aggregate(Avg('benchmark__log_vgr'))
        value_pair = [number, log_vgr_dict['benchmark__approx_vgr__avg']]
        data_dict['values'].append(value_pair)
    return data_dict


def runningTimevsProcessorFamily():
    """
    Returns the aggregated data for Running Time vs processor Family plot in the form of a dictionary.
    """
    data_dict = {'chart_title': "Running Time against Processor Family",
                 'chart_type': "bar",
                 'xaxis_title': "Processor Family",
                 'yaxis_title': "Running Time",
                 'categories': [],
                 'series_type': "single",
                 'values': []}
    distinct_categories_dict = MachineInfo.objects.values('vendor_id').distinct()
    for category in distinct_categories_dict:
        data_dict['categories'].append(category['vendor_id'])
    for processor in data_dict['categories']:
        running_time_dict = MachineInfo.objects.filter(vendor_id=processor).aggregate(Avg('benchmark__running_time'))
        value_pair = [processor, running_time_dict['benchmark__running_time__avg']]
        data_dict['values'].append(value_pair)
    return data_dict


def absPerformancevsRefImages():
    data_dict = {'chart_title': "Absolute Rays Per Sec against Reference Images",
                 'chart_type': "bar",
                 'xaxis_title': "Image",
                 'yaxis_title': "Absolute Rays per Sec",
                 'series_type': "single",
                 'categories': ["Moss", "World", "Star", "Bldg391", "M35", "Sphflake"],
                 'values': []}
    for category in data_dict['categories']:
        model_name = "Rt"+category
        model_class = get_model('plots', model_name)
        value_pair = [category, model_class.objects.all().aggregate(Avg('abs_rps'))['abs_rps__avg']]
        data_dict['values'].append(value_pair)
    return data_dict


def processorFamiliesvsRefImages():
    """
    Returns the aggregated data for the performance of Processor Families against Reference Images plot
    in the form of a dictionary.
    """
    data_dict = {'chart_title': "Absolute Rays Per Sec against Reference Images",
                 'chart_type': "line",
                 'xaxis_title': "Image",
                 'yaxis_title': "Absolute Rays per Sec",
                 'series_type': "multi",
                 'categories': ["Moss", "World", "Star", "Bldg391", "M35", "Sphflake"],
                 'labels': [],
                 'values': []}
    processor_dict = MachineInfo.objects.values('vendor_id').distinct()
    series_data = []
    for processor in processor_dict:
        for category in data_dict['categories']:
            model_name = 'Rt'+category
            field = model_name.lower()
            value_pair = [category,
                          BenchmarkLogs.objects.filter(machineinfo__vendor_id=processor['vendor_id'])
                              .aggregate(Avg(field+'__abs_rps'))[field+'__abs_rps__avg']]
            series_data.append(value_pair)
        data_dict['labels'].append(processor['vendor_id'])
        data_dict['values'].append(series_data)
    return data_dict


def avgVGRvsCPUmhz():
    """
    Returns the aggregated data for Average VGR vs CPU MHz plot in the form of a dictionary.
    """
    data_dict = {'chart_title': "Efficiency: Average VGR Rating vs CPU MHz",
                 'chart_type': "line",
                 'yaxis_title': "Average VGR Rating",
                 'xaxis_title': "CPU MHz",
                 'categories': [],
                 'series_type': "single",
                 'values': []}
    distinct_number_dict = MachineInfo.objects.values('cpu_mhz').distinct()
    for number in distinct_number_dict:
        data_dict['categories'].append(number['cpu_mhz'])
    for number in data_dict['categories']:
        approx_vgr_dict = MachineInfo.objects.filter(cpu_mhz=number).aggregate(Avg('benchmark__approx_vgr'))
        value_pair = [number, approx_vgr_dict['benchmark__approx_vgr__avg']]
        data_dict['values'].append(value_pair)
    return data_dict