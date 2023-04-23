def comb(n,r):
    if r == 0:
        return 1
    num = 1
    for i in range(n-r+1, n+1):
        num *= i
    den = 1
    for i in range(1, r+1):
        den *= i
    return num // den

print(comb(40,20))