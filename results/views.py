# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from libs.parser import Parser
import os, settings
from plots.models import Md5Log, BenchmarkLogs, MachineInfo, RtAverage, RtMoss, RtBldg391, RtM35, RtSphflake, RtWorld, RtStar

def show_result(request, filename):
    """
    """
    # Parse the file
    if not Md5Log.objects.filter(file_name=filename+'.log'):
        file = settings.MEDIA_ROOT + filename + '.log'
        parser_obj = Parser(file)
        parser_obj.run()

    data_dict = {
    }
    #Query the database for Benchmark data from benchmark_logs table
    file_obj = Md5Log.objects.filter(file_name=filename+'.log')[0]
    data_dict['BRLCAD_Version'] = file_obj.benchmark.brlcad_version
    data_dict['Running_Time'] = file_obj.benchmark.running_time
    data_dict['Time_of_Execution'] = file_obj.benchmark.time_of_execution
    data_dict['VGR_Rating'] = file_obj.benchmark.approx_vgr
    data_dict['Log_VGR'] = file_obj.benchmark.log_vgr
    data_dict['Parameters'] = file_obj.benchmark.params

    #Query the database for System Information from machine_info table
    data_dict['Clock_Speed'] = file_obj.benchmark.machineinfo.cpu_mhz
    data_dict['NCores'] = file_obj.benchmark.machineinfo.cores
    data_dict['NProcessors'] = file_obj.benchmark.machineinfo.processors
    data_dict['Vendor_ID'] = file_obj.benchmark.machineinfo.vendor_id
    data_dict['OS_Type'] = file_obj.benchmark.machineinfo.ostype
    data_dict['Processor_Model_Name'] = file_obj.benchmark.machineinfo.model_name

    #Query the database for individual Image Performance
    data_dict['Rt_Average'] = file_obj.benchmark.rtaverage_set.all()[0].abs_rps
    data_dict['Rt_Bldg391'] = file_obj.benchmark.rtbldg391_set.all()[0].abs_rps
    data_dict['Rt_M35'] = file_obj.benchmark.rtm35_set.all()[0].abs_rps
    data_dict['Rt_Moss'] = file_obj.benchmark.rtmoss_set.all()[0].abs_rps
    data_dict['Rt_Sphlake'] = file_obj.benchmark.rtbldg391_set.all()[0].abs_rps
    data_dict['Rt_Star'] = file_obj.benchmark.rtstar_set.all()[0].abs_rps
    data_dict['Rt_World'] = file_obj.benchmark.rtworld_set.all()[0].abs_rps

    return render_to_response('result.html', data_dict, context_instance=RequestContext(request))



