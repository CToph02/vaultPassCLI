#For cryptography
from cryptography.hazmat.primitives.ciphers import Cipher,algorithms,modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import bcrypt
import base64
import os
import utils

jsonFunc = utils.jsonUtils()

class Crypto():
    def __init__(self):
        self.pwdData = jsonFunc.load_json("userVault.json")

    def base64ToBytes(self, base_64: str) -> bytes:
        return base64.b64decode(base_64.encode())

    def bytesToBase64(self, bytesData: bytes) -> str:
        return base64.b64encode(bytesData).decode()

    def save_hash_b64(self, pwd: str, salt: bytes):
        hashed_pwd: bytes = self.hash_master_pwd(pwd) #Hashea a bytes la contraseña
        pwd64 = self.bytesToBase64(hashed_pwd)

        self.pwdData = {
            'masterPwd': pwd64,
            'salt': salt
        }

        jsonFunc.save_json("userVault.json", self.pwdData)

    def load_hash_b64(self) -> bytes:
        data = jsonFunc.load_json("userVault.json")
        return self.base64ToBytes(data["pwd"])

    def hash_master_pwd(self, password: str) -> bytes:
        hash_pwd = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        return hash_pwd

    def verify_hash_pwd(self, password: str, hashed_pwd64: bytes) -> bool:
        check = bcrypt.checkpw(password.encode(), hashed_pwd64)
        return check

    #Derivate master password 
    def derive_key(self, master: str, salt: bytes) -> bytes:
        if not master:
            raise ValueError("La contraseña maestra está vacía.")

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(), #SHA256 hash function
            length=32,                 #32bits clave generada
            salt=salt,            #Salt para que c/pwd séa única  
            iterations=100000
        )

        return kdf.derive(master.encode()) #Genera y devuelve la clave
    
    def base64_to_bytes_with_padding(self, base64_str: str) -> bytes:
        # Agregar padding si es necesario
        padding = len(base64_str) % 4
        if padding != 0:
            base64_str += "=" * (4 - padding)
        return base64.b64decode(base64_str)

    def encrypt(self, password, key) -> str:
        iv = os.urandom(12)
        cipher  = Cipher(algorithms.AES(key), modes.GCM(iv))
        encryptor = cipher.encryptor()
        encrypted_pass = encryptor.update(password.encode())+encryptor.finalize()
        return base64.b64encode(iv + encryptor.tag + encrypted_pass).decode()


    def decrypt(self, encrypted_pwd, key) -> dict:
        encrypted_pwd = self.base64_to_bytes_with_padding(encrypted_pwd)
        iv, tag, encrypted_data = encrypted_pwd[:12], encrypted_pwd[12:28], encrypted_pwd[28:] #12bits para iv, 16bits tag, resto de bits son los datos
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag))
        decryptor = cipher.decryptor()
        return (decryptor.update(encrypted_data) + decryptor.finalize()).decode()