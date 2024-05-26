from math import sqrt
from backend.util_internal.ecc_inspector import ECCInvestigator
from Crypto.Random import random

def generate_practice_points(a: int, b: int, p: int):
    ecc = ECCInvestigator(a, b, p)
    
    points = ecc.get_positive_points_on_elliptic_curve()
    base_point = random.choice(points)

    # m, n, k, where m + 2n = k or 2m + n = k
    practice_combinations = [
        (1,2,5),
        (2,3,7),
        (2,3,8),
        (3,4,10),
        (3,4,11),
        (2,4,10),
        (3,5,13),
        (3,5,11),
        (3,6,15),
        (2,6,14),
        (5,7,17),
        (5,7,19),
        (4,7,15),
        (4,7,18),
        (3,8,14),
        (3,8,19),
        (5,6,16),
        (5,6,17),
        (7,8,22),
        (7,8,23)
    ]

    practice_points = random.choice(practice_combinations)

    m = ecc.scalar_multiplication(practice_points[0], base_point)
    k = ecc.scalar_multiplication(practice_points[1], base_point)
    q = ecc.scalar_multiplication(practice_points[2], base_point)

    mod_inverse_table = [ecc.mod_inverse(i) for i in range(1, p-1)]

    return {
        "m": m,
        "k": k,
        "q": q,
        "inverse_table": mod_inverse_table,
        "practice_points": practice_points
    }

def check_nonsingularity(a: int, b: int, p: int):
    # return result instead of boolean
    return 4 * pow(a, 3) + 27 * pow(b, 2) % p

def check_point_on_curve(x: int, y: int, a: int, b: int, p: int):
    # return results of both sides of equation to check inputs
    left = pow(y, 2) % p
    right = (pow(x, 3) + a * x + b) % p
    return left, right

def inverse_point(x: int, y: int, p: int):
    return x, -y % p

def hasse_theorem(p: int):
    return p+1 - 2*(sqrt(p)), p+1 + 2*(sqrt(p))