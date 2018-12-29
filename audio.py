import wave
import pyaudio
import struct

p = pyaudio.PyAudio()

""" 
First, record a Wave audio file from SOURCE of LENGTH seconds.
Then, analyze the waveform of the file for its amplitude.

Returns the average amplitude of the audio in SOURCE.


### If ACCURATE (default False) is True, begin recording the next sequence before analysis.

Thanks to Hubert Pham and other contributors behind PyAudio for their Python-compatible recording tool.

"""

BUFFER_SIZE = 1024
RECORD_SECONDS = 4
FORMAT = pyaudio.paInt16
CHANNELS = 1
SOURCE = 1                                              # Index of MME audio source defined in p.get_device_info_by_index(i)
RATE = 44100
WAVE_OUTPUT_FILENAME = "output.wav"



def record():
    stream = p.open(format=FORMAT,\
                input_device_index=SOURCE,\
                channels=CHANNELS,\
                rate=RATE,\
                input=True,\
                frames_per_buffer=BUFFER_SIZE)

    print("Recording new file with {0} channel(s) at {1} Hz.".format(CHANNELS, RATE))

    frames = []

    for i in range(0, int(RATE / BUFFER_SIZE * RECORD_SECONDS)):
        data = stream.read(BUFFER_SIZE)
        #print(len(data))
        frames.append(data)
        #print(len(frames))

    print("Recording complete.")

    stream.stop_stream()
    stream.close()
    #p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()




def analyze():
    FRAMES = RATE * RECORD_SECONDS
    aud = wave.open(WAVE_OUTPUT_FILENAME)
    byte = aud.readframes(FRAMES)
    amplitudes = struct.unpack(str(len(byte)) + 'B', byte)

    total, i = 0, 512
    while i < len(amplitudes):
        total += amplitudes[i] * amplitudes[i+1]
        i += 2
    return max(0, 29000 - total/FRAMES)

def terminate():
    p.terminate()