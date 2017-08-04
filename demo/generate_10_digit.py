import math


def generator_digit_max(n):
    if n == 0:
        return 1 * 9
    return generator_digit_max(n-1) + math.pow(10, n) * 9

def generator_digit(n):
    for i in range(int(generator_digit_max(n))):
        yield f"{i:0>{n}}"

a = generator_digit(10)

for i, x in enumerate(a):
    if i < 10:
        print(x)