import math
from Crypto.Random import random
from typing import List, Tuple


class ECCInvestigator:
    def __init__(self, a: int, b: int, p: int):
        self.a = a
        self.b = b
        self.p = p

        if self.p <= 1:
            raise Exception("p must be at least 2")

    def is_curve_elliptic(self) -> bool:
        return (4 * pow(self.a, 3) + 27 * pow(self.b, 2)) % self.p != 0

    # extremely bruteforce way to do it, might be improvable
    def get_all_points_on_ec(self) -> List[Tuple[int, int]]:
        if not self.is_curve_elliptic():
            raise Exception("Curve must be elliptic")

        points_on_curve = []
        
        for x in range(-self.p + 1, self.p):
            for y in range(-self.p + 1, self.p):
                if self.is_point_on_curve(x, y):
                    points_on_curve.append((x, y))
        return points_on_curve

    def get_positive_points_on_elliptic_curve(self) -> List[Tuple[int, int]]:
        if not self.is_curve_elliptic():
            raise Exception("Curve must be elliptic")

        points_on_curve = []

        for x in range(self.p):
            for y in range(self.p):
                if self.is_point_on_curve(x, y):
                    points_on_curve.append((x, y))

        return points_on_curve

    def get_order(self) -> int:
        return len(self.get_positive_points_on_elliptic_curve()) + 1

    def get_primitive_points_on_elliptic_curve(self) -> List[Tuple[int, int]]:
        primitive_points = []

        positive_points = self.get_positive_points_on_elliptic_curve()
        last_calculated_point = None

        traversed_points_dict = {}

        for current_point in positive_points:
            traversed_points = [current_point]

            for y in range(1, len(positive_points)):
                try:
                    if y == 1:
                        last_calculated_point = self.double_point(current_point)
                    else:
                        last_calculated_point = self.add_two_points(current_point, last_calculated_point)
                    traversed_points.append(last_calculated_point)
                except ZeroDivisionError:
                    break

            #print(f"For point ({current_point[0]} , {current_point[1]}), traversed points:")
            traversed_points_dict[current_point] = traversed_points[:]

            # point_counter = 0
            # for point in traversed_points:
            #     point_counter += 1
            #     print(f"Point {point_counter}: ({point[0]} , {point[1]})")
            # print("\n")

            if len(traversed_points) == len(positive_points):
                primitive_points.append(current_point)

                for positive_point in positive_points:
                    for point in traversed_points:
                        if positive_point == point:
                            traversed_points.remove(point)
                            break

                if len(traversed_points) != 0:
                    raise RuntimeError("Error in point iteration: new point found or point traversed multiple times")
        return primitive_points, traversed_points_dict

    def double_point(self, point: Tuple[int, int]) -> Tuple[int, int]:
        if not self.is_curve_elliptic():
            raise RuntimeError("Curve must be elliptic")
        
        if point == (None, None):
            return (None, None)  # Point at infinity

        numerator = 3 * pow(point[0], 2) + self.a
        denominator = 2 * point[1]

        if denominator == 0:
            return (None, None)

        if denominator < 0:
            denominator *= -1
            numerator *= -1

        denominator = self.mod_inverse(denominator)
        if denominator is None:
            raise RuntimeError("Modular inverse does not exist.")

        s = int(numerator * denominator) % self.p

        x2 = (int(pow(s, 2)) - point[0] - point[0]) % self.p
        while x2 < 0:
            x2 += self.p

        y2 = (s * (point[0] - x2) - point[1]) % self.p
        while y2 < 0:
            y2 += self.p

        return (x2, y2)

    def add_two_points(self, point1: Tuple[int, int], point2: Tuple[int, int]) -> Tuple[int, int]:
        if not self.is_curve_elliptic():
            raise RuntimeError("Curve mustbe elliptic")

        if point1 == (None, None):
            return point2
        if point2 == (None, None):
            return point1
        if point1 == point2:
            return self.double_point(point1)

        numerator = point2[1] - point1[1]
        denominator = point2[0] - point1[0]

        if denominator == 0:
            return (None, None)

        if denominator < 0:
            denominator *= -1
            numerator *= -1

        denominator = self.mod_inverse(denominator)
        if denominator is None:
            raise RuntimeError("Modular inverse does not exist.")

        s = int(numerator * denominator) % self.p

        x3 = (int(pow(s, 2)) - point1[0] - point2[0]) % self.p
        while x3 < 0:
            x3 += self.p

        y3 = (s * (point1[0] - x3) - point1[1]) % self.p
        while y3 < 0:
            y3 += self.p

        return (x3, y3)

    def is_point_on_curve(self, x: int, y: int) -> bool:
        if not self.is_curve_elliptic():
            raise RuntimeError("Curve must be elliptic")

        return pow(y, 2) % self.p == (pow(x, 3) + self.a * x + self.b) % self.p

    # also very brutforce, is there no algorithm for this?
    def mod_inverse(self, value: int) -> int:
        if self.p == 1 or self.p == 0:
            return None

        if value % self.p == 0:
            raise ZeroDivisionError("Modular inverse does not exist if the value is a multiple of p")

        if math.gcd(value, self.p) != 1:
            raise ZeroDivisionError("p and the value are not coprime")

        if value < 0:
            raise ZeroDivisionError("Value cannot be negative for modular inverse calculation")

        for i in range(self.p):
            if (value * i) % self.p == 1:
                return i

        return None
    
    # added method to check if curve is cyclic
    def is_curve_primitive(self) -> bool:
        return len(self.get_primitive_points_on_elliptic_curve()) == self.get_order() - 1
    
    def scalar_multiplication(self, scalar: int, point: Tuple[int, int]) -> Tuple[int, int]:
        if not self.is_curve_elliptic():
            raise RuntimeError("Curve must be elliptic")
        
        if scalar == 0:
            return (0, 0)
        if scalar == 1:
            return point
        
        result = (None, None)
        addend = point

        while scalar:
            if scalar & 1:
                result = self.add_two_points(result, addend)
            addend = self.double_point(addend)
            scalar >>= 1
        return result

    
# random curve generator
def random_curve():
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    sanitycounter = 0
    while sanitycounter < 1000:
        a = random.randint(-30, 30)
        b = random.randint(-30, 30)
        p = random.choice(primes)

        ecc = ECCInvestigator(a, b, p)
        if ecc.is_curve_elliptic():
            return a, b, p, ecc.get_order()
        sanitycounter += 1
    print("Could not find a valid curve after 1000 tries")
    return None, None, None
    
def random_cyclic_curve():
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    sanitycounter = 0
    while sanitycounter < 1000:
        a = random.randint(-30, 30)
        b = random.randint(-30, 30)
        p = random.choice(primes)

        ecc = ECCInvestigator(a, b, p)
        if ecc.is_curve_elliptic() and ecc.is_curve_primitive():
            return a, b, p
        sanitycounter += 1
    print("Could not find a valid curve after 1000 tries")
    return None, None, None

def generate_private_key(order: int):
    return random.randint(1, order - 1)

def generate_base_point(a: int, b: int, p: int):
    ecc = ECCInvestigator(a, b, p)
    points = ecc.get_primitive_points_on_elliptic_curve()[0]
    return random.choice(points)

def generate_public_key(private_key: int, a: int, b: int, p: int, base_point: Tuple[int, int]):
    ecc = ECCInvestigator(a, b, p)
    return ecc.scalar_multiplication(private_key, base_point)