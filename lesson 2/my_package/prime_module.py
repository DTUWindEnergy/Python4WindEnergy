n = 100
primes = []
for p in range(3,n):
    for x in range(2,p):
        if p%x==0:
            break
    else:
        primes.append(p)
print primes