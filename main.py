from PasswordManager import PasswordManager
from settings import db_connection_data

if __name__ == "__main__":
    pm = PasswordManager(**db_connection_data)
    pm.delete_password(site_name="test2", username="hi")
    print(pm.get_all())