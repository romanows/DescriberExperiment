'''
Contains relevant information about the image of the object shown to participants.

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
import pygame

class ExperimentObject:
    '''
    Holds information relevant to the experiment image object shown to the participant.
    '''

    def __init__(self, dirname, filename, imageWidth, imageHeight):
        '''
        Constructor.
        @param dirname: path to the directory where the image file is located
        @param filename: image filename
        @param imageWidth: width to which image will be scaled
        @param imageHeight: height to which image will be scaled     
        '''
        self.dirname = dirname
        self.filename = filename
        self.type, self.color = filename.split('.')[0:2]
        self.image = pygame.image.load(dirname + "/" + filename)
        self.image = pygame.transform.scale(self.image, (int(imageWidth), int(imageHeight)))
        
    def __repr__(self):
        return '(%s,%s)' % (self.type, self.color)