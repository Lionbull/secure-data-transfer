from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

def encrypt_message(plaintext: str):
    """ Encrypt a message using AES-GCM and return the ciphertext, key, IV, and tag """
    key = os.urandom(32)  # AES 256-bit key
    iv = os.urandom(12)   # IV for AES-GCM
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
    return {
        "ciphertext": ciphertext.hex(),  # Store as hex string
        "key": key.hex(),                # Hex encode the key
        "iv": iv.hex(),                  # Hex encode the IV
        "tag": encryptor.tag.hex()       # Hex encode the GCM tag
    }


def decrypt_message(ciphertext_hex, key_hex, iv_hex, tag_hex):
    """ Decrypt a message using AES-GCM and return the plaintext """
    # Decode the hex-encoded data back to bytes
    ciphertext = bytes.fromhex(ciphertext_hex)
    key = bytes.fromhex(key_hex)
    iv = bytes.fromhex(iv_hex)
    tag = bytes.fromhex(tag_hex)
    
    # Set up the cipher
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag))
    decryptor = cipher.decryptor()
    
    # Decrypt and return plaintext
    return decryptor.update(ciphertext) + decryptor.finalize()
