#                     perf_vs_arch.py
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



@app.route('/avgperfvsarch', method = 'GET')
def perf_vs_arch_form():
    
    return template('plot', title = 'Average Absolute Performance vs Architecture', 
                    form = get_perf_vs_arch_form(), js_code = '',
                    msg = '', text_result = '')


def get_perf_vs_arch_form():
    
    conn = dbutils.get_connection()
    
    query = "SELECT DISTINCT model_name from machine_info"
    results = dbutils.db_select(conn, query)
    
    model_options = {}
    for result in results :
        model_options[result[0]] = result[0]
    
    output_options = {'Graph' : 'graph', 'Table' : 'table'}
    yes_no_opt = {'Yes' : 'yes', 'No' : 'no'}
    
    form = Form('/avgperfvsarch', 'POST')
    
    form.add_select_field('Models to Compare', 'models', model_options, True)
    form.add_select_field('Output Type', 'output_type', output_options)
    form.add_select_field('Get per MHz result ?', 'per_mhz', yes_no_opt)
    
    return form.render()


@app.route('/avgperfvsarch', method = 'POST')
def avg_perf_vs_arch():
    """
    Average Performance vs Architectures
    """
    
    output_type = request.forms.get('output_type')
    per_mhz = request.forms.get('per_mhz')
    models = request.forms.getall('models')
    
    if per_mhz == 'yes' :
        per_mhz_line = '/cpu_mhz'
    else :
        per_mhz_line = ''
    
    
    options = {'t' : 'Average Absolute Performance{:s} vs Architecture'.format(per_mhz_line), 
               'h' : 'Architecture', 'v' : 'Avg Performance'}
    
    conn = dbutils.get_connection()
        
    
    where_clauses = []
    
    if not len(models) == 0 :
        model_comp = []
        for model in models :
            model_comp.append("\'{:s}\'".format(model))
        where_clauses.append(" model_name IN ({:s}) ".format(",".join(model_comp)))
    
    if not len(where_clauses) == 0 :
        where_query = "WHERE "+" AND ".join(where_clauses)
    else :
        where_query = ''
        
    query = """
            SELECT AVG( abs_rps ){:s} , model_name
            FROM `rt_average` r
            JOIN machine_info m ON r.benchmark_id = m.benchmark_id
            {:s}
            GROUP BY model_name
            """.format(per_mhz_line, where_query)
            
    results = dbutils.db_select(conn, query)
    
    
    if len(results) <= 1 :
        return template('plot', title = 'Average Absolute Performance{:s} vs Architecture'.format(per_mhz_line), 
                    form = get_perf_vs_arch_form(), js_code = '',
                    msg = 'Select atleast two architectures', text_result = '')
        
    table_entries = []
    for row in results :
        table_entries.append({'Arch' : row[1], 'Avg_Perf' : float(row[0])})
    
    if output_type == 'graph' :
        
        chart = LineChart(table_entries, 'Arch', options)
        script = chart.render()
    
    elif output_type == 'table' :
        
        chart = TableChart(table_entries, 'Arch', options)
        script = chart.render()
    
    return template('plot', title = 'Average Absolute Performance{:s} vs Architecture'.format(per_mhz_line), 
                    form = get_perf_vs_arch_form(), js_code = script,
                    msg = '', text_result = '')
    


# Local Variables:
# mode: python
# tab-width: 8
# python-indent-offset: 4
# indent-tabs-mode: t
# End:
# ex: shiftwidth=4 tabstop=8