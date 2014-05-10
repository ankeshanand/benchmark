#                     imageperf_vs_cpus.py
# BRL-CAD
#
# Copyright (c) 2007-2012 United States Government as represented by
# the U.S. Army Research Laboratory.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following
# disclaimer in the documentation and/or other materials provided
# with the distribution.
#
# 3. The name of the author may not be used to endorse or promote
# products derived from this software without specific prior written
# permission.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS
# OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
# GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
###

import os
import sys


from src import app

import libs.dbutils as dbutils
from libs.Form import Form
from libs.charting import LineChart, TableChart
 
from bottle import request, template



@app.route('/imgperfvscpus', method = 'GET')
def perf_vs_cpus_form():
    
    return template('plot', title = 'Image Performance vs Number of CPUs', 
                    form = get_img_perf_vs_cpus_form(), js_code = '',
                    msg = '', text_result = '')


def get_img_perf_vs_cpus_form():
    
    conn = dbutils.get_connection()
    
    query = "SELECT DISTINCT model_name from machine_info"
    results = dbutils.db_select(conn, query)
    
    model_options = {}
    for result in results :
        model_options[result[0]] = result[0]
    
    output_options = {'Graph' : 'graph', 'Table' : 'table'}
    
    form = Form('/imgperfvscpus', 'POST')
    
    form.add_select_field('Models to Compare', 'models', model_options)
    # form.add_text_field('CPU MHz limit (Leave empty if you choose not to use this)', 'cpu_limit')
    form.add_select_field('Output Type', 'output_type', output_options)
    
    return form.render()


@app.route('/imgperfvscpus', method = 'POST')
def img_perf_vs_cpus():
    """
    Average Performance vs Architectures
    """
    
    output_type = request.forms.get('output_type')
    # cpu_limit = request.forms.get('cpu_limit')
    model = request.forms.get('models')
        
    
    options = {'t' : 'Image Performance vs Number of CPUs', 
               'h' : 'CPUs', 'v' : 'Avg Performance'}
    
    
    conn = dbutils.get_connection()
        
    
    where_clause = " WHERE model_name IN ('{:s}') ".format(model)
    
    
    tests = ['moss', 'world', 'star', 'bldg391', 'm35', 'sphflake', 'average']
    agg_results = []
    
    for test in tests :
        query = """
                SELECT cores, AVG( abs_rps ), '{:s}'
                FROM `rt_{:s}` r
                JOIN machine_info m ON r.benchmark_id = m.benchmark_id
                {:s}
                GROUP BY model_name, cores
                """.format(test, test, where_clause)
        
        results = dbutils.db_select(conn, query)
        agg_results.extend(results)
        
    table_entries = []
    
    cores_data = {}
    for result in agg_results :
        try :
            cores_data[result[0]][result[2]] = float(result[1])
        except KeyError, e:
            cores_data[result[0]] = {}
            for test in tests :
                cores_data[result[0]][test] = 0
            
            cores_data[result[0]][result[2]] = float(result[1])
    
    for cores, results in cores_data.items() :
        temp = results
        temp.update({'cores' : cores})
        table_entries.append(temp)
            
    
    if output_type == 'graph' :
        
        chart = LineChart(table_entries, 'cores', options)
        script = chart.render()
    
    elif output_type == 'table' :
        
        chart = TableChart(table_entries, 'cores', options)
        script = chart.render()
    
    return template('plot', title = 'Image Performance vs Number of CPUs', 
                    form = get_img_perf_vs_cpus_form(), js_code = script,
                    msg = '', text_result = '')
    


# Local Variables:
# mode: python
# tab-width: 8
# python-indent-offset: 4
# indent-tabs-mode: t
# End:
# ex: shiftwidth=4 tabstop=8