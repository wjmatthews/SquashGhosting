"""
This script is to test playing .wav files via python
"""

import pdb

def native_player():

    #runs and completes, but does not play audio. Did not explore much
    #it seems that the shell restarts much more quickly than the length
    #of the wav file, so assuming it is doing nothing.
    import os

    os.chdir('/home/pi/PythonFIles/SquashGhosting')
    file = '/home/pi/PythonFIles/SquashGhosting/test.wav'
    os.system('mpg123 ' + file)

def playsound_mod():

    #could not be made to work.
    #crashed system last two times it was run. can delete playsound.py
    import os
    from playsound import playsound

    os.chdir('/home/pi/PythonFIles/SquashGhosting')
    print('Prior to playing')
    playsound('test.wav')
    print('Playback complete')

def with_pyaudio():

    #getting error in a module I'm not familliar with
    #either need to get or update PortAudio.  Also possible it has not been
    #updated to work with Python 3.7
    import pyaudio
    import wave

    #filename = '/home/pi/PythonFIles/SquashGhosting/test.wav'
    filename = '/usr/share//sounds/alsa/Front_Center.wav'
    
    chunk = 1024

    wf = wave.open(filename, 'rb')

    p = pyaudio.PyAudio()

    #tester code to determine device info
    for i in range(p.get_device_count()):
        print(p.get_device_info_by_index(i))
    print(f'frequency from file: {wf.getframerate()}')
 
    stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate = wf.getframerate(),
                    output = True
                    )
    data = wf.readframes(chunk)
    #pdb.set_trace()
    while data != '':
        print(f'loop with data: {data}')
        stream.write(data)
        data = wf.readframes(chunk)
    print('before stream stop')
    stream.stop_stream()
    stream.close()
    p.terminate()

def with_simpleaudio():

    import simpleaudio as sa
    filename = '/home/pi/PythonFIles/SquashGhosting/Sounds/middle_right.wav'
    wav_obj = sa.WaveObject.from_wave_file(filename)
    play_obj = wav_obj.play()
    play_obj.wait_done()


#native_player()
#playsound_mod()
#with_pyaudio()
with_simpleaudio()
