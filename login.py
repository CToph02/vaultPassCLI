import crypto
import tables
import utils
import main
import os

jsonFunc = utils.jsonUtils()

crypt = crypto.Crypto()

class signup_login():
    def __init__(self):
        if not os.path.exists("userVault.json"):
            self.salt = os.urandom(16)
            self.salt64 = crypt.bytesToBase64(self.salt)

            self.pwdData = {
                'salt': self.salt64
            }

            jsonFunc.save_json("userVault.json", self.pwdData)

        else:
            self.pwdData = jsonFunc.load_json("userVault.json")

    def getSalt(self) -> str:
        return self.pwdData['salt']

    def sign_up(self):
        
        pwd = input("Ingrese una contraseña: ")
        
        salt = self.pwdData['salt']
        
        crypt.save_hash_b64(pwd, salt)

    def login(self):
        #inicio de sesion
        self.pwdData = jsonFunc.load_json("userVault.json")
        pwd = input("Password: ")
        
        hashed_pwd = self.pwdData['masterPwd']
        pwd64 = crypt.base64ToBytes(hashed_pwd)

        if crypt.verify_hash_pwd(pwd, pwd64):
            print("Welcome to vaultPass.")
            main.menu()
            return True
        
        else:
            print("user not found.")
            return False

def menu():
    obj_login = signup_login()

    while True:
        tables.login()

        try:
            opc = int(input("Select an option: "))

            if opc == 1:
                obj_login.sign_up()
                continue
                
            if opc == 2:
                if obj_login.login() is False:
                    continue
                else:
                    return True

            if opc == 0:
                break

            else:
                print("Invalid option.")
                continue

        except ValueError:
            print("Please, enter a number")

if __name__ == "__main__":
    menu()