from audio import record, analyze, terminate
from audio import BUFFER_SIZE
from configure import modify_configuration, apply_configuration, devices

print("-_-_- Audio Loudness Extraction -_-_-")

# Record audio and 
def rec(i, text_output, filename=""):
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
    
    print("\
            R: Run with selected settings\n\
            C: Configure")
    choice = input("Choose an option: ")

    if choice.upper() == 'R':
        apply_configuration()
        rec(iterations, output, filename)
    elif choice.upper() == 'C':
        config()

    #i = input("(Leave blank for indefinite recording) How many trials? ")
    #filename = input("(Leave blank for no output) Where should this value be written? ")



    rec(i, True if (filename) else False, filename)
    
def config():

    print("\
            M: Modify and apply new settings\n\
            D: Display all input devices\n\
            <: Return")
    choice = input("Choose an option: ")

    if choice.upper() == 'M':
        modify_configuration()
        #apply_configuration()
    elif choice.upper() == 'D':
        devices()
    elif choice == '<':
        pass
    run()

run()
# Test call
# rec(10, True, "last_loudness.txt")