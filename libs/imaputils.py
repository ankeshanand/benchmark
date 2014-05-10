#                     imaputils.py
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
# This contains the utility functions needed to access the IMAP 
# server.

__author__ = 'Suryajith Chillara'
__license__ = 'Modified BSD licence'

import email
import imaplib

from ConfigParser import ConfigParser

def get_imapserv_conn():
    """
    Return the connection to an imap server and 
    choose the default mailbox as INBOX.
    """
    config = ConfigParser()
    config.read(['../config'])
    
    imap_server = imaplib.IMAP4_SSL(config.get("imap_credentials", "imap_server"),
                                    config.get("imap_credentials", "imap_port"))
    imap_server.login(config.get("imap_credentials", 'username'), 
                      config.get("imap_credentials", 'password'))

    imap_server.select('INBOX')
    
    return imap_server



def get_attachment(imap_server, email_id):
    """
    Get attachments and return as a dictionary.
    """
    
    attachments = {}
    msg, data = imap_server.fetch(email_id, "(RFC822)")
    # Convert the message
    email_body = email.message_from_string(data[0][1])
    
    # Walk through the sections of the code
    for section in email_body.walk() :
        if section.get_content_maintype() == 'multipart':
            continue
        if section.get('Content-Disposition') is None:
            continue
        
        # Get the filename of the attachment
        filename = section.get_filename()
        
        # Get the content of the attachment
        content = section.get_payload(decode=True)
        
        attachments[filename] = content
        
    
    return attachments

# Local Variables:
# mode: python
# tab-width: 8
# python-indent-offset: 4
# indent-tabs-mode: t
# End:
# ex: shiftwidth=4 tabstop=8