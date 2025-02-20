from Crypto.PublicKey import RSA as CryptoRSA
from Crypto.Cipher import PKCS1_OAEP

# Gera chaves RSA com PyCryptodome
def generate_key(key_size=4096):
    key = CryptoRSA.generate(key_size)
    return key, key.publickey()

# Criptografa com PyCryptodome
def encrypt(message, public_key):
    cipher = PKCS1_OAEP.new(public_key)
    return cipher.encrypt(message)

# Descriptografa com PyCryptodome
def decrypt(ciphertext, private_key):
    cipher = PKCS1_OAEP.new(private_key)
    return cipher.decrypt(ciphertext)