#                     bp_logger.py
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

__author__ = 'Suryajith Chillara'
__license__ = 'Modified BSD licence'
import os
import logging

from ConfigParser import ConfigParser

class bp_logger(object):
    '''
    A wrapper over the logging module of python.
    '''
    
    logger = None

    def __init__(self, module_name):
        '''
        Constructor
        Logger is a singleton class
        '''
        
        if bp_logger.logger == None :
            
            config = ConfigParser()
            try :
                config.read(['../project_config'])
            except ConfigParser.NoSectionError, e:
                os.chdir('libs/')
                config.read(['../config'])
                os.chdir('../')
            
            os.chdir('libs/')
            config.read(['../project_config'])
            os.chdir('../')
            
            # Open the log file in apend mode.
            logfilename = os.path.join(os.path.dirname(__file__), '../', config.get("locations", "log"),
                                       'benchmark.log')
            
            bp_logger.logger = logging.getLogger(module_name)
            bp_logger.logger.setLevel(logging.DEBUG)
            handler = logging.FileHandler(logfilename)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            bp_logger.logger.addHandler(handler)
            
        
            
    def info(self, message):
        '''
        Write the message as an information
        '''
        bp_logger.logger.info(message)
        
    def warning(self, message):
        '''
        Write the message as a warning
        '''
        bp_logger.logger.warning(message)
        
    def critical(self, message):
        '''
        Write the message as critical
        '''
        bp_logger.logger.critical(message)
    
    def error(self, message):
        '''
        Write the message as an error
        '''
        bp_logger.logger.error(message)
        
    def debug(self, message):
        '''
        Write the message as a debug message
        '''
        bp_logger.logger.debug(message)
    
        
# Local Variables:
# mode: python
# tab-width: 8
# python-indent-offset: 4
# indent-tabs-mode: t
# End:
# ex: shiftwidth=4 tabstop=8       
        