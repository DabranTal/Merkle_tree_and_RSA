import base64
import textwrap

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key


def findPublicAndPrivateKeys():
    alg = serialization.NoEncryption()
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
    public_key = private_key.public_key()
    private_key_hex = private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                                    encryption_algorithm=alg).decode()
    public_key_hex = public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                              format=serialization.PublicFormat.SubjectPublicKeyInfo).decode()
    print(private_key_hex)
    print(public_key_hex)

def signatureOnRoot(key):
    root = b"ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb"
    realSignature = key.sign(root, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
                         hashes.SHA256())
    signature = base64.encodebytes(key.sign(root, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
                         hashes.SHA256())).decode()
    print(signature.replace("\n", ""))


def verification(key, signatureInBytes, message):
    message = message.encode()
    try:
        key.verify(
            signatureInBytes,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        print(True)
    except:
        print(False)

def getInput(key):
    v = input()
    while(v != ""):
        key += v
        key += "\n"
        v = input()
    return key



while(True):
    val = input()
    if val == "5":
        findPublicAndPrivateKeys()
    else:
        userInput = val[:2]
        if userInput == "6 ":
            key = val[2:]
            key += "\n"
            key = getInput(key)
            jKey = textwrap.dedent(key).encode()
            oKey = load_pem_private_key(jKey, password=None, backend=default_backend())
            signatureOnRoot(oKey)
        elif userInput == "7 ":
            key = val[2:]
            key += "\n"
            key = getInput(key)
            jKey = textwrap.dedent(key).encode()
            oKey = load_pem_public_key(jKey, backend=default_backend())
            anInput = input()
            signature, verText = anInput.split()
            signatureInBytes = base64.decodebytes(bytes(signature, "utf-8"))
            verification(oKey, signatureInBytes, verText)



