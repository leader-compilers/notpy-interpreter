def factorial(n):
    if n == 1:
        return 1
    return n * factorial(n-1)

def sum_digits(n):
    if n < 10:
        return n
    return n % 10 + sum_digits(n // 10)

print(sum_digits(factorial(100)))