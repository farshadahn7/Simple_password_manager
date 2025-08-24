from cryptography.fernet import Fernet
from db.db_connection import connect_db
from settings import db_connection_data

def get_key():
    conn = connect_db(**db_connection_data)
    sql = "select my_key from mykey"
    cursor = conn.cursor()
    cursor.execute(sql)
    query = cursor.fetchall()
    if query:
        return query[0][0].encode("utf-8")
    else:
        my_key = Fernet.generate_key()
        sql = "Insert into mykey (my_key) values (%s)"
        cursor.execute(sql,(my_key.decode('utf-8'),))
        conn.commit()
        conn.close()
        cursor.close()
        return my_key



