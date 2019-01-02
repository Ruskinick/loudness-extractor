import pyaudio
from utils import ask_for, add_suffix, between
p = pyaudio.PyAudio()
# Make and apply modifications to the default configuration stored in config.txt

def modify_configuration():
    """ 
    Rewrites the Python statements in config.txt so that their execution results
    in the proper recording format.

    """
    buffer = ask_for("Enter a buffer size (samples): ", int, BUFFER_SIZE)
    time = ask_for("Enter a file length (seconds): ", float, RECORD_SECONDS)
    channels = ask_for("Enter number of channels (1 for mono, 2 for stereo): ", int, CHANNELS)

    devices()
    src = between(ask_for("Enter the index of the recording source: ", int, SOURCE), 0, p.get_device_count() - 1)
    samplesize = ask_for("Enter a sample rate (44100, 48000, 96000...): ", int, RATE)

    # Quote nesting to prevent Python from directly evaluating the response to the prompt.
    wav_filename = '"{0}"'.format(add_suffix(ask_for("Enter .wav filename of output: ", str), ".wav"))
    print("Audio output will be saved to " + wav_filename)

    txt_filename = '"{0}"'.format(add_suffix(ask_for("Enter .txt filename of output: ", str), ".txt"))
    print("Text output will be saved to " + txt_filename)

    iterations = between(ask_for("Enter number of iterations (leave blank for infinity): ", int, 2147483647), 1, 2147483647)

    output = True if txt_filename else False

    config = open("config.txt", "w")
    config.write(\
"\
BUFFER_SIZE = {0}\n\
RECORD_SECONDS = {1}\n\
FORMAT = pyaudio.paInt16\n\
CHANNELS = {2}\n\
SOURCE = {3}\n\
RATE = {4}\n\
OUTPUT = {5}\n\
TXT_OUTPUT_FILENAME = {6}\n\
WAVE_OUTPUT_FILENAME = {7}\n\
ITERATIONS = {8}"\
.strip().format(buffer, time, channels, src, samplesize, output, txt_filename, wav_filename, iterations \
))

def devices():
    """ 
    Display device indices for input configuration. 
    Note: p.get_device_info_by_index(...) returns a dictionary.

    """
    print("Index: Name")
    for i in range(p.get_device_count()):
        print(str(p.get_device_info_by_index(i)['index']) + ": " + p.get_device_info_by_index(i)['name'])
    print()

def apply_configuration():
    """ 
    Open and execute each line in config.txt if it is parseable.
    Otherwise, use the previous (or default) value.
    Returns a list containing the values of each variable in config.txt.

    """

    config = open("config.txt", "r")
    
    options = []
    i = 1
    for line in config:
        try:
            exec(line)
        except Exception:
            print("Line {0} of config.txt is unreadable. Using default values.".format(i))
        options.append(eval(line.split(' ', 1)[0]))
        i += 1
    config.close
    return options


# Default "safe" setup automatically loaded in before applying a configuration.
BUFFER_SIZE = 1024
RECORD_SECONDS = 4
FORMAT = pyaudio.paInt16
CHANNELS = 1
SOURCE = 1
RATE = 44100
OUTPUT = False
TXT_OUTPUT_FILENAME = "last_loudness.txt"
WAVE_OUTPUT_FILENAME = "output.wav"
ITERATIONS = float('inf')

# Try block errors when no configuration file is detected, and the program starts by setting up config.txt
try:
    run_options = apply_configuration()

    BUFFER_SIZE = run_options[0]
    RECORD_SECONDS = run_options[1]
    FORMAT = run_options[2]
    CHANNELS = run_options[3]
    SOURCE = run_options[4]
    RATE = run_options[5]
    OUTPUT = run_options[6]
    TXT_OUTPUT_FILENAME = run_options[7]
    WAVE_OUTPUT_FILENAME = run_options[8]
    ITERATIONS = run_options[9]
except FileNotFoundError:
    print("First time setup detected. Let's start by setting up a configuration file.")
    open("config.txt", "a")
    modify_configuration()