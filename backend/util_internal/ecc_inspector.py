import math
from Crypto.Random import random
from typing import List, Tuple, Dict


class ECCInvestigator:
    def __init__(self, a: int, b: int, p: int):
        self.a = a
        self.b = b
        self.p = p

        if self.p <= 1:
            raise Exception("p must be at least 2")

    def is_curve_elliptic(self) -> bool:
        return (4 * pow(self.a, 3) + 27 * pow(self.b, 2)) % self.p != 0

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

    def get_primitive_points_on_elliptic_curve(self) -> Tuple[List[Tuple[int, int]], Dict[Tuple[int, int], List[Tuple[int, int]]]]:
        primitive_points = []
        traversed_points_dict = {}

        positive_points = self.get_positive_points_on_elliptic_curve()
        total_points_count = len(positive_points) + 1  # Including point at infinity

        for current_point in positive_points:
            traversed_points = [current_point]
            last_calculated_point = current_point

            while True:
                last_calculated_point = self.add_two_points(last_calculated_point, current_point)
                if last_calculated_point == (None, None) or last_calculated_point in traversed_points:
                    break
                traversed_points.append(last_calculated_point)

            traversed_points_dict[current_point] = traversed_points[:]
            if len(traversed_points)+1 == total_points_count:
                primitive_points.append(current_point)
        return primitive_points, traversed_points_dict

    def get_order_of_point(self, point: Tuple[int, int]) -> int:
        order = 1
        current_point = point

        while current_point != (None, None):
            current_point = self.add_two_points(current_point, point)
            order += 1

        return order
    
    def count_points_by_order(self) -> Dict[int, int]:
        order_count = {}
        for point in self.get_all_points_on_ec():
            order = self.get_order_of_point(point)
            if order in order_count:
                order_count[order] += 1
            else:
                order_count[order] = 1
        return order_count

    def double_point(self, point: Tuple[int, int]) -> Tuple[int, int]:
        if not self.is_curve_elliptic():
            raise RuntimeError("Curve must be elliptic")
        
        if point == (None, None):
            return (None, None)  # Point at infinity

        if point[1] == 0:
            return (None, None)  # Tangent is vertical, result is point at infinity

        numerator = 3 * pow(point[0], 2) + self.a
        denominator = 2 * point[1]

        denominator = self.mod_inverse(denominator)
        if denominator is None:
            return (None, None)

        s = (numerator * denominator) % self.p

        x2 = (pow(s, 2) - 2 * point[0]) % self.p
        y2 = (s * (point[0] - x2) - point[1]) % self.p

        return (x2, y2)

    def add_two_points(self, point1: Tuple[int, int], point2: Tuple[int, int]) -> Tuple[int, int]:
        if not self.is_curve_elliptic():
            raise RuntimeError("Curve must be elliptic")

        if point1 == (None, None):
            return point2
        if point2 == (None, None):
            return point1
        if point1[0] == point2[0] and point1[1] != point2[1]:
            return (None, None)  # Points are vertical, result is point at infinity
        if point1 == point2:
            return self.double_point(point1)
        numerator = (point2[1] - point1[1]) % self.p
        denominator = (point2[0] - point1[0]) % self.p

        denominator = self.mod_inverse(denominator)
        if denominator is None:
            return (None, None)

        s = (numerator * denominator) % self.p

        x3 = (pow(s, 2) - point1[0] - point2[0]) % self.p
        y3 = (s * (point1[0] - x3) - point1[1]) % self.p

        return (x3, y3)

    def is_point_on_curve(self, x: int, y: int) -> bool:
        if not self.is_curve_elliptic():
            raise RuntimeError("Curve must be elliptic")

        return pow(y, 2) % self.p == (pow(x, 3) + self.a * x + self.b) % self.p

    def mod_inverse(self, value: int) -> int:
        value = value % self.p
        if value < 0:
            value += self.p

        g, x, _ = self.extended_gcd(value, self.p)
        if g != 1:
            raise ZeroDivisionError("Modular inverse does not exist if the value is a multiple of p")
        return x % self.p

    def extended_gcd(self, a: int, b: int) -> Tuple[int, int, int]:
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = self.extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

    def is_curve_primitive(self) -> bool:
        return len(self.get_primitive_points_on_elliptic_curve()[0]) == self.get_order() - 1

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
    
    def get_x_at_infinity(self, starting_point: Tuple[int, int]) -> int:
        order = self.get_order_of_point(starting_point)
    
        current_point = starting_point
        for i in range(1, order + 1):
            current_point = self.add_two_points(current_point, starting_point)
            if current_point == (None, None):
                return starting_point[0]
    
        raise ValueError("This infinity was very short (didn't reach infinity)")
    
# random curve generator
def random_curve():
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    sanitycounter = 0
    while sanitycounter < 1000:
        a = random.randint(0, 30)
        b = random.randint(0, 30)
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
        a = random.randint(0, 30)
        b = random.randint(0, 30)
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
    primitive_points, _ = ecc.get_primitive_points_on_elliptic_curve()
    if not primitive_points:
        raise ValueError("No primitive points found on the curve")
    return random.choice(primitive_points)

def generate_public_key(private_key: int, a: int, b: int, p: int, base_point: Tuple[int, int]):
    ecc = ECCInvestigator(a, b, p)
    return ecc.scalar_multiplication(private_key, base_point)
