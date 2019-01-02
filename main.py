from audio import record, analyze, terminate
from configure import modify_configuration, devices, apply_configuration

print("-_-_- Audio Loudness Extraction -_-_-")


def rec(i, text_output, filename=""):

    """
    Initiate the loop of recording and analyzing audio for I iterations.
    If TEXT_OUTPUT, an output file containing an integer, named FILENAME, is created.

    """
    
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


def run():

    """ Display menus to direct and the user in setup. """

    choice = ''
    while not choice:
        
        print("\
            R: Run with selected settings\n\
            C: Configure")
        choice = input("Choose an option: ")

        if choice.upper() == 'R':
            run_options = apply_configuration()
            ITERATIONS = run_options[9]
            OUTPUT = run_options[6]
            TXT_FILENAME = run_options[7]
            rec(ITERATIONS, OUTPUT, TXT_FILENAME)
        elif choice.upper() == 'C':
            config()
        else:
            print('Unrecognized choice ' + choice + ', try again.')
            choice = ''
            


    rec(ITERATIONS, True if (TXT_FILENAME) else False, TXT_FILENAME)


def config():

    choice = ''
    while not choice:
        print("\
            M: Modify and apply new settings\n\
            D: Display all input devices\n\
            <: Return")
        choice = input("Choose an option: ")

        if choice.upper() == 'M':
            modify_configuration()
        elif choice.upper() == 'D':
            devices()
        elif choice == '<':
            pass
        else:
            print('Unrecognized choice ' + choice + ', try again.')
            choice = ''
    run()

run()