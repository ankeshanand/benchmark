<?php
#                     BenchmarkExtension.api.php
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
 
class ApiBenchmark extends ApiBase{
    
    protected $mUpload = null;

    protected $mParams;

    public function __construct( $main, $action ) {
        parent::__construct( $main, $action );
    }

    
    public function execute() {
         
        $this->mParams = $this->extractRequestParams();
        $request = $this->getMain()->getRequest();
        
        $filename = $this->mParams['filename'];
        $content = $this->mParams['content'];
        
        
        $config = parse_ini_file(dirname(__FILE__).'/config.ini', true); 
        
        $queueFolder = $config['locations']['queue'];
        $file = $queueFolder.'/'.$filename.'.'.md5($content);
        
        $return = "ERROR_OTHERS";
        
        if (file_exists($file))
            $return = "ERROR_FILE_ALREADY_EXISTS";
        else {
            $fileHandle = fopen($file, 'w');
            fwrite($fileHandle, $content);
            fclose($fileHandle);           
            $return = "FILE_HAS_BEEN_SUBMITTED";
        }
        
        
        $results = array('STATUS' => $return);
        
        $this->getResult()->setIndexedTagName($results, 'benchmark');
        $this->getResult()->addValue( array('benchmark', 'status'), 'STATUS', $return);
        
    }
     
    public function mustBePosted() {
        return true;
    }

    public function isWriteMode() {
        return true;
    }

    public function getAllowedParams() {
        return array(
            'filename' => array(
                ApiBase::PARAM_TYPE => 'string',
                ApiBase::PARAM_REQUIRED => true,
            ),
            'content' => array(
                ApiBase::PARAM_TYPE => 'string',
                ApiBase::PARAM_REQUIRED => true
            ),
            'comment' => array(
                ApiBase::PARAM_TYPE => 'string',
                ApiBase::PARAM_REQUIRED => false
            )
        );
    }
     
    public function getParamDescription() {
        return array(
            'filename' => 'the name of the file',
            'content' => 'File contents',
            'comment' => 'same as the description',
        );
    }
 
    public function getDescription() {
        return 'Used to have a custom fileupload';
    }

    public function needsToken() {
        return false;
    }
    
    public function getVersion() {
        return __CLASS__ . ': $Id$';
    }
}
?>