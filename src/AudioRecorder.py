'''
Standalone audio recording program, requires PortAudio.  

This will record for RECORD_SECONDS seconds and then automatically stop 
recording.  Otherwise, press Ctrl-C to quit cleanly.

Created on Jun 28, 2011
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
import os, math, sys, signal
import pyaudio, wave
from datetime import datetime


chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 30 * 60
WAVE_OUTPUT_FILENAME = "pyAudioRecorder"


if __name__ == '__main__':

    p = pyaudio.PyAudio()
    
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')
    wavFilename = "%s.%s.wav" % (WAVE_OUTPUT_FILENAME,timestamp) 
    if os.path.lexists(wavFilename):
        raise Exception('Error: audio recorder output file already exists')

    wf = wave.open(wavFilename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    
    stream = p.open(format = FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    input = True,
                    frames_per_buffer = chunk)
    
    print "AudioRecorder is recording:", (wavFilename)
    print "Press Ctrl-C to quit (this won't work from within Eclipse!)"
    
    def cleanup():
        stream.close()
        wf.close()
        p.terminate()
        print "AudioRecorder has stopped recording"
    
    def signal_handler(signal, frame):
        print "Shutdown signal caught"
        cleanup()
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)
    
    for i in xrange(0, int(math.ceil(RATE / chunk * RECORD_SECONDS))):
        data = stream.read(chunk)
        wf.writeframes(data)

    cleanup()        
    