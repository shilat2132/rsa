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