#                     perf_vs_images.py
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



@app.route('/absperformance', method = 'GET')
def perf_vs_images_form():
    """
    Return the form so as to be rendered as a part of the template
    """
    
    return template('plot', title='Absolute Performance vs Images over various Architectures', 
                    form=get_perf_vs_images_form(), js_code='',
                    msg='', text_result='')


    
@app.route('/absperformance', method = 'POST')
def absolute_perf_vs_images():
    """
    Absolute Performance vs Reference images over various architectures
    """
    
    
    output_type = request.forms.get('output_type')
    
    models = request.forms.getall('models')
    
    if len(models) == 0 :
        model_comparision_query = ''
    else :
        model_comp = []
        for model in models :
            model_comp.append("\'{:s}\'".format(model))
        model_comparision_query = " WHERE model_name IN ({:s})".format(",".join(model_comp))
        
    conn = dbutils.get_connection()
    
    tests = ['moss', 'world', 'star', 'bldg391', 'm35', 'sphflake', 'average']
    
    data = []
    
    for test in tests :
        
        query = """
                SELECT AVG( abs_rps ) , model_name
                FROM `rt_{:s}` r
                JOIN machine_info m ON r.benchmark_id = m.benchmark_id
                {:s}
                GROUP BY model_name 
                """.format(test, model_comparision_query)
                
        results = dbutils.db_select(conn, query)
        
        table_row = {'Image' : test}
        
        for row in results :
            table_row[row[1]] = float(row[0])
            
        data.append(table_row)
    
    options = {'t' : 'Absolute Performance vs Images over various Architectures', 'h' : 'Reference Images', 'v' : 'Absolute Performance'}    
    
    script = ''
    if output_type == 'graph' :
        
        chart = LineChart(data, 'Image', options)
        script = chart.render()
    
    elif output_type == 'table' :
        
        chart = TableChart(data, 'Image')
        script = chart.render()
        
    return template('plot', title='Absolute Performance vs Images over various Architectures', 
                    form=get_perf_vs_images_form(), js_code=script,
                    msg='', text_result='')


def get_perf_vs_images_form():
    """
    Generate the form
    """
    conn = dbutils.get_connection()
    
    query = "SELECT DISTINCT model_name from machine_info"
    results = dbutils.db_select(conn, query)
    
    model_options = {}
    for result in results :
        model_options[result[0]] = result[0]
    
    output_options = {'Graph' : 'graph', 'Table' : 'table'}
    
    form = Form('/absperformance', 'POST')
    
    form.add_select_field('Models to Compare', 'models', model_options, True)
    form.add_select_field('Output Type', 'output_type', output_options)
    
    return form.render()


# Local Variables:
# mode: python
# tab-width: 8
# python-indent-offset: 4
# indent-tabs-mode: t
# End:
# ex: shiftwidth=4 tabstop=8