# Overview
This code presents a series of images to a human subject and records audio 
of the description uttered by the subject.  Emphasis is placed on maintaining a
detailed record of experiment events.  

Images look like this:
![Image presented to the experimental subject; grid layout of different types and colors of hand-drawn objects](http://github.com/romanows/DescriberExperiment/raw/master/exampleDescriberImage.png)


Brian Romanowski 
romanows@gmail.com


# Requirements
DescriberTask is known to run with these Ubuntu 11.04 packages installed:

* Python 2.7.1
* PyGame 1.9.1
* PyAudio 0.2.4-2 (using PortAudio 19+svn20110317-1)
* Eclipse Indigo and PyDev 2.1.0 (not required, just what I used)

There should be no major difficulties to getting it running on another platform
such as Windows or Mac, but there are almost certainly a trivial bugs that 
would need to be fixed.


# Usage
DescriberTask.py is the main script that runs the experiment.  It will attempt 
to read a configuration file at resources/config/ but if this isn't present, 
it will create and write a default version.  As the experiment progresses, 
logs of user actions and script states are maintained.  Screenshots of the 
scenes presented to the user are recorded, as is an uninterrupted microphone 
recording.

AudioRecorder.py is a standalone script that records audio data and writes it 
to disk.  It is automatically started and terminated by the DescriberTask.py, 
but feel free to use it stand-alone in other applications.  Note that it 
currently is set to stop recording after RECORD_SECONDS (currently 30 minutes).
Make sure to remove this or change the the value if you need to record more 
audio data in one session!

ExtractUtterances.py is a script that uses logged keypress data to split the 
continuous recording made by DescriberTask.py into individual timestamped 
WAVE utterance files. 


# Bugs
Please file bug reports and bug fixes in the GitHub issue tracker.  Feel free 
to shoot the author an email if you find this software useful, it would make 
his day.


# Known Bugs
"Escape" quits the experiment, but this is only registered after a new scene 
fades in and the yellow box appears. 

Utterances are delimited by pressing the space bar.  There is no effort made
to very accurately determine when the keypresses are made, so test to make sure 
this timing data is accurate enough if your hypothesis relies upon it.

Default paths for reading and writing files are ugly.  When run from Eclipse, 
the audio files are written in the src/ directory while the experiment logs, 
screenshots, and configuration are written in the experimentData/ directory.  
ExtractUtterances.py places the extracted utterances in the same directory as
the log file.

For some reason, I wrote my own logger rather than use Python's logging 
package.


# Thanks
The audio files were taken from the Ubuntu project. 


# LICENSE
This software is released under the Simplified BSD License, see LICENSE.TXT. 
