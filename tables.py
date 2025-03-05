from rich.table import Table
from rich.console import Console
import crypto
import utils
import json

consola = Console()
crypt = crypto.Crypto()
jsonFunc = utils.jsonUtils()

def listTable(deriveKey, favorite = None, name = None):
    
    data_user = jsonFunc.load_json("userVault.json")
    data = data_user["data"]

    if data and len(data) > 16:
        try:
            decrypted_data = crypt.decrypt(data, deriveKey)
            listTable = Table(title="Passwords", show_lines=True)

            listTable.add_column("App name",justify="center")
            listTable.add_column("Password",justify="center")
            listTable.add_column("Created at",style="color(2)")
            listTable.add_column("Updated at",style="color(3)")

            if favorite is not None:
                listTable.add_column("Favorite",style="color(5)")
            else:
                listTable.add_column("Favorite",style="color(1)")

            data_dict = json.loads(decrypted_data)

            for app, pwd in data_dict.items():
                password = pwd.get("password", "N/A")
                createdAt = pwd.get("createdAt", "N/A")
                updatedAt = pwd.get("updatedAt", "N/A")
                fav = pwd.get("favorite", "no")

                if (favorite is None and name is None) or (favorite is not None and fav == favorite) or (name is not None and app.startswith(name)):
                        listTable.add_row(
                                    app,
                                    password, 
                                    createdAt, 
                                    updatedAt,
                                    fav
                                )
                        
            if listTable.rows:
                consola.print(listTable)

            else:
                print("No results found.")

        except Exception as e:
            print(f"\nDecryption error: {e}")
            decrypted_data = {}
    else:
        decrypted_data = {}
    

def menuTable():
    menuTable = Table(title="vaultPass", show_lines=True)
    menuTable.add_column("Option")
    menuTable.add_column("Description")

    menuTable.add_row("1", "Add password")
    menuTable.add_row("2", "Edit password")
    menuTable.add_row("3", "Delete password")
    menuTable.add_row("4", "List passwords")
    menuTable.add_row("5", "Search password by favorite")
    menuTable.add_row("6", "Search by name")
    menuTable.add_row("7", "add or remove passwords from favorites")
    menuTable.add_row("8", "Generate random password")
    menuTable.add_row("0", "Exit")

    consola.print(menuTable)

def login():
    loginTable = Table(title="vaultPass access")
    loginTable.add_column("Option")
    loginTable.add_column("Description")

    loginTable.add_row("1", "Sign up")
    loginTable.add_row("2", "Log in")
    loginTable.add_row("0", "Exit")
    consola.print(loginTable)