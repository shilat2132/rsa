import itertools

def find_in_delta_table(delta_table, current_state, symbols):
    interchangeable = {'_', 0}

    # נסה התאמה מדויקת
    delta_input = (current_state,) + tuple(symbols)
    if delta_input in delta_table:
        return delta_table[delta_input]

    # נסה התאמות מבוססות שקילות
    indices_to_alternate = [i for i, s in enumerate(symbols) if s in interchangeable]

    for replacements in itertools.product(interchangeable, repeat=len(indices_to_alternate)):
        altered = list(symbols)
        for i, index in enumerate(indices_to_alternate):
            altered[index] = replacements[i]

        delta_input = (current_state,) + tuple(altered)
        if delta_input in delta_table:
            return delta_table[delta_input]

    raise KeyError(f"No match found in delta table for state {current_state} and symbols {symbols}")





def print_steps(steps, indent=0):
    for step in steps:
        if step.get("action") == "submachine" or step.get("action") == "main":  # Handle "submachine" separately
            print(" " * indent + "Submachine:")
            if step.get("formula"): print(" " * indent + f"formula: {step['formula']}")
            print(" " * indent + f"tapes: {step['tapes']}")
            print(" " * indent + "Steps:")
            # Recursively print the nested steps with increased indentation
            print_steps(step["steps"], indent + 4)

        else:
            # Print the current step with indentation
            print(" " * indent + str(step))




def getHeadIndex(tape: list)-> int:
    """
    given a tape (list), return the index of the first character that's different from "_".
        - if all characters are "_", returns 0 (the first index)
    """
    l = len(tape)
    head=0
    for i in range(l):
        if tape[i]!= "_": 
            head=i
            break
    return head

def decimalToBinaryList(num, minus = False):
    a = bin(num)[2:]
    a = list(a)
    a = [int(c) for c in a]
    if minus:
        a.insert(0, "-")
    
    return a



def getLastCharIndex(tape: list)-> int:
    """
    given a tape (list), return the index of the last character that's different from "_".
        - if all characters are "_", returns the last index
    """
    n = len(tape)-1
    k = n
    while k>=0:
        if tape[k]!= "_": return k
        k-=1
    return n

def binaryToDecimal(t) -> int:
    """
    gets a tape from a machine with a number in binary base and returns the decimal number.
    """
    
    start = getHeadIndex(t)
    end = getLastCharIndex(t)  

    is_negative = t[start] == "-"
    if t[start] == "_": return 0
    numberTape = t[start+1:end+1] if is_negative else t[start:end+1]

    binary = "".join(map(str, numberTape)) 
    decimal = int(binary, 2)

    return -decimal if is_negative else decimal



def isZero(tape: list):
    """
     given a tape of a machine, checks if the number appearing in it is zero
        returns: true if it is zero, false otherwise
    """

    for t in tape:
        if t == 1:
            return False
        
    return True

def tapeToBinaryString(tape: list) -> str:
    """
    Given a Turing tape (list) with elements '_', 0, and 1,
    returns the binary number as a string with '0b' prefix (e.g., '0b1011').
    Ignores '_' characters.
    """
    return '0b' + ''.join(str(x) for x in tape if x in (0, 1))


def is_prime(n):
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True



