#                     benchmark_upload.py
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

import sys
import urllib
import urllib2

from ConfigParser import ConfigParser

def main() :

    if len(sys.argv) == 2 :
        filename = sys.argv[1]

        config = ConfigParser()
        config.read(['../project_config'])

        url = config.get("locations", "api_url")

        content = open(filename, 'r').read()
        filename_clean = filename.split('/')[-1]

        values = {'action' : 'benchmark',
                  'filename' : filename_clean,
                  'content' : content,
                  'format' : 'xml',
                  }

        data = urllib.urlencode(values)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        print response.read()


    else :
        print "Usage: python benchmark_upload.py <relative-path-to-file>"
        sys.exit(1)




if __name__ == '__main__':

    main()

# Local Variables:
# mode: python
# tab-width: 8
# python-indent-offset: 4
# indent-tabs-mode: t
# End:
# ex: shiftwidth=4 tabstop=8
