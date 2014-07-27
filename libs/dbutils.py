#                     dbutils.py
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
# This consists of the tools required to access the database. 

__author__ = 'Suryajith Chillara'
__license__ = 'Modified BSD licence'

import os
import sys

import _mysql
import _mysql_exceptions

from ConfigParser import ConfigParser

from libs.bp_logger import bp_logger
import settings
def get_connection():
    """
    Get the cursor for the MySQL connection.
    """
    config = ConfigParser()
    
#    try :
#        config.read(['../config'])
#    except ConfigParser.NoSectionError, e:
#        os.chdir('libs/')
#        config.read(['../config'])
#        os.chdir('../')
#    os.chdir(settings.SITE_ROOT+'libs/')
    config.read([settings.SITE_ROOT+'project_config'])
    os.chdir('../')

    connection = _mysql.connect(host=config.get("database", "host"), 
                                 user=config.get("database", "username"), 
                                 passwd=config.get("database", "password"), 
                                 db=config.get("database", "database"))

    return connection



def db_insert(conn, query):
    """
    Execute the insert the query on the db and return the insert id
    @param conn: Connection
    @param query: Query string to be executed
    """
    logger = bp_logger('dbutils')

    try :
        conn.query(query)
    except _mysql_exceptions.ProgrammingError as (errno, strerror) :
        logger.error("Error: Query error. \n {:d} \t {:s} for query {:s}".format(errno, strerror, query))
        sys.exit(1)
        
    except _mysql_exceptions.IntegrityError as (errno, strerror) :
        logger.error("Error: Query error. \n {:d} \t {:s} for query {:s}".format(errno, strerror, query))
        print "Error: Query error. \n {:d} \t {:s}".format(errno, strerror)
        return False 
       
    return conn.insert_id()



def db_select(conn, query):
    """
    Execute the select query on the db and return the rows
    @param conn: Connection
    @param query: Query string to be executed
    """
        
    conn.query(query)
    result = conn.store_result()
    
    select_data = []
    
    while True :
        row_data = result.fetch_row()
        if not row_data :
            break
        
        select_data.append(row_data[0])
    
    return  select_data



def check_if_file_exists_in_db(conn, md5sum):
    """
    Check if the file already exists in the database by md5sum match
    @param conn: db connection
    @param md5sum: md5sum to check against
    """
    
    query = """
            SELECT COUNT(*) FROM `md5_log` where `md5sum` LIKE \"{:s}\"
            """.format(md5sum)
    
    return int(db_select(conn, query)[0][0])

def close_connection(conn):
    _mysql.connection.close(conn)

# Local Variables:
# mode: python
# tab-width: 8
# python-indent-offset: 4
# indent-tabs-mode: t
# End:
# ex: shiftwidth=4 tabstop=8