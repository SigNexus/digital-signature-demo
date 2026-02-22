from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os

# Generate private key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

# Serialize private key
pem_private = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption()
)

# Serialize public key
pem_public = private_key.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Save private key to sender/Level3
os.makedirs('sender/Level3', exist_ok=True)
with open('sender/Level3/private.pem', 'wb') as f:
    f.write(pem_private)

# Save public key to root
with open('public.pem', 'wb') as f:
    f.write(pem_public)

print("Keys generated successfully.")
print("- Private: sender/Level3/private.pem")
print("- Public: public.pem")
