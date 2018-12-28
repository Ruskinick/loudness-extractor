from audio import record, analyze, terminate
from audio import BUFFER_SIZE

print("-_-_- Audio Loudness Extraction -_-_-")

# Record audio and 
def rec(i=float('inf'), text_output=False, filename=""):
    iteration = 0
    while iteration < i:	
        record()
        loudness = str(int(analyze()))
        print("Loudness measure: " + loudness)
        if text_output:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(loudness)
        iteration += 1
    terminate()

# Ask for input number of trials and output filename if needed.
def run():
    
    i = input("(Leave blank for indefinite recording) How many trials? ")
    filename = input("(Leave blank for no output) Where should this value be written? ")

    try:
        i = int(i)
    except ValueError:
        print("Invalid integer input; proceeding with infinity.")
        i = float('inf')

    rec(i, True if (filename) else False, filename)
    
#def config():
#    from audio import

run()
# Test call
# rec(10, True, "last_loudness.txt")