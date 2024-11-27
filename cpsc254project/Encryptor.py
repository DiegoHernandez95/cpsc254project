import os
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

class Encryptor:
    @staticmethod
    def encryptAESfile(file_path, aes_key):
        try:
            # after doing some research using an initialization vector
            # helps further obfuscate the ciphertext making it difficult
            # to find patterns in the data
            iv = get_random_bytes(16)

            # decided to use CBC mode, other options are CTR
            # but it is not recommended
            cipher = AES.new(aes_key, AES.MODE_CBC, iv)
            with open(file_path, "rb") as file:
                plaintext = file.read()

            # Pad the plaintext and encrypt
            padded_data = pad(plaintext, AES.block_size)
            ciphertext = cipher.encrypt(padded_data)

            # Save the IV and ciphertext
            encrypted_file_path = file_path + ".enc"
            with open(encrypted_file_path, "wb") as enc_file:
                enc_file.write(iv + ciphertext)

            return encrypted_file_path
        except Exception as e:
            print(f"Error encrypting file with AES: {e}")
            return None

    # IMPORTANT RSA CAN ONLY ENCRYPT DATA EQUAL TO THE KEY SIZE
    # IN THIS CASE ANY FILE OVER 256 BYTES WILL RESULT IN AN ERROR
    # primary use case is to encrypt small data or the AES keys
    @staticmethod
    def encryptRSAfile(file_path, rsa_public_key_path):
        try:
            # Load the RSA public key
            with open(rsa_public_key_path, "rb") as key_file:
                rsa_key = RSA.import_key(key_file.read())
            cipher_rsa = PKCS1_OAEP.new(rsa_key)

            with open(file_path, "rb") as file:
                plaintext = file.read()

            encrypted_data = cipher_rsa.encrypt(plaintext)

            # Save the encrypted file
            encrypted_file_path = file_path + ".rsa.enc"
            with open(encrypted_file_path, "wb") as enc_file:
                enc_file.write(encrypted_data)

            return encrypted_file_path
        except Exception as e:
            print(f"Error encrypting file with RSA: {e}")
            return None

    # this method calls the static methods above to encrypt a file
    @staticmethod
    def BeginEncryption(file_path, key_file_path, key_type):
        try:
            if key_type == "AES":
                with open(key_file_path, "rb") as aes_key_file:
                    aes_key = aes_key_file.read()
                return Encryptor.encryptAESfile(file_path, aes_key)
            elif key_type == "RSA":
                return Encryptor.encryptRSAfile(file_path, key_file_path)
            else:
                print("Unsupported key type!")
                return None
        except Exception as e:
            print(f"Error during encryption: {e}")
            return None
