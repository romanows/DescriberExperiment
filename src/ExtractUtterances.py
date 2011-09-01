'''
Given an audio recording and an experiment log recorded during a run of 
DescriberTask.py, this script will extract individual utterances and 
write them as audio files. 

Created on Jul 7, 2011
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
import wave
import math, os, sys, datetime
from EventLog import EventLog

def main(argv):
    if len(argv) != 3:
        print 'Usage: ExtractUtterances <path_to_WAVE_Filename> <path_to_logfile>'
        return
    
    # get user's utterance segmentation
#    wavFilename = 'pyAudioRecorder.2011-07-07_08-58-50-651998.wav'
#    logFilename = '../experimentData/2011-07-07_08-58-47-503245/deepsemasr.devel.2011-07-07_08-58-47-503439.log.txt'
    wavFilename = argv[1]    
    logFilename = argv[2]
    
    if not os.path.exists(wavFilename):
        print "Can't find audio file:",wavFilename
        return
    if not os.path.exists(logFilename):
        print "Can't find log file:",logFilename
        return
    
    logDirname = os.path.split(logFilename)[0]
    log = EventLog.parse(logFilename)
    
    def filterAudioEvents(dt,ts,mt,msg):
        if mt == 'AUDIO_RECORDING': return True
    def filterStartRecording(dt,ts,mt,msg):
        if mt == 'SCRIPT_STATE' and msg == 'started audio recording': return True
        
    audioEventLog = EventLog.filter(log, filterAudioEvents)
    startRecordingEvent = EventLog.filter(log, filterStartRecording)[0]
    startRecordingTime, startRecordingTimestamp = startRecordingEvent[:2]
        
    # load audio data
    wf = wave.open(wavFilename, 'r')
    if not(wf.getcompname() == 'NONE' or wf.getcompname() == 'not compressed'):
        raise Exception('unsupported WAV audio compression')  # need to use another wav-reading module?
    sampFreqHz = wf.getframerate()
    wavTime = startRecordingTime
    uttIdx = 0
    
    # cut at timestamps into "utt.wavTimestamp.uttIndex.wav"
    outDirname = os.path.join(logDirname,'uttAudio.%s' % (startRecordingTimestamp)) 
    os.mkdir(outDirname)
    i = 0
    while i < (len(audioEventLog) - 1):
        if audioEventLog[i][3] != 'False':
            print 'Warning: expected audio start event but not found'
            i += 1 
            continue
        j = i+1
        while j < len(audioEventLog):
            if audioEventLog[j][3] == 'True':
                endFound = True
                break
            print 'Warning: expected audio stop event but not found'
            j += 1
        if not endFound:
            print 'Error: start audio event with no corresponding stop audio event'
            break

        startTime = audioEventLog[i][0]
        stopTime = audioEventLog[j][0]
        i = j + 1
        
        # skip ahead in wav file to start
        timeToStart = startTime - wavTime 
        samplesToStart = int(math.floor(timeToStart.total_seconds() * sampFreqHz))
        wf.readframes(samplesToStart)
        wavTime += datetime.timedelta(seconds=(samplesToStart / sampFreqHz))
        
        # read in/write out activated audio
        audioDuration = stopTime - startTime
        audioDurationSamples = int(math.ceil(audioDuration.total_seconds() * sampFreqHz))
        wavOutFilename = os.path.join(outDirname,'utt.%s.%d.wav' % (startRecordingTimestamp, uttIdx))
        print 'writing the %d seconds of utterance %d as: %s' % (audioDuration.total_seconds(), uttIdx, wavOutFilename)
        wfout = wave.open(wavOutFilename, 'w')
        wfout.setparams(wf.getparams())
        wfout.writeframes(wf.readframes(audioDurationSamples))
        wfout.close()
        wavTime += datetime.timedelta(seconds=(audioDurationSamples / sampFreqHz))
        uttIdx += 1
        
    wf.close()
    

if __name__ == '__main__':
    main(sys.argv)