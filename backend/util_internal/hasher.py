import Crypto.Hash.BLAKE2b
import Crypto.Hash.BLAKE2s
import Crypto.Hash.CMAC
import Crypto.Hash.cSHAKE128
import Crypto.Hash.cSHAKE256
import Crypto.Hash.HMAC
import Crypto.Hash.KangarooTwelve
import Crypto.Hash.keccak
import Crypto.Hash.KMAC128
import Crypto.Hash.KMAC256
import Crypto.Hash.MD2
import Crypto.Hash.MD4
import Crypto.Hash.MD5
import Crypto.Hash.Poly1305
import Crypto.Hash.RIPEMD160
import Crypto.Hash.SHA
import Crypto.Hash.SHA1
import Crypto.Hash.SHA224
import Crypto.Hash.SHA256
import Crypto.Hash.SHA384
import Crypto.Hash.SHA3_224
import Crypto.Hash.SHA3_256
import Crypto.Hash.SHA3_384
import Crypto.Hash.SHA3_512
import Crypto.Hash.SHA512
import Crypto.Hash.SHAKE128
import Crypto.Hash.SHAKE256
import Crypto.Hash.TupleHash128
import Crypto.Hash.TupleHash256


def create_hash(algorithm: str, data: str):
    match algorithm:
        case "blake2b":
            h = Crypto.Hash.BLAKE2b.new()
        case "blake2s":
            h = Crypto.Hash.BLAKE2s.new()
        case "cmac":
            h = Crypto.Hash.CMAC.new()
        case "cshake128":
            h = Crypto.Hash.cSHAKE128.new()
        case "cshake256":
            h = Crypto.Hash.cSHAKE256.new()
        case "hmac":
            h = Crypto.Hash.HMAC.new()
        case "kangarootwelve":
            h = Crypto.Hash.KangarooTwelve.new()
        case "keccak":
            h = Crypto.Hash.keccak.new()
        case "kmac128":
            h = Crypto.Hash.KMAC128.new()
        case "kmac256":
            h = Crypto.Hash.KMAC256.new()
        case "md2":
            h = Crypto.Hash.MD2.new()
        case "md4":
            h = Crypto.Hash.MD4.new()
        case "md5":
            h = Crypto.Hash.MD5.new()
        case "poly1305":
            h = Crypto.Hash.Poly1305.new()
        case "ripemd" | "ripemd160":
            h = Crypto.Hash.RIPEMD160.new()
        case "sha":
            h = Crypto.Hash.SHA.new()
        case "sha1":
            h = Crypto.Hash.SHA1.new()
        case "sha224":
            h = Crypto.Hash.SHA224.new()
        case "sha256":
            h = Crypto.Hash.SHA256.new()
        case "sha384":
            h = Crypto.Hash.SHA384.new()
        case "sha3_224":
            h = Crypto.Hash.SHA3_224.new()
        case "sha3_256":
            h = Crypto.Hash.SHA3_256.new()
        case "sha3_384":
            h = Crypto.Hash.SHA3_384.new()
        case "sha3_512":
            h = Crypto.Hash.SHA3_512.new()
        case "sha512":
            h = Crypto.Hash.SHA512.new()
        case "shake128":
            h = Crypto.Hash.SHAKE128.new()
        case "shake256":
            h = Crypto.Hash.SHAKE256.new()
        case "tuplehash128":
            h = Crypto.Hash.TupleHash128.new()
        case "tuplehash256":
            h = Crypto.Hash.TupleHash256.new()
        case _:
            return None
    h.update(data.encode())
    return h.hexdigest()