'''
Object image onscreen layout using Pygame.

Created on Jun 24, 2011
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
from __future__ import division
import pygame
from random import Random


class GridElement:
    def __init__(self, rect, row, col):
        self.obj = None # experiment object
        self.rect = rect
        self.row = row
        self.col = col
        
        
    def __repr__(self):
        if self.obj is not None:
            # object filename, type, color, row, col, x, y
            s = '(%s,%s,%s,%d,%d,%d,%d)' % (self.obj.filename, self.obj.type, self.obj.color, self.row, self.col, self.rect.left, self.rect.top)
        else :
            s = '(,,,%d,%d,%d,%d)' % (self.row, self.col, self.rect.left, self.rect.top)
        return s
            

class ObjectGrid:
    '''
    Onscreen grid for object placement.
    Uses PyGame for drawing. 
    '''

    def __init__(self, windowSurface, numRows, numCols, jitterFactor = 1.0, avgNumMissing = 3, keepCenter = True, fontSize = 48, rnd = Random(42)):
        '''
        Constructor.
        @param windowSurface: pygame surface object
        @param numRows: number of rows in grid
        @param numCols: number of columns in grid
        @param jitterFactor: a number between 0 and 1.0 that is multiplied with a random jitter offset for row and column screen coordinates
        @param avgNumMissing: about how many grid elements should be empty (not containing objects)
        @param keepCenter: always keep the center object
        @param fontSize: font size of the labels used for the images
        @param rnd: a Random.random object     
        '''
        self.windowSurface = windowSurface
        self.numRows = numRows
        self.numCols = numCols
        self.size = numRows * numCols
        self.fontSize = fontSize
        self.fractionMissing = avgNumMissing / self.size
        self.keepCenter = keepCenter
        self.jitterFactor = jitterFactor
        
        self.rnd = rnd
        
        # Sprite size depends on how many we expect to fit on the screen, plus room for margin/padding.  They must be square.
        self.imageWidth = min(windowSurface.get_rect().width/(numCols+2), windowSurface.get_rect().height/(numRows+2))
        self.imageHeight = self.imageWidth
        
        # Distribute leftover space as padding between the sprites.  Note that there are N+1 padding "cells" for N images.
        self.paddingWidth = (self.windowSurface.get_rect().width - self.numCols * self.imageWidth) / (self.numCols+1)
        self.paddingHeight = (self.windowSurface.get_rect().height - self.numRows * (self.imageHeight + self.fontSize)) / (self.numRows+1)
        
        # a fractional number effectively indicates no center
        self.centerRow = (self.numRows - 1) / 2.0
        self.centerCol = (self.numCols - 1) / 2.0
        
        self.elements = [] # flat 1d container for grid elements
                
                
    def populate(self, experimentObjects):
        # Clear old rectangles and objects
        del(self.elements[:])

        # Create grid of rectangles to later receive images        
        for r,y in [(y*(self.paddingHeight + self.imageHeight + self.fontSize),y) for y in xrange(self.numRows)]:
            for c,x in [(x*(self.paddingWidth + self.imageWidth),x) for x in xrange(self.numCols)]:
                if self.rnd.random() < self.fractionMissing:
                    if not self.keepCenter or (self.keepCenter and not(y == self.centerRow and x == self.centerCol)):
                        self.elements.append(None)
                        continue
                colJitter = int(self.jitterFactor * self.rnd.uniform(-self.paddingWidth/2.0, self.paddingWidth/2.0))
                rowJitter = int(self.jitterFactor * self.rnd.uniform(-self.paddingHeight/2.0, self.paddingHeight/2.0))
                self.elements.append(GridElement(pygame.Rect(c + self.paddingWidth + colJitter, r + self.paddingHeight + rowJitter, self.imageWidth, self.imageHeight),y,x))                                

        # Copy and shuffle the objects to fill the grid
        objectDeck = []
        while len(objectDeck) < self.size:
            self.rnd.shuffle(experimentObjects)
            objectDeck.extend(experimentObjects)
        objectDeck = objectDeck[:self.size]

        labelFont = pygame.font.SysFont(None, self.fontSize)

        # draw the object images on the rectangles
        for e,o in zip(self.elements,objectDeck):
            if e is None:
                continue # skip empty grid elements
            
            r = e.rect
            self.windowSurface.blit(o.image,r)
            e.obj = o
            e.label = labelFont.render(o.type, True, (0, 0, 0), (255,255,255,0))
            lr = e.label.get_rect()
            lr.left, lr.top = r.left, r.bottom
            self.windowSurface.blit(e.label, lr)
            
            
    def get(self, row, col):
        return self.elements[row*self.numCols + col]
   
   
    def highlight(self):
        # pick a valid displayed object in the non-edge portion of the screen
        # TODO: FIXME: repeated random selections is ugly, and might never halt if center is empty, but let's not worry about that now
        while True:
            r,c = self.rnd.randint(1, self.numRows-2), self.rnd.randint(1, self.numCols-2)
            if self.get(r,c) is not None:
                break
        e = self.get(r,c)
        p = e.rect
        pygame.draw.rect(self.windowSurface, (0,0,0), (p.left, p.top, p.width, p.height), 12)
        pygame.draw.rect(self.windowSurface, (255,255,0), (p.left, p.top, p.width, p.height), 4)
        return e