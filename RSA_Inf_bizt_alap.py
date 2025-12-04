from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
import binascii
#Létrehozzuk a kulcspárokat
def generate_keys(bits=2048):
    key=RSA.generate(bits)
    private_key=key.export_key()
    public_key=key.publickey().export_key()
    return public_key,private_key
#Titkosítási folyamat
def encrypt(message,public_key):
    rsa_key=RSA.import_key(public_key)
    cipher=PKCS1_OAEP.new(rsa_key)
    encrypted_bytes=cipher.encrypt(message.encode("utf-8"))
    return binascii.hexlify(encrypted_bytes).decode("utf-8")
#Visszafejtési folyamat
def decrypt(ciphertext,private_key):
    rsa_key=RSA.import_key(private_key)
    cipher=PKCS1_OAEP.new(rsa_key)
    encrypted_bytes=binascii.unhexlify(ciphertext)
    decrypted_bytes=cipher.decrypt(encrypted_bytes)
    return decrypted_bytes.decode("utf-8")
#Az algoritmus kipróbálása
if __name__ == '__main__':
    public,private=generate_keys()

    print("Nyilvános kulcs:",public)
    print("Privát kulcs:",private)
    print()

    input_message= input("Írja be a titkosítani kívánt üzenetet:")
    encrypted_message=encrypt(input_message,public)
    print()
    print("Az üzenet titkosítva:",encrypted_message)

    decrypted_message=decrypt(encrypted_message,private)
    print("Visszafejtett üzenet:",decrypted_message)