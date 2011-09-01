'''
Main script to run the Describe Task data collection.

Press 'a' to start audio recording, space to indicate the start of an 
utterance, space again to indicate the end of an utterance, and escape to quit
the script cleanly. 

Created on Apr 30, 2011
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
import pygame, sys, time, os
from ObjectManager import ObjectManager
from ObjectGrid import ObjectGrid
from pygame.locals import QUIT, KEYUP, K_ESCAPE, K_SPACE, K_a, NOFRAME, FULLSCREEN, BLEND_ADD
import ConfigParser
import subprocess
from ExperimentEventLog import ExperimentEventLog
import datetime

dataRootDir = '../experimentData/'
if not os.path.isdir(dataRootDir):
    os.mkdir(dataRootDir)
if not os.path.isdir(dataRootDir):
    raise Exception('ERROR: unable to use an experimental data root directory:',dataRootDir)

dataDir = os.path.join(dataRootDir,datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f'))
if os.path.isdir(dataDir):
    raise Exception('ERROR: experimental data directory already exists:',dataDir)
os.mkdir(dataDir)
if not os.path.isdir(dataDir):
    raise Exception('ERROR: unable to use an experimental data directory:',dataDir)

screenshotIdx = 0
dataScreenshotDir = os.path.join(dataDir,'screenshots')
if not os.path.isdir(dataScreenshotDir):
    os.mkdir(dataScreenshotDir)
    
log = ExperimentEventLog(os.path.join(dataDir,'deepsemasr.devel'))


# Multiple config filenames lets you specify a developer-specific configuration file and a generic configuration file; it'll use the first one it finds
WRITE_DEFAULT_CONFIG = True
WRITE_CONFIG_FILENAME = '../resources/config/defaultConfig.ini'
CONFIG_FILENAMES = ['../resources/config/config.ini', '../resources/config/defaultConfig.ini']

CONFIG_DIRS = 'ResourceDirectories'
CONFIG_SND = 'SoundFiles'
CONFIG_EXP = 'ExperimentParameters'
CONFIG_REC = 'MicrophoneRecording'

config = ConfigParser.ConfigParser()
if CONFIG_FILENAMES is not None and not WRITE_DEFAULT_CONFIG:
    for fn in CONFIG_FILENAMES:
        if os.path.exists(fn): 
            log.scriptState('CONFIG\tloading from ' + fn)
            config.read(fn)
            break
else:
    log.scriptState('CONFIG\tcreating default')
    
    config.add_section(CONFIG_DIRS)
    config.set(CONFIG_DIRS, 'imageDir', '../resources/objectImages/')
    config.set(CONFIG_DIRS, 'audioDir', '../resources/gameAudio/')
    
    config.add_section(CONFIG_SND)
    config.set(CONFIG_SND, 'recordOn', 'button-pressed.ogg')
    config.set(CONFIG_SND, 'recordOff', 'button-toggle-off.ogg')
    config.set(CONFIG_SND, 'recordStart', 'service-login.ogg')
    config.set(CONFIG_SND, 'quitWithSuccess', 'service-logout.ogg')
    config.set(CONFIG_SND, 'showSelectedObject', 'dialog-warning.ogg')
    
    config.add_section(CONFIG_EXP)
    config.set(CONFIG_EXP, 'fullscreen', 'False')
    config.set(CONFIG_EXP, 'numRows', '3')
    config.set(CONFIG_EXP, 'numCols', '3')
    
    CONFIG_REC = 'MicrophoneRecording'
    config.add_section(CONFIG_REC)
    config.set(CONFIG_REC, 'commandLineList', ['python','AudioRecorder.py'])

    if WRITE_CONFIG_FILENAME is not None:
        log.scriptState('CONFIG\twriting default: ' + WRITE_CONFIG_FILENAME)
        configFile = open(WRITE_CONFIG_FILENAME,'w')
        config.write(configFile)
        
# Always have a copy of the config used for a particular experiment
configCopyFilename = os.path.join(dataDir,'config.used.ini')
with open(configCopyFilename, 'w') as f: config.write(f)
log.scriptState('CONFIG\twriting copy used in this experiment: ' + configCopyFilename)

audioDir = config.get(CONFIG_DIRS, 'audioDir')
imageDir = config.get(CONFIG_DIRS, 'imageDir')


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


pygame.init()
pygame.display.set_caption('Experiment')


pygame.mixer.init()
sndRecordOn = pygame.mixer.Sound(os.path.join(audioDir, config.get(CONFIG_SND, 'recordOn')))
sndRecordOff = pygame.mixer.Sound(os.path.join(audioDir, config.get(CONFIG_SND, 'recordOff')))
sndStart = pygame.mixer.Sound(os.path.join(audioDir, config.get(CONFIG_SND, 'recordStart')))
sndStop = pygame.mixer.Sound(os.path.join(audioDir, config.get(CONFIG_SND, 'quitWithSuccess')))
sndHighlight = pygame.mixer.Sound(os.path.join(audioDir, config.get(CONFIG_SND, 'showSelectedObject')))


if 'True' == config.get(CONFIG_EXP, 'fullscreen'):
    windowSurface = pygame.display.set_mode((0,0),NOFRAME | FULLSCREEN)  # defaults to fullscreen
else:
    windowSurface = pygame.display.set_mode((0,0),NOFRAME)  # non-fullscreen good for debugging purposes
    
windowSurface.fill(WHITE)

grid = ObjectGrid(windowSurface, int(config.get(CONFIG_EXP, 'numRows')), int(config.get(CONFIG_EXP, 'numCols')), jitterFactor = 0.5, avgNumMissing = 2)
objectManager = ObjectManager(imageDir, grid.imageWidth, grid.imageHeight)
grid.populate(objectManager.objects)
    
# draw the window onto the screen
pygame.display.update()
log.image('new objects displayed')
log.scene(grid)
time.sleep(0.5)
highlightGridElement = grid.highlight()
#sndHighlight.play()
pygame.display.update()
log.image('selected object indicated: ' + str(highlightGridElement))

screenshotFilename = os.path.join(dataScreenshotDir, 'screenshot.' + str(screenshotIdx) + '.png')
pygame.image.save(windowSurface, screenshotFilename)
screenshotIdx += 1
log.scriptState('screenshot saved: ' + screenshotFilename)

audioRecorderProcess = None


# game loop; break on escape key
log.scriptState('entering main loop')
isSceneRecorded = False
while True:
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            log.scriptState('quitting')
            if audioRecorderProcess is not None and audioRecorderProcess.poll() is None:
                log.scriptState('stopping audioRecorder process') 
                audioRecorderProcess.send_signal(subprocess.signal.SIGINT) # will cause the AudioRecorder to close its streams
                audioRecorderProcess.wait()
                log.scriptState('audioRecorder process stopped')
            
            sndStop.play()
            while pygame.mixer.get_busy() > 0:
                time.sleep(.2)
                
            pygame.quit()
            log.scriptState('closed pygame')
            log.close()
            sys.exit()
        elif event.type == KEYUP and event.key == K_SPACE:
            if isSceneRecorded is False:
                log.scriptState('user indicated utterance start')
                log.recordingToggle()
                isSceneRecorded = True
                sndRecordOn.play()
                # Here we need to make annotation
                pygame.event.clear()
            else:
                # Generate new scene, select new object
                log.scriptState('user indicated utterance stop')
                log.recordingToggle()

                log.scriptState('generate new scene')
                isSceneRecorded = False 
                sndRecordOff.play()
                time.sleep(.5)

                # TODO: Use a proper alpha surface so you can fade out/fade in and have it look nicer
                fadeStep = 16
                for x in xrange(int(255/fadeStep)):
                    windowSurface.fill((fadeStep,fadeStep,fadeStep), None, BLEND_ADD)
                    pygame.display.update()
                windowSurface.fill(WHITE)
                pygame.display.update()
                time.sleep(1)            
            
                grid.populate(objectManager.objects)
                pygame.display.update()
                log.image('new objects displayed')
                log.scene(grid)
                time.sleep(0.5)
                highlightObjectPosition = grid.highlight()
#                sndHighlight.play()
                pygame.display.update()
                log.image('selected object indicated: ' + str(highlightGridElement))
                screenshotFilename = os.path.join(dataScreenshotDir, 'screenshot.' + str(screenshotIdx) + '.png')
                pygame.image.save(windowSurface, screenshotFilename)
                screenshotIdx += 1
                log.scriptState('screenshot saved: ' + screenshotFilename)
                pygame.event.clear()
        elif event.type == KEYUP and event.key == K_a: 
            audioRecorderProcess = subprocess.Popen(list(config.get(CONFIG_REC, 'commandLineList')))
            log.scriptState('started audio recording')
            sndStart.play()
            pygame.event.clear()