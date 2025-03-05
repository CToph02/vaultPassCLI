from datetime import datetime
import passGen
import tables
import crypto
import json
from login import signup_login
import utils

crypt = crypto.Crypto()
log = signup_login()
jsonFunc = utils.jsonUtils()

class functMain():
    def __init__(self):
        self.decrypted_data = {}
        self.pwdData = jsonFunc.load_json("userVault.json")
        self.salt64 = log.getSalt()
        self.saltBytes = crypt.base64ToBytes(self.salt64)

    def deriveMaster(self) -> bytes:
        self.pwdData = jsonFunc.load_json("userVault.json")      
        if self.pwdData["masterPwd"]:
            self.derive = crypt.derive_key(self.pwdData["masterPwd"], self.saltBytes)
            return self.derive
        else:
            raise ValueError("No hay contraseña.")

    def addPwd(self, nameService, pwd):
        deriveKey: bytes = self.deriveMaster()

        if not nameService or not pwd:
            print("Please, fill data.")

        else:
            try:
                encrypted_data = self.pwdData.get("data", "")
                

                if encrypted_data:
                    self.decrypted_data = json.loads(crypt.decrypt(encrypted_data, deriveKey))

                new = {
                    "password": pwd,
                    "createdAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "updatedAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "favorite": "no"
                }
                
                self.decrypted_data[nameService] = new

                encrypted_data = crypt.encrypt(json.dumps(self.decrypted_data), deriveKey)

                self.pwdData["data"] = encrypted_data

                jsonFunc.save_json("userVault.json", self.pwdData)

            except Exception as e:
                print(f"Error: {e}")

    def editPwd(self, name):
        deriveKey: bytes = self.deriveMaster()
        encrypted_data = self.pwdData.get("data", "")

        if encrypted_data:
            decrypted_data = json.loads(crypt.decrypt(encrypted_data, deriveKey))

        if not name:
            print("Please, fill data.")

        elif name in decrypted_data:
            try:
                print(decrypted_data)
                newName = input(
                    f"Enter new name for: {name}. (Leave blank if you don´t want to change it): "
                ).strip()
                print(newName)

                newPwd = input(
                    f"Enter new password for: {decrypted_data[name]['password']}. (Leave blank if you don´t want to change it): "
                ).strip()

                if newName:
                    decrypted_data[newName] = decrypted_data.pop(name)
                    name = newName

                if newPwd:
                    decrypted_data[name]["password"] = newPwd

                # Actualize update time
                decrypted_data[name]["updatedAt"] = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                encrypted_data = crypt.encrypt(json.dumps(decrypted_data), deriveKey)

                self.pwdData["data"] = encrypted_data
                print(self.pwdData["data"])

                # Save new data
                jsonFunc.save_json("userVault.json", self.pwdData)
                print(
                    f"\nActualized data for {name}: Name: {newName if newName else name}, Password: {newPwd} "
                )

            except Exception as e:
                print(f"Error: {e}")

    def delPwd(self, name):
        deriveKey: bytes = self.deriveMaster()

        encrypted_data = self.pwdData.get("data", "")

        if encrypted_data:
            try:
                decrypted_data = json.loads(crypt.decrypt(encrypted_data, deriveKey))
            except Exception as e:
                print(f"Error al desencriptar: {e}")
                return

        if name in decrypted_data:
            confirm = input(f"Seguro que quieres eliminar {name}? (Y/n): ")

            if confirm.lower() == "y":
                del decrypted_data[name]
                print(f"{name} has been succesfully removed.")

                if not decrypted_data:
                    self.pwdData["data"] = ""
                else:

                    encrypted_data = crypt.encrypt(json.dumps(decrypted_data), deriveKey)
                    self.pwdData["data"] = encrypted_data

                jsonFunc.save_json("userVault.json", self.pwdData)
            else:
                print("deletion cancelled.")

        else:
            print("no exist.")

    def searchByName(self, name=None):
        derive = self.deriveMaster()
        
        tables.listTable(derive, name=name)

    def listPwd(self, favorite=None):
        if self.pwdData["data"] == "":
            print("No hay datos para mostrar.")
        else:
            derive = self.deriveMaster()
            
            tables.listTable(derive, favorite=favorite)

    def genPwd(self):
        defOrCust = (
            input("Do you want a custom password? (Yes/no = Default): ").strip().lower()
        )

        if defOrCust == "no" or defOrCust == "":
            print(f"Your password: {passGen(20, True, False, True, True)}")

        elif defOrCust == "yes":
            try:
                length = int(input("Lenght: ").strip())

                low = input("Lower case? (y/no = Enter):").strip().lower() == "y"
                up = input("Upper case? (y/no = Enter): ").strip().lower() == "y"
                dig = input("Digits? (y/no = Enter): ").strip().lower() == "y"
                symb = input("Symbols? (y/no = Enter): ").strip().lower() == "y"

                if not (low or up or dig or symb):
                    print("Error: deberias de seleccionar por lo menos una opción")
                    return

                else:
                    print(f"Your password: {passGen(length, low, up, dig, symb)}")

            except ValueError:
                print("Invalid input for length. Please enter a valid integer.")

    def favorite(self):
        deriveKey: bytes = self.deriveMaster()

        name = input("Enter name to add to favorite: ")
        encrypted_data = self.pwdData.get("data", "")

        if encrypted_data:
            decrypted_data = json.loads(crypt.decrypt(encrypted_data, deriveKey))

        if name in decrypted_data:
            addFavorite = input("add/remove: ").lower().strip()

            if addFavorite not in ("add", "remove"):
                print("Please enter add or remove.")

            elif addFavorite == "add":
                if decrypted_data[name]["favorite"] == "yes":
                    print("Is already in favorites.")
                else:
                    decrypted_data[name]["favorite"] = "yes"

            elif addFavorite == "remove":
                if decrypted_data[name]["favorite"] == "no":
                    print("Its not in favorites.")
                else:
                    decrypted_data[name]["favorite"] = "no"
            
            encrypted_data = crypt.encrypt(json.dumps(decrypted_data), deriveKey)
            self.pwdData["data"] = encrypted_data

            jsonFunc.save_json("userVault.json", self.pwdData)

        else:
            print(f"The name {name} is not in the database.")