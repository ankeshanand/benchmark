#                     parser.py
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
# This is a modular code for the benchmark log processing.
# Each pattern of the class Parser has a different method here. 
# 


__author__ = 'Suryajith Chillara'
__license__ = 'Modified BSD licence'


import re
import sys

import util
import dbutils 
from bp_logger import bp_logger

class Parser:
    """
    Parser class
    """
    
    filename = ""
    content = ""
    
    def __init__(self, filename):
        """
        Initialization
        """
        self.filename = filename
        self.content = open(filename, 'r').read().split('\n')
        self.connection = dbutils.get_connection()
        self.md5sum_file = util.md5_for_file(open(self.filename, 'r'))
        self.logger = bp_logger('Log Parser')
        
    def run(self):
        """
        The method that gets the actual writing to db done.
        """
        if self.check_if_file_exists_in_db() :
            self.logger.error("File {:s} already exists in the db.".format(self.filename.split('/')[-1]))
        else :
            self.write_to_db()
            # self.archive_file()
            self.logger.info("Success: Done writing {:s} to db.".format(self.filename.split('/')[-1]))
    
    
    def check_if_file_exists_in_db(self):
        """
        Check if the file exists in the database.
        """
        try :
            md5sum =  util.md5_for_file(open(self.filename, 'r'))
        except IOError:
            self.logger.error("File {:s} does not exist.".format(self.filename))
            print "Error: File {:s} does not exist.".format(self.filename)
            print "Usage: python parser.py <relative-path-to-file>"
            sys.exit(1)
        
        exists = dbutils.check_if_file_exists_in_db(self.connection, md5sum)
        
        if exists > 0 :
            self.logger.error("Error: The file already exists in the database.")
            return True
        
        return False
    
        
    def get_machine_desc(self):
        """
        Returns the machine description
        """
        line_counter = 0
        
        for line in self.content :
            line_counter += 1
            
            # Machine description
            if line_counter == 5 :
                return line
        self.logger.debug("Machine description not found.")
    
    
    def get_raytracing_results(self):
        """
        Get the results for each of the tests and report them
        cumulatively as a dictionary.
        """
        result_regex = "[A-Za-z0-9]*.pix: [A-Za-z\s]*"
        raytracing_results = {}
        
        for line in self.content :
            
            if not re.search(result_regex, line) == None :
                result = re.search(result_regex, line).group()
                test_result = ""
                
                # Finding individial results and putting them in a dictionary
                if not re.search("RIGHT", line) == None:
                    test_result = "RIGHT"
                
                if not re.search("WRONG", line) == None:
                    test_result = "WRONG"
                
                if not re.search("BENCHMARK COMPARISION FAILURE", line) == None:
                    test_result = "COMPARISION_FAILURE"
                    
                test_name = result.split(' ')[0].split('.')[0]
                
                raytracing_results[test_name] = test_result
                
        return raytracing_results
    
    def get_rays_per_sec(self, type = 'abs'):
        """
        Get the rays shot per second for each of the reference images.
        """
        
        tests_order = {'moss' : 0, 'world' : 1, 'star' : 2, 'bldg391' : 3, 'm35' : 4, 'sphflake' : 5, 'average' : 6}
        
        if type == 'abs' :
            regex = "^Abs\s+[A-Za-z]+\s+([0-9]+\.*[0-9]*\s+){6}"
        elif type == 'vgr' :
            regex = "^\*vgr\s+[A-Za-z]+\s+([0-9]+\.*[0-9]*\s+){6}"
            
        accumulator = {}
        
        for line in self.content :
            if not re.search(regex, line, re.I) == None :
                results = re.findall("[0-9]+\.*[0-9]*\s", line, re.I)
                for test, order in tests_order.items() :
                    accumulator[test] = float(results[order])

        print accumulator
        return accumulator
                
        
    def get_abs_rays_per_sec(self):
        """
        Get the absolute rays shot per second for each of the reference images 
        """
        return self.get_rays_per_sec('abs')
    
    def get_vgr_rays_per_sec(self):
        """
        Get the rays shot per second for each of the reference images in *vgr
        """
        return self.get_rays_per_sec('vgr')
    
    def get_approx_vgr(self):
        """
        Get the approximate VGR of the run and the machine.
        """
        for line in self.content :
            
            if not re.search("approximate VGR", line) == None :
                approx_vgr = int(re.search("[0-9]+", line).group())
                return approx_vgr
        
        return 0
    
    
    def get_log_vgr(self):
        """
        Get the logarithmic VGR of the run and the machine.
        """
        for line in self.content :
            
            if not re.search("logarithmic VGR", line, re.I) == None :
                
                log_vgr = float(re.findall("[0-9]+\.*[0-9]*", line)[0])
                return log_vgr
        
        return 0.0
    
    
    def get_params(self):
        """
        Return the parameters of the run as a dictionary.
        """
        params = {}
        for line in self.content :
            if not re.search("TIMEFRAME", line) == None :
                params['timeframe'] = re.search("[0-9]+", line).group()
                
            if not re.search("MAXTIME", line) == None :
                params['maxtime'] = re.search("[0-9]+", line).group()
                
            if not re.search("DEVIATION", line) == None :
                params['deviation'] = re.search("[0-9]+", line).group()
            
            if not re.search("AVERAGE", line) == None :
                params['average'] = re.search("[0-9]+", line) .group()
                
        return params
    
    
    def get_brlcad_version(self):
        """
        Check if the version numbers are right. If yes use the correct version.
        Otherwise just return some arbitrary version amongst those.
        """
        return self.verify_version(True)
        
    
    
    def verify_version(self, get = False):
        """
        Check if there is any discrepancy with respect to version numbers
        in the RT reports. If there is a version mismatch report False.
        Else, report the version number.
        If get is set to True, send an arbitrary version number.
        """
        from sets import Set
        versions = Set([])
        
        for line in self.content :
            if not re.search("Release", line) == None :
                versions.add(re.search("[0-9]+\.[0-9]+\.[0-9]+", line).group())
                
        if len(versions) == 1 or get:
            
            return versions.pop()
        else :
            self.logger.error("Mismatch in the version numbers.")
            return False
    
          
    def get_time_of_execution(self):
        """
        Get the time of execution and return it in TIMESTAMP format for MySQL
        """
        time_regex = "[A-Z][a-z]{2} [A-Z][a-z]{2} [0-9]{2} [0-2][0-9]:[0-5][0-9]:[0-5][0-9] [A-Z]{3,4} [0-9]{4}"
        for line in self.content :
            if not re.search(time_regex, line) == None : 
                return util.time_conversion(re.search(time_regex, line).group())
    
    
    def get_running_time(self):
        """
        Get the total running time/time elapsed in seconds.
        """
        for line in self.content :
            
            if not re.search("time elapsed", line) == None :
                #Find the individual fields and typecast them
                times = map(int, re.findall("[0-9]+", line))
                
                if len(times) == 3 :
                    running_time = times[0]*3600 + times[1]*60 + times[2]
                elif len(times) == 2 :
                    running_time = times[0]*60 + times[1]
                elif len(times) == 1 :
                    running_time = times[0]
                else :
                    running_time = 0
                    
        return running_time
    
    
    def get_proc_count(self):
        """
        Get processor count. This can be different from the core count.
        """
        proc_count = 0
        proc_numbers = []   
        for line in self.content :         
            if not re.search("processor\s+:\s*[0-9]+", line) == None :
                proc_number = re.search("[0-9]+", line).group()
                if proc_number in proc_numbers :
                    self.logger.error("Error: duplicate processor numbers")
                else :
                    proc_count += 1
                    proc_numbers.append(proc_number)
        
        return proc_count
    
    def get_cores(self):
        """
        Get the number of cores on the machine.
        """
        for line in self.content :         
            if not re.search("cores\s+:\s*[0-9]+", line) == None :
                return int(re.search("[0-9]+", line).group())
    
    def get_vendor_id(self):
        """
        Get the vendor ID for the processor.
        """
        for line in self.content :         
            if not re.search("vendor_id\s+:\s*[A-Za-z]+", line) == None :
                return (re.search(":\s*[A-Za-z]+", line).group())[1:].strip()
            
            
    
    def get_address_sizes(self):
        """
        The first element in the list gives the 
        physical address size and second virtual.
        """
        sizes = [0, 0]
        for line in self.content :         
            if not re.search("address sizes\s+:", line) == None :
                sizes = map(int, re.findall("[0-9]+", line))
        
        return sizes
    
    
    def get_cpu_mhz(self):
        """
        Get the CPU frequency at which the machine is being run.
        """ 
        for line in self.content :         
            if not re.search("cpu MHz\s+:\s*[0-9]+", line, re.I) == None :
                return float(re.search("[0-9]+\.*[0-9]*", line).group())
        
        return 0
    
    
    def get_model_name(self):
        """
        Get the model name of the processor.
        """
        for line in self.content :         
            if not re.search("model name\s+:\s*\S+", line, re.I) == None :
                return line.split(':')[1].strip()
        
        return ''
    
    
    def get_kernel_param(self, word):
        """
        A common method to get Kernel parameters
        """
        for line in self.content :         
            if not re.search("kernel.{}".format(word), line, re.I) == None :
                ostype = re.search("=\s*\S+", line).group()
                return re.sub("=", "", ostype).strip()
            
        return ''
    
    
    def get_hostname(self):
        """
        use get_kernel_param for this
        """
        return self.get_kernel_param('hostname')
    
    
    
    def get_osrelease(self):
        """
        use get_kernel_param for this
        """    
        return self.get_kernel_param('osrelease')
    
    
    
    def get_ostype(self):
        """
        Get ostype from kernel.ostype. Else return empty string
        """
        return self.get_kernel_param('ostype')
    
    
    
    def archive_file(self):
        """
        Move the file to the specified archive spot
        """
        util.archive_file(self.filename)
        
        
        
    def write_individual_results(self, benchmark_id):
        """
        """
        tests = ['moss', 'world', 'star', 'bldg391', 'm35', 'sphflake', 'average']
        
        abs = self.get_abs_rays_per_sec()
        vgr = self.get_vgr_rays_per_sec()
        res = self.get_raytracing_results()
        
        for test in tests :
            if test == 'average' :
                result = 'NULL'
            else :
                result = res[test]
                
            query = """
                    INSERT INTO `rt_{:s}` (benchmark_id, abs_rps, vgr_rps, result)
                    VALUES
                    ({:d}, {:f}, {:f}, \"{:s}\")
                    """.format(test, int(benchmark_id), float(abs[test]), float(vgr[test]), result)
            
            id = dbutils.db_insert(self.connection, query)
            if id == None :
                self.logger.error("Error: Insertion into the rt_{:s} table might not have taken place. \n Query : {:s}".format(test, query))
                
            
                   
    def write_to_db(self):
        """
        Write the parsed content to the db.  
        """  
        # Benchmark logs query
        bl_query = """
                    INSERT INTO benchmark_logs (machine_desc, brlcad_version,
                    running_time, time_of_execution, approx_vgr, log_vgr, params,
                    results, complete_info) VALUES 
                    (\"{:s}\", \"{:s}\", {:d}, \"{:s}\", {:d}, {:f}, \"{:s}\", \"{:s}\", \"{:s}\")
                    """.format(self.get_machine_desc(), self.get_brlcad_version(), 
                               self.get_running_time(), self.get_time_of_execution(), 
                               self.get_approx_vgr(), self.get_log_vgr(), self.get_params(), 
                               self.get_raytracing_results(), util.sanitize_file(self.content))
        
        benchmark_id = dbutils.db_insert(self.connection, bl_query)
    
        if benchmark_id == None :
            self.logger.error("Error: Benchmark insert might not have taken place")
            
        
        md5_query = """
                    INSERT INTO `md5_log` (benchmark_id, file_name, 
                    `md5sum`, archived, db_entries) VALUES
                    ({:d}, \"{:s}\", \"{:s}\", \"{:s}\", \"{:s}\")
                    """.format(benchmark_id, self.filename.strip().split('/')[-1], 
                               self.md5sum_file, 'YES', 'YES')
        
        log_id = dbutils.db_insert(self.connection, md5_query)
    
        if log_id == None :
            self.logger.error("Error: Log insert might not have taken place")
            
        
        hw_query = """
                    INSERT INTO `machine_info` (`benchmark_id`, `osrelease`,
                    `hostname`, `cores`, `processors`, `physical_addr_size`,
                    `virtual_addr_size`, `vendor_id`, `ostype`, `cpu_mhz`, `model_name`) 
                    VALUES
                    ({:d}, \"{:s}\", \"{:s}\", {:d}, {:d}, {:d}, {:d}, "{:s}\", \"{:s}\", {:f}, \"{:s}\")   
                    """.format(benchmark_id, self.get_osrelease(), self.get_hostname(),
                               self.get_cores(), self.get_proc_count(), self.get_address_sizes()[0],
                               self.get_address_sizes()[1], self.get_vendor_id(), self.get_ostype(),
                               self.get_cpu_mhz(), self.get_model_name())
        
                    
        hw_id = dbutils.db_insert(self.connection, hw_query)
        if hw_id == None :
            self.logger.error("Error: Insertion into the machine_info table might not have taken place")
        
        self.write_individual_results(benchmark_id)
            
        return benchmark_id

# Local Variables:
# mode: python
# tab-width: 8
# python-indent-offset: 4
# indent-tabs-mode: t
# End:
# ex: shiftwidth=4 tabstop=8
