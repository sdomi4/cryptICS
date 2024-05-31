from functools import reduce
from typing import List, Dict, Tuple
import math

def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def lcm(x, y):
    return (x * y) // math.gcd(x, y)

def carmichael(n: int) -> Dict[str, List[Tuple[str, int]]]:
    if n <= 0:
        raise ValueError("n must be a positive integer")
    
    # Factorize n
    original_n = n
    factors = []
    i = 2
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)

    unique_factors = list(set(factors)) 
    steps = {}
    steps["factorization"] = factors

    # Calculate lambda(p^e) for each unique prime factor
    lambdas = []
    steps["lambdas"] = []
    for p in unique_factors:
        exp = factors.count(p)
        if p == 2 and exp >= 3:
            lambda_pe = 2 ** (exp - 2)
        elif p == 2 and (exp == 1 or exp == 2):
            lambda_pe = 2 ** (exp - 1)
        else:
            lambda_pe = (p - 1) * (p ** (exp - 1))

        steps["lambdas"].append((f"λ({p}^{exp})", lambda_pe))
        lambdas.append(lambda_pe)
    
    # Compute lcm of all lambda(p^e)
    lambda_n = reduce(lcm, lambdas)
    steps["result"] = ("λ(n)", lambda_n)

    return {
        "number": original_n,
        "steps": steps,
        "result": lambda_n
    }