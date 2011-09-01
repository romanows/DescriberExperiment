'''
Holds experiment objects for display code.

Created on Jun 23, 2011
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
from collections import defaultdict
from ExperimentObject import ExperimentObject

class ObjectManager:
    '''
    Container for ExperimentObjects.
    Supports retrieving sub-collections according to type, color, etc. 
    '''

    def __init__(self, objectImageDirname, imageWidth, imageHeight):
        '''
        Constructor.
        @param objectImageDirname: path to a directory containing object images of the form "type.color.png" 
        '''
        self.objects = []
        self.typeToObjects = defaultdict(list)
        self.colorToObjects = defaultdict(list)
        
        for fn in os.listdir(objectImageDirname):
            o = ExperimentObject(objectImageDirname, fn, imageWidth, imageHeight)
            self.objects.append(o)
            self.typeToObjects[o.type].append(o)
            self.colorToObjects[o.color].append(o)
            
            
    def byType(self, type):
        return self.typeToObjects[type]

    
    def byColor(self, color):
        return self.colorToObjects[color]
    
        
    def len(self):
        return len(self.objects)
        
        
    def __repr__(self):
        return self.objects.__repr__()