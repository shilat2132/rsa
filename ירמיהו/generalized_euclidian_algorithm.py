a = 1440;
b = 31;

r0=a; r1=b; 
s0=1; s1=0;
t0=0; t1=1;

rn=r1
sn=s1
tn=t1

rnm1 = r0; 
snm1 = s0;
tnm1 = t0;

def floor(a,b):
    q=0
    c = a-b
    while True :
        c=c-b    
        q=q+1
        if c<0:
            break
    return q

k=1;
while rn!=0:
    
    q = int((rnm1//rn))

    rnp1=rnm1 - q*rn
    snp1=snm1 - q*sn
    tnp1=tnm1 - q*tn
    
    print("שלב k=%d" % k)
    print("q%d=%d"%(k,q) )
    print("r%d=%d" % (k + 1,rnp1))
    print("s%d=%d" % (k + 1,snp1))
    print("t%d=%d\n\n" % (k + 1,tnp1))
    
    rnm1 = rn
    rn = rnp1 
    
    snm1 = sn 
    sn = snp1
    
    tnm1 = tn 
    tn =  tnp1 
    
    k = k + 1;
    
s=snm1
t=tnm1
d=rnm1

print("s=",s)
print("t=",t)
print("d=",d)

print(s*a+t*b==d)
    
    
