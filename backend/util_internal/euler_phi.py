from math import gcd

def _is_coprime(x, y):
    return gcd(x, y) == 1

def euler_phi(x):
    if x == 1:
        return 1
    n = [y for y in range(1, x) if _is_coprime(x, y)]
    return len(n)