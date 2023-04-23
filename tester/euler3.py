k = 600851475143                                    
primeFactors = []                                   
while k > 1:                                       
    i = 2                                           
    while k % i != 0:                               
        i += 1                                      
    k = k / i                                       
    primeFactors.append(i)                          
print(primeFactors[len(primeFactors) - 1])          
print(len(primeFactors))