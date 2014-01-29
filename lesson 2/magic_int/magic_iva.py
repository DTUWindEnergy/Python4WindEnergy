"""
Exercise Magic number

Make a class MagicInt that satisfies the assert statements, i.e:
Is a int
Makes 2 + 2 = 5
Result of addition is also a MagicInt object
Lets len(magicInt) return the number of digits
Has a property prime that returns True the if it is a prime.
Allows the user to set the prime property manually
""" 

def is_prime(n):
    for i in range(3, n):
        if n % i == 0:
            return False
    return True  


class MagicInt(int):
    broj = 0
    _prime = None
	
    @property
    def prime(self):
        if self._prime == None:
            self._prime = is_prime(self.broj)
        return self._prime
		
    @prime.setter
    def prime(self, value):
        self._prime = value
	
    def __init__(self, value):
        self.broj = value
        
    def __add__(self, other):
        if self.broj == 2 and other == 2:
            return MagicInt(5)
        return MagicInt(self.broj + other)
        
    def __len__(self):
        return len(str(abs(self.broj)))


#Do not modify code below
two = MagicInt(2)
m9 = MagicInt(9)
m127 = MagicInt(127)

# a int
assert isinstance(two, int)

## 2 + 2 = 5
assert two + two == 5
assert m9 + m9 == 18
assert two + 3 == 5
#
##Result of addition is also a MInt object
assert isinstance(two + two, MagicInt)
assert isinstance(two + 3, MagicInt)
#
## len() return the number of digits
assert len(two)==1
assert len(m127) == 3
assert len(MagicInt(-127)) == 3
#
## property prime that returns True the if it is a prime
assert m127.prime
assert (two+m127).prime==False
#
## Allow the user to set the 'prime' property manually
m127.prime = False
assert m127.prime==False

print("Yeah!!! All asserts satisfied")
