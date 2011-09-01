'''
A specific kind of event log for the DescriberTask experiment. 

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
from EventLog import EventLog
import itertools

class ExperimentEventLog(EventLog):
    '''
    Extends EventLog with convenience functions.
    '''

    def __init__(self, filename):
        '''
        Constructor.
        '''
        EventLog.__init__(self, filename)
        self.__recordingToggle = itertools.cycle((False,True))
        
        
    def scriptState(self, msg):
        self.write('SCRIPT_STATE',msg)
        
        
    def image(self, msg):
        self.write('IMAGE',msg)


    def recordingToggle(self):
        self.write('AUDIO_RECORDING', self.__recordingToggle.next())
        
        
    def scene(self, objectGrid):
        self.write('IMAGE', ','.join([str(x) for x in objectGrid.elements if x is not None]))