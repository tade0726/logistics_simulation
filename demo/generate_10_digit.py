import math
import time
from functools import wraps


def generator_digit_max(n):
    if n == 0:
        return 1 * 9
    return generator_digit_max(n-1) + math.pow(10, n) * 9

def generator_digit(n):
    for i in range(int(generator_digit_max(n-1))):
        yield f"{i:0>{n}}"

def generator_digit2(n):
    for i in range(int('9' * n)):
        yield f"{i:0>{n}}"

a = generator_digit(10)
b = generator_digit2(10)


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        t0 = time.time()
        result = func(*args, **kwargs)
        print('%r (%r, %r) %2.5f sec' % \
              (func.__name__, args, kwargs, time.time() - t0) )
        return result
    return wrapper


@timer
def test1():
    for i, x in enumerate(a):
        if i < 10:
            print(x)
        else:
            break

@timer
def test2():
    for i, x in enumerate(b):
        if i < 10:
            print(x)
        else:
            break

if __name__ == '__main__':
    test1()
    test2()
