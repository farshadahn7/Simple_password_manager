from db.db_connection import connect_db
import psycopg2
from cryptography.fernet import Fernet

class PasswordManager:
    def __init__(self, db_name, db_user, db_pass, db_host, db_port, encrypt_key):
        self.conn = connect_db(db_name, db_user, db_pass, db_host, db_port)
        self.cipher_suite = Fernet(encrypt_key)
    def get_cursor(self):
        return self.conn.cursor()

    def _encrypt_password(self, password):
        cipher_pass = self.cipher_suite.encrypt(password.encode("utf-8"))
        return cipher_pass.decode("utf-8")

    def _decrypt_password(self, password):
        password_bytes = password.encode("utf-8")
        plain_pass = self.cipher_suite.decrypt(password_bytes)
        return plain_pass.decode()

    def create_password(self, site_name, username, password):
        try:
            site_id = 0
            try:
                site_id = self.get_site_id(site_name)[0][0]
            except IndexError:
                print(f"{site_name} does not exists. Creating a new one ....")
                self.create_site_name(site_name)
                site_id = self.get_site_id(site_name)[0][0]
            except psycopg2.errors as e:
                print(f"opps something went wrong. errors:{e}")
                self.conn.rollback()
            sql = "insert into passwords (site_id,username,password_hash) values (%s,%s,%s)"
            password_hash = self._encrypt_password(password)
            data = (site_id, username, password_hash)
            self.execute_sql(sql=sql,data=data,commit=True)

            print("Data insertion completed successfully.")
        except psycopg2.errors as e:
            print(f"Opps something went wrong during the insertion, errors{e}")

    def create_site_name(self, site_name):
        try:
            sql = "INSERT INTO site (site_name) VALUES (%s)"
            data = (site_name,)
            self.execute_sql(sql=sql,data=data,commit=True)

        except psycopg2.errors as e:
            print(f"Opps something went wrong during the insertion, errors{e}")

    def update_site_name(self, site_name, new_site_name):
        try:
            sql = "update site set site_name=%s where site_name=%s"
            data = (new_site_name, site_name)
            self.execute_sql(sql=sql,data=data,commit=True)
        except psycopg2.errors as e:
            print(f"Oops something went wrong. errors {e}")

        print("Site name is updated successfully.")

    def update_password(self, site_name, username, password):
        try:
            site_id = self.get_site_id(site_name)[0][0]
            sql = "update passwords set password_hash = %s where site_id = %s and username = %s"
            password_hash = self._encrypt_password(password)
            data = (password_hash, site_id, username)
            self.execute_sql(sql=sql,data=data,commit=True)
            print("Password updated_successfully")
        except IndexError:
            print(f"{site_name} does not exists.")
            self.conn.rollback()

    def update_username(self, site_name, username, new_username):
        try:
            site_id = self.get_site_id(site_name)[0][0]
            sql = "update passwords set username = %s where site_id = %s and username = %s"
            data = (new_username, site_id, username)
            self.execute_sql(sql=sql,data=data,commit=True)
            print("username updated successfully.")
        except IndexError:
            print(f"{site_name} does not exists.")
            self.conn.rollback()
        except psycopg2.errors as e:
            print(f"Oops something went wrong. Errors: {e}")

    def get_site_id(self, site_name):
        try:
            sql = "select id from site where site_name=%s"
            data = (site_name,)
            query = self.execute_sql(sql=sql,data=data,fetchall=True)
            return query
        except psycopg2.errors as e:
            print(f"opps sth went wrong by returning site id. Errors: {e}")

    def get_password(self, site_name):
        try:
            site_id = self.get_site_id(site_name)[0][0]
            sql = "select site_name, username, password_hash from passwords inner join site on site_id = site.id where site_id = %s"
            data = (site_id,)
            query = self.execute_sql(sql=sql,data=data,fetchall=True)
            query_data = []
            for site_name,username,password_hash in query:
                query_data.append((site_name,username,self._decrypt_password(password_hash)))

            return query_data
        except IndexError:
            print(f"{site_name} does not exists.")
            self.conn.rollback()
        except psycopg2.errors as e:
            print(f"Oops something went wrong. Errors: {e}")

    def get_all(self):
        try:
            sql = "select site_name, username, password_hash from passwords inner join site on site_id = site.id"
            query = self.execute_sql(sql=sql, fetchall=True)
            query_data = []
            for site_name,username,password_hash in query:
                query_data.append((site_name,username,self._decrypt_password(password_hash)))
            return query_data
        except psycopg2.errors as e:
            print(f"Oops something went wrong. Errors: {e}")

    def delete_password(self, site_name, username):
        try:
            site_id = self.get_site_id(site_name)[0][0]
            sql = "delete from passwords where site_id = %s and username = %s"
            data = (site_id, username)
            self.execute_sql(sql=sql, data=data, commit=True)
            print("Deleted successfully")
        except IndexError:
            print(f"{site_name} does not exists.")
            self.conn.rollback()
        except psycopg2.errors as e:
            print(f"Oops something went wrong. Errors: {e}")

    def close(self):
        self.conn.close()

    def execute_sql(self, sql, data=None, commit=None, fetchall=None):
        cursor = self.get_cursor()
        try:
            cursor.execute(sql, data)
            if commit:
                self.conn.commit()
            if fetchall:
                query = cursor.fetchall()
                return query
        except psycopg2.errors as e:
            print(f"Oops something went wrong. Errors: {e}")
