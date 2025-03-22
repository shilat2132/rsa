# regular function for encryption - no TM

def sq(x, b, n):
    """
    simulates the method of squares of x^b mod n
    """
    binary = bin(b)
    binary = binary[2:] #to remove the '0b' from the beginning
    k = len(binary) -1 #start from the right side of the binary number

    # the final result would be stored in y
    # if x%n is part of the sum of the 2^m elements
    if binary[k]=='1':
        y = x%n
    else:
        y=1
    k-=1
    
    if k>=0:
        m = x 


# while the characters in the binary number aren't over - keep calculating (x^2i) % n
    while k>=0:
        # m would store the current (x^2i) % n
        m = m**2
        m = m%n

        i = 2**(len(binary)-1-k)
        print(f"the result of x^{i}: {m} \n")
   
        # if the current element(x^2i) is part of the sum of the powers of 2, then compute the modular multiplication of it with the current y
        if binary[k]== '1':
            y = y*m
            y = y%n
        
        k-=1 #go to the character of the binary number on the left
    return y



y = sq(2468, 47, 24257)
# y = E(1228, 31, 1517)

print(str(y))