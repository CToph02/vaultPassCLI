#!/usr/bin/env python3
#Main password manager
import functions
from tables import menuTable

objMain = functions.functMain()
    
def menu():
    while True:
        menuTable()
        try:
            menuOpc = int(input("Select option: "))
            
            if menuOpc == 1:
                name = input("App name: ")
                password = input("Password: ")
                objMain.addPwd(name, password)
                continue

            if menuOpc == 2:
                objMain.listPwd()
                nameToEdit = input("\nEnter name to edit: ")
                objMain.editPwd(nameToEdit)
                continue

            if menuOpc == 3:
                nameToDelete = input("\nEnter name to delete: ")
                objMain.delPwd(nameToDelete)
                continue

            if menuOpc == 4:
                objMain.listPwd()
                continue
            
            if menuOpc == 5:
                objMain.listPwd("yes")
                continue

            if menuOpc == 6:
                name = input("Enter name to search: ")
                objMain.searchByName(name)
                continue

            if menuOpc == 7:
                objMain.listPwd() 
                objMain.favorite()
                continue

            if menuOpc == 8:
                objMain.genPwd()
                continue
            
            if menuOpc == 0:
                print("Thanks for use vaultPass.")
                break
            else:
                print("Enter a valid option.")
                continue

        except Exception as e:
            print(f"Error {e}")

#if __name__ == "__main__":
#    menu()