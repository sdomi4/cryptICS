# from ecc_inspector import ECCInvestigator

# a = -4
# b = 0
# p = 7

# ecc = ECCInvestigator(a, b, p)

# if ecc.is_curve_elliptic():
#     print("Curve is elliptic")

#     print("All points on curve:")
#     pointcounter = 0

#     for point in ecc.get_all_points_on_ec():
#         pointcounter += 1
#         print(f"Point {pointcounter}: {point}")
        
#     print("="*50)

#     print("Positive points on curve:")
#     pointcounter = 0

#     for point in ecc.get_positive_points_on_elliptic_curve():
#         pointcounter += 1
#         print(f"Point {pointcounter}: {point}")

#     print("="*50)

#     print("Primitive points on curve:")
#     pointcounter = 0
#     for point in ecc.get_primitive_points_on_elliptic_curve():
#         pointcounter += 1
#         print(f"Point {pointcounter}: {point}")

#     print(f"Order of curve: {ecc.get_order()}")
# else:
#     print("Curve is not elliptic")

