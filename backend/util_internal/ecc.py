import os
from ecpy.curves import Curve, Point
from ecpy.keys import ECPrivateKey, ECPublicKey
from ecpy.ecdsa import ECDSA
from ecpy.formatters import decode_sig, encode_sig
from ecpy.ecschnorr import ECSchnorr

def get_curve_names():
    return Curve.get_curve_names()

def get_curve_by_name(name):
    return Curve.get_curve(name)

c = Curve.get_curve("Brainpool-p256r1")
order = c.order
print(order)

# Generate a private key
scalar = int.from_bytes(os.urandom(32), 'big') % order
private_key = ECPrivateKey(scalar, c)

print(private_key)

public_key = private_key.get_public_key()
print(public_key)