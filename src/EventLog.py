'''
A lightweight logging-type class to record experiment events.

Created on Jun 29, 2011
@author: romanows



Copyright 2011 Brian Romanowski. All rights reserved.

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY BRIAN ROMANOWSKI ``AS IS'' AND ANY EXPRESS OR 
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF 
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO 
EVENT SHALL BRIAN ROMANOWSKI OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT 
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR 
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF 
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE 
OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF 
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those
of the authors.
'''

import os
from datetime import datetime

class EventLog:
    '''
    Lightweight logging class for simple experiment events.
    Format for logging is: "timestamp<TAB>messageType<TAB>message<NEWLINE>".
    Where the messageType and message are user-specified strings.
    "messageType" can not contain tab characters and neither "messageType" nor "message" can contain newline characters.
    '''

    @staticmethod
    def parse(filename):
        '''
        Parse a logfile into a list of tuples of the form: (datetimeObject, timestamp, msgtype, msg)
        @param filename: filename of the logfile to read
        @return: a list of parsed log tuples  
        '''
        log = []
        f = open(filename,'r')
        for x in f:
            if x == '':
                continue
            timestamp,msgtype,msg = x.strip().split('\t',2)
            t = datetime.strptime(timestamp,'%Y-%m-%d_%H-%M-%S-%f')
            log.append(tuple([t,timestamp,msgtype,msg]))
        f.close()
        return log
    
    
    @staticmethod
    def filter(log, matcherFunction):
        '''
        Creates a new log list that contains only the log entries matched by the matcherFunction.
        @param log: log list
        @param matcherFunction: function whose input is (datetimeObject, timestamp, msgType, msg) and whose output is True if a log entry should be copied to the output list
        @return: a new log list with only entries where matcherFunction is True 
        '''
        newLog = []
        for x in log:
            if matcherFunction(*x):
                newLog.append(tuple(x))
        return newLog
         
        
    def __init__(self, filenamePrefix):
        '''
        Constructor.
        @param filenamePrefix: path and start of filename for logfile, e.g., "../logfiles/mylog.foobar' where 
            one will expect something like this log file to be created: 'mylog.foobar.2011-01-01_01-00-00-000000.txt'  
        '''
        self.startTime = self.__timestamp()
        self.filename = '%s.%s.log.txt' % (filenamePrefix, self.startTime)
        if os.path.lexists(self.filename):
            raise Exception('Error: event log output file %s already exists' % (self.filename))
 
        self.logFile = open(self.filename, 'w')
        self.write('EVENT_LOG','open')

        
    def __timestamp(self):
        return datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')

    
    def write(self, msgtype='', msg=''):
        if self.logFile.closed:
            print 'ERROR: attempting to write to a closed log file'
            return
        msgtype = str(msgtype)
        msg = str(msg)
        if msgtype.find('\t') >= 0 or msgtype.find('\n') >= 0:
            print 'WARNING: msgtype contains a forbidden character, this will be removed for logging:',msgtype
            msgtype = msgtype.replace('\t','').replace('\n','')
            self.write('EVENT_LOG_WARNING', 'forbidden characters removed from msgtype: ' + msgtype)
        if msg.find('\n') >= 0:
            print 'WARNING: msg contains a forbidden character, this will be removed for logging:',msg
            msg = msg.replace('\n','')
            self.write('EVENT_LOG_WARNING', 'forbidden characters removed from msg: ' + msg)
        try:
            self.logFile.write('%s\t%s\t%s\n' % (self.__timestamp(), msgtype, msg))
            self.logFile.flush()
        except Exception as e:
            print 'ERROR: exception while writing event:', e


    def close(self):
        self.write('EVENT_LOG','close')
        self.logFile.close()