from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa

print('::::::::::::: Welcome to KEYGEN :::::::::::::')
print('WARNING: Are you sure you want to run the script ?')
input("Press Enter to continue...")
print('It will over-write any existing keys in this directory. The consequences are irreversible, Do you REALLY wanna run it ?')
input("Press Enter to continue... ^C to quit.")
print('You were warned.')

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)
public_key = private_key.public_key()

from cryptography.hazmat.primitives import serialization
pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

with open('af_private_key.pem', 'wb') as f:
    f.write(pem)

pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

with open('af_public_key.pem', 'wb') as f:
    f.write(pem)

print('Done.')