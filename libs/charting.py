#                     charting.py
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
# 
# Wrapper over Google Charts
# Creates the js code to be embedded into the browser.
# 

from bottle import run, route

class Charts :
    """
    Base class for the wrapper over GCharts
    """
    title = 'Chart'
    chart_type = None
    options = None
    options_code = "var options = null;"
    base_code = """

<!--Load the AJAX API-->

<script type="text/javascript" src="https://www.google.com/jsapi"></script>
<script type="text/javascript">

    // Load the Visualization API and the piechart package.
    google.load('visualization', '1', {'packages':['{{package}}']});

    // Set a callback to run when the Google Visualization library is loaded.
    google.setOnLoadCallback(drawChart);

    
    // Callback that creates and populates a data table,
    // instantiates the pie chart, passes in the data and
    // draws it.
    function drawChart() {
    
        {{content}}
    
        {{options}}
    
        var chart = new google.visualization.{{chart_type}}(document.getElementById('charts_div'));
        chart.draw(data, options);
    
    }
</script>
            """
        
    def __init__(self):
        pass
        
    def render(self):
        """
        Dummy method for the inheritors to implement
        """
        pass
    
    
    def create_table_from_data(self, data, base):
        """
        Construct the data table for Google visualization
        """
        data_init = "var data = new google.visualization.DataTable();"
        
        table_rows = self.order_the_data(data, base)
        headings = table_rows[0]
        row_data = table_rows[1]
        
        
        col_types = []
        for i in xrange(0, len(headings)) :
            
            data_type = False
            if isinstance(row_data[i], str) :
                data_type = 'string'
            elif isinstance(row_data[i], int) or isinstance(row_data[i], float) :
                data_type = 'number'
            elif isinstance(row_data[i], bool) :
                data_type = 'boolean'
            else :
                data_type = 'string'
            col_types.append({'type' : data_type, 'value' : headings[i]})
        
        column_code = self.create_columns(col_types)
        
        del table_rows[0]
        
        row_code = self.create_rows(table_rows)
        
        return data_init+column_code+row_code
    
        
    def create_columns(self, columns):
        """
        Create columns for adding data to the dataTable of google visualization
        """
        code_gen = ""
        for column in columns :
            code_gen += "data.addColumn('{:s}', '{:s}');".format(column['type'], column['value'])
        return code_gen
                 
                                        
    
    def create_rows(self, rows):
        """
        Create columns for adding data to the dataTable of google visualization
        """
        
        code_gen = "data.addRows(["
        row_text = []
        for row in rows :
            ind_row_text = []
            for element in row :
                if isinstance(element, str) :
                    ind_row_text.append('\'{:s}\''.format(element))
                elif isinstance(element, int) :
                    ind_row_text.append('{:d}'.format(element))
                elif isinstance(element, float) :
                    ind_row_text.append('{:f}'.format(element))
                else :
                    ind_row_text.append('\'{:s}\''.format(element))
                
            row_text.append("[ {:s} ]".format(",".join(ind_row_text)))
            
        code_gen += ','.join(row_text) + "]);"
        
        return code_gen
    
    
    
    def construct_options(self, options):
        """
        Construct options code for the given graph options 
        """
        if self.options == None :
            return self.options_code
        
        return """
                var options = { 
                                title : '{{main_title}}',
                                hAxis : {title : \'{{h_title}}\'}, 
                                vAxis : {title : \'{{v_title}}\'},
                                pointSize : 3
                                };
                """.replace('{{main_title}}', options['t']).replace('{{h_title}}', options['h']).replace('{{v_title}}', options['v'])
                
    
    def create_data_table(self, data, base):
        """
        Create data table for arrayToDataTable method instead of DataTable()
        of Google Visualization 
        """
        data_table_base_code = "var data = google.visualization.arrayToDataTable(["
        
        table_rows = self.order_the_data(data, base)
        table_rows = map(str, table_rows)
        data_table_base_code += ','.join(table_rows)+"]);"
        
        return data_table_base_code
    
    def order_the_data(self, data, base):
        
        table_rows = []
        count = 0
        
        for row in data :
            temp = row
            if count == 0 :
                keys = row.keys()
                keys.remove(base)
                new_order = [base]
                new_order.extend(keys)
                table_rows.append(new_order)
            
            base_value = temp[base]
            del temp[base]
            new_order_val = [base_value]
            new_order_val.extend(temp.values())
            table_rows.append(new_order_val)
            count += 1
            
        return table_rows
    


class PieChart(Charts):
    """
    Class to create PieCharts
    """
    def __init__(self, columns, rows, options = None):
        """
        Initialization
        """
        self.chart_type = 'PieChart'
        self.options = options
        self.columns = columns
        self.rows = rows
    
    
    def render(self):
        """
        Method that returns the html code with js code embedded
        """
        data_init = "var data = new google.visualization.DataTable();"
        columns_code = self.create_columns(self.columns)
        rows_code = self.create_rows(self.rows)
        content = data_init+columns_code+rows_code
        options = self.construct_options(self.options)
        return self.base_code.replace('{{package}}', 'corechart').replace('{{content}}', content).replace('{{options}}', options).replace('{{chart_type}}', self.chart_type)



class LineChart(Charts) :
    """
    Class that constructs and renders Line charts by inheriting charts
    """
    def __init__(self, data, base, options = None):
        """
        Initialization
        """
        self.chart_type = 'LineChart'
        self.options = options
        self.base = base
        self.data = data        
    
    
    def render(self):
        """
        Method that returns the html code with js code embedded
        """
        content = self.create_data_table(self.data, self.base)
        options = self.construct_options(self.options)
        
        return self.base_code.replace('{{package}}', 'corechart').replace("{{content}}", content).replace("{{options}}", options).replace('{{chart_type}}', self.chart_type)
    

class TableChart(Charts) :
    """
    Class that constructs and renders Line charts by inheriting charts
    """
    def __init__(self, data, base, options = None):
        """
        Initialization
        """
        self.chart_type = 'Table'
        self.options = None
        self.base = base
        self.data = data        
    
    
    def render(self):
        """
        Method that returns the html code with js code embedded
        """
        content = self.create_table_from_data(self.data, self.base)
        options = self.construct_options(None)
        return self.base_code.replace('{{package}}', 'table').replace("{{content}}", content).replace("{{options}}", options).replace('{{chart_type}}', self.chart_type)
    
        
class ColumnChart(Charts) :
    """
    Class to create Column charts
    """
    
    def __init__(self, data, options = None) :
        """
        Initialization
        """
        self.chart_type = 'ColumnChart'
        self.options = options
        self.data = data
    
    # TODO: Need to fix the upper and lower limits properly. Render of the last two columns fails
    def render(self):
        """
        Method that returns the html code with js code embedded
        """
        content = self.create_data_table(self.data)
        options = self.construct_options(self.options)
        return self.base_code.replace("{{content}}", content).replace("{{options}}", options).replace('{{chart_type}}', self.chart_type)


"""
# Example code implementation is as follows :



@route('/line', method='GET')
def line_chart() :
    
    data = [{'base' : 'a', 'value1' : 10, 'value2' : 15}, 
            {'base' : 'b', 'value1' : 20, 'value2' : 25}, 
            {'base' : 'c', 'value1' : 30, 'value2' : 35}, 
            {'base' : 'd', 'value1' : 40, 'value2' : 45}]
    
    chart = LineChart(data)
    return chart.render()
    
run(host='localhost', port='8080')
"""

# Local Variables:
# mode: python
# tab-width: 8
# python-indent-offset: 4
# indent-tabs-mode: t
# End:
# ex: shiftwidth=4 tabstop=8          