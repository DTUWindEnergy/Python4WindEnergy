# -*- coding: utf-8 -*-
"""
Python 2.7.5
System: Sager NP8230 Clevo P151SM1 - Fenix
OS: Windows 7 x64 Professional
Date: Tue Jan 21 20:27:23 2014

*******************************************************************
*                                                                 *
*   Function Description: Exercise Magic Number.                  *
*   Class MagicInt that satisfies the assert statements:          *
*   •Is a int                                                     *
*   •Makes 2 + 2 = 5                                              *
*   •Result of addition is also a MagicInt object                 *
*   •Lets len(magicInt) return the number of digits               *
*   •Has a property prime that returns True the if it is a prime. *
*   •Allows the user to set the prime property manually           *
*                                                                 *
*                                                                 *
*   Copyright (c) / Derechos Reservados                           *
*   José Francisco Herbert Acero                                  *
*   jf.herbert.phd.mty@itesm.mx                                   *
*   http://fisica.mty.itesm.mx/fisica/WEG/                        *
*                                                                 *
*   Cátedra de Energía Eólica / Research Chair for Wind Energy    *
*   Departamento de Física / Physics Department                   *
*   Tecnológico de Monterrey, Campus Monterrey                    *
*   Monterrey, N.L., México                                       *
*                                                                 *
*******************************************************************

"""
#MagicInt Class definition, inherits from the int class.
#By convention, user-defined classes start with a capital letter:
class MagicInt(int):
    
    #Initialization function. Self refers to the MagicInt object 
    #being created and num refers to an arbitrary integer number:
    def __init__(self,num):
        self.val=num                    #Gives the attribute val to self.
        self.prime=self.is_prime(num)   #Gives the attribute prime to self,
                                        #which is a boolean value determined
                                        #by the function is_prime implemented
                                        #next:
    
    #is_prime function. Determines if an integer number is a prime number:
    def is_prime(self,num):
        #A prime number is a positive integer greater than 1 that has no 
        #positive divisors other than 1 and itself.
        if num > 1:                     #Verify if num is prime:
            return all([num%x>0 for x in range(2,num)])
        else:                           #num was lower than one.
            return False
    
    #Add function. (1) Verifies if num2 is a MagicInt object, (2) Performs 
    #the sum of num and num2.
    def __add__(self,num2):
        #Checks if num2 is an instance of the MagicInt class:
        if isinstance(num2,MagicInt):
            #If num2.val and self.val are equal then returns their sume +1:
            if num2.val==self.val:
                summ=MagicInt(self.val+num2.val+1)
                return summ
            #Otherwise returns their sum:
            else:
                summ=MagicInt(self.val+num2.val)
                return summ
        
        #num2 is not an instance of MagicInt class. Creates a MagicInt instance
        #using num2 and performs the sum between num and num2:        
        else:
            return MagicInt.__add__(self,MagicInt(num2))
    
    #Length function. Returns the number of digits of self.val without including
    #its sign:
    def __len__(self):
        return len(str(abs(self.val)))


#Test section: Do not modify code below.
two = MagicInt(2)
m127 = MagicInt(127)

# a int
assert isinstance(two, int)

# 2 + 2 = 5
assert two + two == 5
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