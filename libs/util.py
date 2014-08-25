#                     util.py
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
# Generic utility functions to be used elsewhere.
# 

__author__ = 'Suryajith Chillara'
__license__ = 'Modified BSD licence'

import re
import os
import shutil
import hashlib


from ConfigParser import ConfigParser

def convert_month_to_digit(month):
    """
    A method to convert posix date output to timestamp format
    @param month : Text version of month
    """

    month_reference = {'Jan' : '01', 'Feb' : '02', 'Mar' : '03', 'Apr' : '04', 
                       'May' : '05', 'Jun' : '06', 'Jul' : '07', 'Aug' : '08',
                       'Sep' : '09', 'Oct' : '10', 'Nov' : '11', 'Dec' : '12'}
    
    return month_reference[month]


def time_conversion(date_string):
    """
    Convert the date from a format posix date to MySQL date
    @param date_string: date in the posix date command form
    """    
    date_split = date_string.split(' ')
    return "{year}-{mm}-{dd} {time}".format(year = date_split[5],
                                            mm = convert_month_to_digit(date_split[1]),
                                            dd = date_split[2],
                                            time = date_split[3])

    

def check_if_file_exists_on_disk(filepath):
    """
    Checks if the file exists on the disk.
    Could use os.path.exists() but some its safer to do that following.
    @param filepath: path to the file including the filename
    """
    try :
        with open(filepath) as f : 
            return True
    except :
        return False  

    
def archive_file(path):
    """
    Move the file into the archive folder.
    FIXME: 2 different files can contain same name as the process id could be the same. 
    Should change the naming scheme in archives.
    """    
    config = ConfigParser()
    config.read(['../project_config'])
    
    
    # shutil is the safest way to move files
    shutil.move(os.path.join(os.getcwd(), path), 
                os.path.join(os.path.dirname('__FILE__'), '../',
                             config.get("locations", "archives")))
    
    

def md5_for_file(file_desc):
    """
    Return the md5 hexdigest of the file.
    @param file_desc: File descriptor for the file whose digest is needed
    """
    md5 = hashlib.md5()
    while True:
        data = file_desc.read(128)
        if not data:
            break
        md5.update(data)
    return md5.hexdigest()


def sanitize_file(content):
    """
    Sanitizing content for queries
    @param content: content of the file as in iterator
    """
    
    new_content = []
    for line in content :
        new_content.append(re.sub("\"", "", line))
        
    return "\n".join(new_content)

# Local Variables:
# mode: python
# tab-width: 8
# python-indent-offset: 4
# indent-tabs-mode: t
# End:
# ex: shiftwidth=4 tabstop=8