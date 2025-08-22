from PasswordManager import PasswordManager
from settings import db_connection_data

if __name__ == "__main__":
    pm = PasswordManager(**db_connection_data)
    pm.update_username(site_name="test",username="nre_test", new_username="new_test")
    print(pm.get_password("test"))