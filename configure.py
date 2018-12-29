import pyaudio
# Make and apply modifications to the default configuration stored in config.txt


def ask_for(prompt, input_type, default=None):
    response = input(prompt)
    if input_type == int:
        try:
            response = int(response)
        except ValueError:
            print("Invalid integer input; proceeding with prior value {0}.", "<to be implemented>")
            response = default
    if input_type == str:
        if response == '':
            return None
    return response

def modify_configuration():
    """ 
    Rewrites the Python statements in config.txt so that their execution results
    in the proper recording format.

    """
    buffer = ask_for("Enter a buffer size (samples): ", int)
    time = ask_for("Enter a file length (seconds): ", int)
    channels = ask_for("Enter number of channels (1 for mono, 2 for stereo): ", int)

    devices()
    src = ask_for("Enter the index of the recording source: ", int, 0)
    samplesize = ask_for("Enter a sample rate (44100, 44000, 96000...): ", int)
    filename = ask_for("Enter .txt filename of output: ", str)
    iterations = ask_for("Enter number of iterations: ", int, float('inf'))

    output = True if filename else False

    if filename[-4:] != ".txt":
        filename = filename + ".txt"

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
WAVE_OUTPUT_FILENAME = {6}\n\
ITERATIONS = {7}"\
.strip().format(buffer, time, channels, src, samplesize, output, filename, iterations \
))


def devices():
    """ 
    Display device indices for input configuration. 
    Note: p.get_device_info_by_index(...) returns a dictionary.

    """
    from audio import p
    print("Index: Name")
    for i in range(p.get_device_count()):
        print(str(p.get_device_info_by_index(i)['index']) + ": " + p.get_device_info_by_index(i)['name'])
    print()

def apply_configuration():
    config = open("config.txt", "r")
    
    i = 1
    for line in config:
        try:
            exec(line)
        except Exception:
            print("Line {0} of config.txt is unreadable. Using default values.".format(i))
        i += 1
    config.close


devices()