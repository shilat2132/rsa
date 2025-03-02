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
    numberTape = t[start+1:end+1] if is_negative else t[start:end+1]

    binary = "".join(map(str, numberTape)) 
    decimal = int(binary, 2)

    return -decimal if is_negative else decimal