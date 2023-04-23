def collatz_length(n):
    length = 1
    while n > 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        length += 1
    return length

max_length = 0
max_start = 0

for i in range(1, 1000000):
    length = collatz_length(i)
    if length > max_length:
        max_length = length
        max_start = i

print(max_start)