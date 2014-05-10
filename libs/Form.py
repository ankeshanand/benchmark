#                     Form.py
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

class Form(object):
    '''
    classdocs
    '''


    def __init__(self, action, method = 'GET'):
        '''
        Constructor
        '''
        self.fields = []
        self.action = action
        self.method = method 
    
    
    def add_select_field(self, Name, param, options, multiple = False, default = None):
        """
        Create the select field. 
        """
        
        options_html = []
        for opt_name, value in options.items() :
            
            default_html = ''
            
            if not default == None :
                if opt_name == default :
                    default_html = "selected='selected'"
            
            options_html.append("<option value='{:s}' {:s}> {:s} </option>".format(value, default_html, opt_name))
        
        multiple_html = ''
        if multiple == True :
            multiple_html = "multiple='multiple'" 
        
        self.fields.append("<tr> <td> {:s} </td><td> <select name='{:s}' {:s}>\t {:s} \t</select> </td></tr>".format(Name, param, multiple_html,  '\t'.join(options_html)))
        
        
    def add_text_field(self, Name, param):
        """
        Create the text field 
        """
        self.fields.append("<tr> <td> {:s} </td><td> <input type='text' name='{:s}'/> </td> </tr>".format(Name, param))
        
    
    def render(self):
        """
        Render the form as required.
        """
        
        return """
                <form action='{:s}' method='{:s}'>
                    <table>
                    {:s}
                    </br>
                    <tr> <td><input type='submit' name='Submit' /></td> </tr>
                    </table>
                </form>
                """.format(self.action, self.method, '</br>\n\t\t\t\t\t'.join(self.fields))


# Local Variables:
# mode: python
# tab-width: 8
# python-indent-offset: 4
# indent-tabs-mode: t
# End:
# ex: shiftwidth=4 tabstop=8