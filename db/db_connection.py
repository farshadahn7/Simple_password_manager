import psycopg2


def connect_db(db_name,db_user, db_pass, db_host,db_port):
    try:
        connection = psycopg2.connect(
            database= db_name,
            user=db_user,
            password=db_pass,
            host=db_host,
            port=db_port
        )
        print("Db connected")
        return connection
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
