from db.db_connection import connect_db
import psycopg2


class PasswordManager:
    def __init__(self, db_name, db_user, db_pass, db_host, db_port):
        self.conn = connect_db(db_name, db_user, db_pass, db_host, db_port)

    def get_cursor(self):
        return self.conn.cursor()

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
            data = (site_id, username, password)
            cursor = self.get_cursor()
            cursor.execute(sql, data)
            self.conn.commit()

            print("Data insertion completed successfully.")
        except psycopg2.errors as e:
            print(f"Opps something went wrong during the insertion, errors{e}")

    def create_site_name(self, site_name):
        try:
            sql = "INSERT INTO site (site_name) VALUES (%s)"
            data = (site_name,)
            cursor = self.get_cursor()
            cursor.execute(sql, data)
            self.conn.commit()

        except psycopg2.errors as e:
            print(f"Opps something went wrong during the insertion, errors{e}")

    def update_site_name(self, site_name, new_site_name):
        try:
            sql = "update site set site_name=%s where site_name=%s"
            data = (new_site_name, site_name)
            cursor = self.get_cursor()
            cursor.execute(sql, data)
            self.conn.commit()
        except psycopg2.errors as e:
            print(f"Oops something went wrong. errors {e}")

        print("Site name is updated successfully.")

    def update_password(self, site_name, username, password):
        try:
            site_id = self.get_site_id(site_name)[0][0]
            sql = "update passwords set password_hash = %s where site_id = %s and username = %s"
            data = (password, site_id, username)
            cursor = self.get_cursor()
            cursor.execute(sql, data)
            self.conn.commit()
            print("Password updated_successfully")
        except IndexError:
            print(f"{site_name} does not exists.")
            self.conn.rollback()

    def update_username(self, site_name, username, new_username):
        try:
            site_id = self.get_site_id(site_name)[0][0]
            sql = "update passwords set username = %s where site_id = %s and username = %s"
            data = (new_username, site_id, username)
            cursor = self.get_cursor()
            cursor.execute(sql, data)
            self.conn.commit()
            print("username updated successfully.")
        except IndexError:
            print(f"{site_name} does not exists.")
            self.conn.rollback()
        except psycopg2.errors as e:
            print(f"Oops something went wrong. Errors: {e}")

    def get_site_id(self, site_name):
        try:
            cursor = self.get_cursor()
            sql = "select id from site where site_name=%s"
            data = (site_name,)
            cursor.execute(sql, data)
            query = cursor.fetchall()
            return query
        except psycopg2.errors as e:
            print(f"opps sth went wrong by returning site id. Errors: {e}")

    def get_password(self, site_name):
        try:
            site_id = self.get_site_id(site_name)[0][0]
            sql = "select site_name, username, password_hash from passwords inner join site on site_id = site.id where site_id = %s"
            data = (site_id,)
            cursor = self.get_cursor()
            cursor.execute(sql, data)
            query = cursor.fetchall()
            return query
        except IndexError:
            print(f"{site_name} does not exists.")
            self.conn.rollback()
        except psycopg2.errors as e:
            print(f"Oops something went wrong. Errors: {e}")

    def close(self):
        self.conn.close()
