def ask_for(prompt, input_type, default=None):

    """ 
    Prompt the user for input with string PROMPT.
    Return user input converted to type INPUT_TYPE.
    If the provided string cannot be converted to INPUT_TYPE, return DEFAULT.

    >>> ask_for("Enter a filename: ", str)
    Enter a filename: config
    "config"

    # No input
    >>> ask_for("Enter a filename: ", str, "config")
    Enter a filename: 
    "config"

    # Invalid input for INPUT_TYPE = int
    BUFFER_SIZE = 1024
    
    >>> ask_for("Enter a buffer size: ", int, BUFFER_SIZE)
    Enter a buffer size: 10k
    Invalid integer input; proceeding with prior value 1024.

    """

    response = input(prompt)
    if input_type == int:
        try:
            response = int(response)
        except ValueError:
            print("Invalid integer input; proceeding with prior value {0}.".format(default))
            response = default
    elif input_type == str:
        if response == '':
            response = default
    elif input_type == float:
        try:
            float(response)
        except ValueError:
            print("Invalid float input; proceeding with prior value {0}.".format(default))
            response = default

    return response

def add_suffix(string, suffix):
    """ 
    Add SUFFIX to the end of a filename STRING if it is not already present. 
    
    >>> add_suffix("last_loudness", ".txt")
        "last_loudness.txt"
    >>> add_suffix("audio.wav", ".wav")
        "audio.wav"

    """

    if string[(0 - len(suffix)):] != suffix:
        string = string + suffix
    return string

def between(input, low, high):
    """ Check that an int is between some minimum and maximum value. """
    if input >= low and input <= high:
        return input
    else:
        if abs(input - low) > abs(input - high):
            return high
        else:
            return low