class MagicInt(int):
    prime=property(get_prime,set_prime):
        _prime=None

    def __init__(self,i):
        self.prime=self.is_prime()

    def __add__(self,b):
        if isinstance(b,MagicInt):
            normal_sum=int.__add__(self,b)
            return MagicInt(int.__add__(normal_sum,1))
        else:
            return MagicInt(int.__add__(self,b))

    def __len__(x):
        return len(str(abs(x)))


    def get_prime(self):
        if(self._prime is None):
            isprime= (lambda n : all([n%x for x in range(2,n)]))
            self._prime=isprime(int(self))
        return(self._prime)

    def set_prime(self,val):
        self._prime=val

        




    
        
#Do not modify code below
two = MagicInt(2)
three = MagicInt(3)
m127 = MagicInt(127)

# a int
assert isinstance(two, int)

# 2 + 2 = 5
assert two + two == 5
assert two + three == 6
assert two + 3 == 5

#Result of addition is also a MInt object
assert isinstance(two + two, MagicInt)
assert isinstance(two + 3, MagicInt)

# len() return the number of digits
assert len(two)==1
assert len(m127) == 3
assert len(MagicInt(-127)) == 3

# property prime that returns True the if it is a prime
assert m127.prime
assert (two+m127).prime==False

# Allow the user to set the 'prime' property manually
m127.prime = False
assert m127.prime==False

print "Yeah!!! All asserts satisfied"

