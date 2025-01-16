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

def unaryToDecimal(t) -> int:
    """
    gets a tape from a machine with a number in unary base and returns the decimal number.
    """
    
    if '0' in t: return 0
    num = t.count('1')
    i = getHeadIndex(t)
    if t[i] == "-":
        num = -1*num
    return num