#                     upload.py
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
# 
# 

import os
import sys
import hashlib

from bottle import request
from ConfigParser import ConfigParser

from src import app

import libs.util as utils
from libs.bp_logger import bp_logger



@app.route('/upload', method='GET')
def upload_form():
    return '''<form action="/upload" method="post" enctype="multipart/form-data">
                <input name="logfile"  type="file" />
                <input type='submit' />
              </form>'''
    

@app.route('/upload', method='POST')
def upload_submit():
    
    logger = bp_logger('Upload_file_form')
    file = request.forms.get('file')
    data = request.files.logfile
    
    filename = data.filename
    filecontent =  data.file.read()
    
    config = ConfigParser()
    os.chdir('libs/')
    config.read(['../config'])
    os.chdir('../')
    
    filelocation = os.path.join(config.get("locations", 'queue'), filename)
    
    md5 = hashlib.md5()
    md5.update(filecontent)
    md5_hash = md5.hexdigest()
    filelocation = filelocation + '.' + md5_hash
    
    if not utils.check_if_file_exists_on_disk(filelocation) :
        f = open(filelocation, 'w')
        f.write(filecontent)
        f.close()
        logger.info("Wrote the file as follows : {:s}".format(filelocation))
        
        return "Successfully uploaded the file {:s}".format(filename)
    else :
        logger.error("The file {:s} already exists in the queue".format(filename))
        return "Sorry the file {:s} already exists in the queue".format(filename)



# Local Variables:
# mode: python
# tab-width: 8
# python-indent-offset: 4
# indent-tabs-mode: t
# End:
# ex: shiftwidth=4 tabstop=8
