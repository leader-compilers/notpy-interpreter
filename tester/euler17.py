ones = {
    1: 'one',
    2: 'two',
    3: 'three',
    4: 'four',
    5: 'five',
    6: 'six',
    7: 'seven',
    8: 'eight',
    9: 'nine'
}

tens = {
    2: 'twenty',
    3: 'thirty',
    4: 'forty',
    5: 'fifty',
    6: 'sixty',
    7: 'seventy',
    8: 'eighty',
    9: 'ninety'
}

specials = {
    10: 'ten',
    11: 'eleven',
    12: 'twelve',
    13: 'thirteen',
    14: 'fourteen',
    15: 'fifteen',
    16: 'sixteen',
    17: 'seventeen',
    18: 'eighteen',
    19: 'nineteen'
}

def count_letters(n):
    if n < 10:
        return len(ones[n])
    elif n < 20:
        return len(specials[n])
    elif n < 100:
        count = len(tens[n // 10])
        if n % 10 != 0:
            count += len(ones[n % 10])
        return count
    elif n < 1000:
        count = len(ones[n // 100]) + len('hundred')
        if n % 100 != 0:
            count += len('and') + count_letters(n % 100)
        return count
    else:
        return len('onethousand')

total = sum(count_letters(n) for n in range(1, 1001))
print(total)
