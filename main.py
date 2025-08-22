from PasswordManager import PasswordManager
from settings import db_connection_data

if __name__ == "__main__":
    pm = PasswordManager(**db_connection_data)

    while True:
        user_inp = input(
            "create: 1, update: 2, delete: 3, retrieve: 4, all: 5, exit: n\ntype:"
        )
        if user_inp.lower() not in ["1", "2", "3", "4", "5", "n"]:
            print("Wrong input try again")
            continue
        elif user_inp == "1":
            site_name = input("please enter site name:")
            username = input("please enter username:")
            password = input("please enter password:")
            pm.create_password(site_name, username, password)
            print(f"**********All users of {site_name}**********")
            print(pm.get_password(site_name))
            print("*" * 35)
        elif user_inp == "2":
            while True:
                user_ans = input(
                    "Do you want to update username or password?[username u, password p]"
                )
                if user_ans.lower() not in ["u", "p"]:
                    print("Wrong input try again")
                    continue
                elif user_ans.lower() == "u":
                    site_name = input("In which site you want to change the username?")
                    print(f"**********All users of {site_name}**********")
                    print(pm.get_password(site_name))
                    print("*" * 35)
                    old_username = input("tell me the old username:")
                    new_username = input("tell me the new username:")
                    pm.update_username(site_name, old_username, new_username)
                    break
                elif user_ans.lower() == "p":
                    site_name = input("In which site you want to change the password?")
                    print(f"**********All users of {site_name}**********")
                    print(pm.get_password(site_name))
                    print("*" * 35)
                    username = input("Which username you want to change the password:")
                    new_password = input("tell me the new password:")
                    pm.update_password(site_name, username, new_password)
                    break
        elif user_inp == "3":
            site_name = input("In which site you want to delete the password?")
            username = input("which username you want to delete?")
            pm.delete_password(site_name, username)
            print(f"**********All users of {site_name}**********")
            print(pm.get_password(site_name))
            print("*" * 35)
        elif user_inp == "4":
            site_name = input("which sites password you want to see?")
            print(pm.get_password(site_name))
        elif user_inp == "5":
            print(pm.get_all())
        elif user_inp.lower() == "n":
            print("Bye. have fun.")
            break
