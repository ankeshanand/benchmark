#                     email_verifier.py
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
import re
import sys
import hashlib

from ConfigParser import ConfigParser


sys.path.append("../")

import libs.util as util
import libs.dbutils as dbutils
import libs.imaputils as imaputils
from libs.bp_logger import bp_logger


def is_email_logged(db_conn, email_id):
    """
    Check if the file has been logged into the db.
    """
    query = """
            SELECT * from email_logs where imap_id = {:d}
            """.format(int(email_id))

    result = dbutils.db_select(db_conn, query)

    if len(result) == 0 :
        return False
    else :
        return True




def is_content_same(imap_server, email_id):
    """
    Check if the content is the same on the disk and the mail.
    """

    config = ConfigParser()
    config.read(['../project_config'])

    attachments = imaputils.get_attachment(imap_server, email_id)

    for filename, content in attachments.items() :


        if re.search("run-[0-9]+-benchmark.log", filename) == None :
                continue


        filelocation_archive = os.path.join(os.path.dirname('__FILE__'), '../',
                                            config.get("locations", "archives"), filename)
        filelocation_queue = os.path.join(os.path.dirname('__FILE__'), '../',
                                          config.get("locations", "queue"), filename)


        md5 = hashlib.md5()
        md5.update(content)
        md5_hash = md5.hexdigest()
        filelocation_archive = filelocation_archive + '.' + md5_hash
        filelocation_queue = filelocation_queue + '.' + md5_hash


        #
        if util.check_if_file_exists_on_disk(filelocation_archive) :
            if util.md5_for_file(open(filelocation_archive, 'r')) == md5_hash :
                return True
            else :
                os.remove(filelocation_archive)
                return False
        elif util.check_if_file_exists_on_disk(filelocation_queue) :
            if util.md5_for_file(open(filelocation_queue, 'r')) == md5_hash :
                return True
            else :
                os.remove(filelocation_queue)
                return False
        else :
            return False


def verify_email(imap_server, db_conn, email_id):
    """
    Verify if the extraction is proper.
    """
    return is_email_logged(db_conn, email_id) and is_content_same(imap_server, email_id)


def main():
    """
    MAIN
    """

    logger = bp_logger('EMAIL_VERIFIER')

    imap_server = imaputils.get_imapserv_conn()
    db_conn = dbutils.get_connection()

    query = """
            SELECT MAX(`verified_till`) FROM email_verification_logs
            """
    result = dbutils.db_select(db_conn, query)
    if result[0][0] == None :
        start = 0
    else :
        start = int(result[0][0])

    end = start


    msg, emails = imap_server.search(None, "SEEN")

    for email_id in emails[0].split() :

        if email_id <= start :
            continue


        # TODO: Make this operation occur as batchwise processing
        if verify_email(imap_server, db_conn, email_id) :
            logger.info("Everything seems alright.")
        else :
            logger.info("Marking {:d} as unread".format(int(email_id)))
            imap_server.store(int(email_id), '-FLAGS', '\SEEN')

        if int(email_id) > end :
            end = int(email_id)

    # Make an entry only if there was something to be checked.
    if end > start :

        query = """
                INSERT INTO email_verification_logs (verified_till, time)
                VALUES ({:d}, NOW())
                """.format(int(end))

        dbutils.db_insert(db_conn, query)


if __name__ == '__main__' :
    main()

# Local Variables:
# mode: python
# tab-width: 8
# python-indent-offset: 4
# indent-tabs-mode: t
# End:
# ex: shiftwidth=4 tabstop=8
