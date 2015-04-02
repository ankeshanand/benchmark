#                     get_email_attachments.py
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
# Get the attachments from all the unread emails.

__author__ = 'Suryajith Chillara'
__license__ = 'Modified BSD licence'

import os
import re
import sys
import hashlib

from ConfigParser import ConfigParser

sys.path.append("../")

import libs.util as util
import libs.dbutils as dbutils
import libs.imaputils as imaputils

from libs.bp_logger import bp_logger



def main():
    """
    Main
    """

    logger = bp_logger('GET_EMAIL_ATTACHMENTS')

    config = ConfigParser()
    config.read(['../project_config'])

    imap_server = imaputils.get_imapserv_conn()

    connection = dbutils.get_connection()

    # This lists out the list of all the
    msg, emails = imap_server.search(None, "(UNSEEN)")
    # print emails


    # Go through each of the ids given out by IMAP
    for email_id in emails[0].split() :

        attachments = imaputils.get_attachment(imap_server, email_id)

        for filename, content in attachments.items() :

            # Filename has to match the required pattern.
            if re.search("run-[0-9]+-benchmark.log", filename) == None :
                logger.debug("The filename {:s} did not match the needed pattern. IMAP id : {:d}".format(filename, int(email_id)))
                continue


            filelocation = os.path.join(config.get("locations", "queue"), filename)

            md5 = hashlib.md5()
            md5.update(content)
            md5_hash = md5.hexdigest()
            filelocation = filelocation + '.' + md5_hash


            #
            if util.check_if_file_exists_on_disk(filelocation) :
                logger.debug("The file {:s} exists on the disk.".format(filelocation))
                continue
            else :
                file_queue = open(filelocation, 'w')
                file_queue.write(content)
                logger.info("The file {:s} has been written to the disk.".format(filelocation))
                file_queue.close()

            # Add code to write it to the db
            query = """
                    INSERT INTO email_logs (`imap_id`, `md5`, `time`)
                    VALUES ({:d}, \"{:s}\", NOW())
                    """.format(int(email_id), md5_hash)

            hw_id = dbutils.db_insert(connection, query)

            if hw_id == None :
                logger.error("The query \n {:s} has not been inserted.".format(query))




if __name__ == '__main__':
    main()

# Local Variables:
# mode: python
# tab-width: 8
# python-indent-offset: 4
# indent-tabs-mode: t
# End:
# ex: shiftwidth=4 tabstop=8
