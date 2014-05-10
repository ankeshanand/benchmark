#                     relperformance.py
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
import sys

sys.path.append('../')

import libs.dbutils as dbutils
from libs.charting import LineChart
 
from bottle import run, route

@route('/absperformance', method = 'GET')
def absolute_perf_vs_images():
    """
    Absolute Performance vs Reference images over various architectures
    """
    conn = dbutils.get_connection()
    
    tests = ['moss', 'world', 'star', 'bldg391', 'm35', 'sphflake', 'average']
    data = []
    for test in tests :
        query = """
                SELECT AVG( abs_rps ) , model_name
                FROM `rt_{:s}` r
                JOIN machine_info m ON r.benchmark_id = m.benchmark_id
                GROUP BY model_name 
                """.format(test)
        results = dbutils.db_select(conn, query)
        table_row = {'Image' : test}
        for row in results :
            table_row[row[1]] = float(row[0])
        data.append(table_row)
    
    options = {'t' : 'Absolute Performance vs Images over various Architectures', 'h' : 'Reference Images', 'v' : 'Absolute Performance'}    
    chart = LineChart(data, 'Image', options)
    return chart.render()



@route('/avgperfvsarch', method = 'GET')
def avg_perf_vs_arch():
    """
    Average Performance vs Architectures
    """
    options = {'t' : 'Absolute Average Performance vs Architecture', 'h' : 'Architecture', 'v' : 'Avg Performance'}
    return get_avg_perf_vs_arch(options)

@route('/avgperfpermhz', method = 'GET')
def avg_perf_per_mhz_vs_arch():
    """
    Average Performance oer CPU MHz vs Architectures
    """
    options = {'t' : 'Absolute Average Performance per MHz vs Architecture', 'h' : 'Architecture', 'v' : 'Avg Performance per MHz'}
    return get_avg_perf_vs_arch(options, True)


def get_avg_perf_vs_arch(options, per_mhz = False):
    """
    The utility for both the above mentioned plots.
    """
    conn = dbutils.get_connection()
    if per_mhz == True :
        per_mhz_line = '/cpu_mhz'
    else :
        per_mhz_line = ''
    
    query = """
            SELECT AVG( abs_rps ){:s} , model_name
            FROM `rt_average` r
            JOIN machine_info m ON r.benchmark_id = m.benchmark_id
            GROUP BY model_name
            """.format(per_mhz_line)
    results = dbutils.db_select(conn, query)
    
    table_entries = []
    for row in results :
        table_entries.append({'Arch' : row[1], 'Avg_Perf' : float(row[0])})
    
    
    chart = LineChart(table_entries, 'Arch', options)
    return chart.render()

    
    
# run(host = 'localhost', port = 8080)            

# Local Variables:
# mode: python
# tab-width: 8
# python-indent-offset: 4
# indent-tabs-mode: t
# End:
# ex: shiftwidth=4 tabstop=8