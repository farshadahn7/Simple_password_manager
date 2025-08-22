from db.db_connection import connect_db
from decouple import config
import psycopg2

db_connection_data = {
    "db_name":config("DB_NAME"),
    "db_user":config("DB_USER"),
    "db_pass":config("DB_PASS"),
    "db_host":config("DB_HOST"),
    "db_port":config("DB_PORT")
}


if __name__ == "__main__":
    conn = connect_db(**db_connection_data)
    cursor = conn.cursor()
    while True:
        user_ans = input("Type 1 for insert password otherwise type 2 for retrieve or n for end the process:")
        if user_ans.lower() not in ('1','2', 'n'):
            print("Wrong input. try again.")
            continue
        elif user_ans == '1':
            site_name = input("please enter the site name:")
            username = input("please enter the username:")
            password = input("please enter the password:")
            sql = "INSERT INTO passwords (site_name, username, password_hash) VALUES (%s,%s,%s)"
            data = (site_name, username,password)
            try:
                cursor.execute(sql, data)
                conn.commit()
            except psycopg2.errors as e:
                print(f"Error Inserting to database: {e}")
        elif user_ans == '2':
            site_name = input("Tell me the site_name:")
            sql = "SELECT * FROM passwords WHERE site_name = %s"
            data = (site_name,)
            cursor.execute(sql, data)
            query = cursor.fetchall()
            print(query)
        elif user_ans.lower() == 'n':
            cursor.close()
            conn.close()
            break