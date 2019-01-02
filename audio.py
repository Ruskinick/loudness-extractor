try:
    import pyaudio
except Exception:
    print("PyAudio is not installed.")

import wave
import struct
from configure import apply_configuration,\
BUFFER_SIZE, RECORD_SECONDS, FORMAT, CHANNELS, SOURCE, RATE, WAVE_OUTPUT_FILENAME 
# Prevent errors with default values ready

# Thanks to Hubert Pham and other contributors behind PyAudio for their Python-compatible recording tool.
p = pyaudio.PyAudio()

config_values = apply_configuration()
BUFFER_SIZE = config_values[0]
RECORD_SECONDS = config_values[1]
FORMAT = config_values[2]
CHANNELS = config_values[3]
SOURCE = config_values[4]
RATE = config_values[5]
WAVE_OUTPUT_FILENAME = config_values[8]

#def calibrate():
#    print("Taking short measurement of quiet input.")

def record():

    """
    Record RECORD_SECONDS of .wav audio with CHANNELS channels and RATE Hz sample rate from device index SOURCE.
    Process microphone/device input in chunks of BUFFER_SIZE.
    Save the recorded audio as WAVE_OUTPUT_FILENAME. Return nothing.

    A list of input devices and their corresponding PyAudio indices can be displayed with devices().

    """

    stream = p.open(format=FORMAT,\
                input_device_index=SOURCE,\
                channels=CHANNELS,\
                rate=RATE,\
                input=True,\
                frames_per_buffer=BUFFER_SIZE)

    print("Recording new file with {0} channel(s) at {1} Hz.".format(CHANNELS, RATE))

    frames = []

    for _ in range(0, int(RATE / BUFFER_SIZE * RECORD_SECONDS)):
        data = stream.read(BUFFER_SIZE)
        frames.append(data)

    print("Recording complete.")

    stream.stop_stream()
    stream.close()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    frames = []
    wf.close()


def analyze():

    """
    Analyze the recorded audio, decoding the bytes into numbers
    and returning a float representing some measure of amplitude per frame.

    """

    FRAMES = RATE * RECORD_SECONDS
    aud = wave.open(WAVE_OUTPUT_FILENAME)
    byte = aud.readframes(FRAMES)
    amplitudes = struct.unpack(str(len(byte)) + 'B', byte)

    # Skip static information stored in file header by skipping
    total, file_index = 0, 512
    while file_index < len(amplitudes):
        total += amplitudes[file_index] * amplitudes[file_index+1]
        file_index += 2
    return total/FRAMES
    #return max(0, 30500 - total/FRAMES)

def terminate():
    p.terminate()