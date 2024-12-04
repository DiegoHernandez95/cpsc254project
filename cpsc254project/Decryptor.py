import os
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import unpad

class Decryptor:
    @staticmethod
    def decryptAESfile(file_path, aes_key):
        try:
            with open(file_path, "rb") as enc_file:
                iv = enc_file.read(16)
                ciphertext = enc_file.read()

            cipher = AES.new(aes_key, AES.MODE_CBC, iv)

            # Decrypt and unpad the plaintext
            padded_plaintext = cipher.decrypt(ciphertext)
            plaintext = unpad(padded_plaintext, AES.block_size)

            # Save the decrypted file
            decrypted_file_path = file_path.replace(".enc", ".dec")
            with open(decrypted_file_path, "wb") as dec_file:
                dec_file.write(plaintext)

            return decrypted_file_path
        except Exception as e:
            print(f"Error decrypting file with AES: {e}")
            return None

    @staticmethod
    def decryptRSAfile(file_path, rsa_private_key_path):
        try:
            # Load the RSA private key
            with open(rsa_private_key_path, "rb") as key_file:
                rsa_key = RSA.import_key(key_file.read())
            cipher_rsa = PKCS1_OAEP.new(rsa_key)

            with open(file_path, "rb") as enc_file:
                encrypted_data = enc_file.read()

            plaintext = cipher_rsa.decrypt(encrypted_data)

            # Save the decrypted file
            decrypted_file_path = file_path.replace(".rsa.enc", ".dec")
            with open(decrypted_file_path, "wb") as dec_file:
                dec_file.write(plaintext)

            return decrypted_file_path
        except Exception as e:
            print(f"Error decrypting file with RSA: {e}")
            return None

    # same as the encryptor.py, just call the functions above for decryption
    @staticmethod
    def BeginDecryption(file_path, key_file_path, key_type):
        try:
            if key_type == "AES":
                with open(key_file_path, "rb") as aes_key_file:
                    aes_key = aes_key_file.read()
                return Decryptor.decryptAESfile(file_path, aes_key)
            elif key_type == "RSA":
                return Decryptor.decryptRSAfile(file_path, key_file_path)
            else:
                raise ValueError("Unsupported key type!")
        except Exception as e:
            print(f"Error during {key_type} decryption: {e}")
            return None
