import time
import psycopg2
import psycopg2.extras
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self) -> None:
        self.hostname = os.getenv('HOSTNAME')
        self.database = os.getenv('DATABASE_1')
        self.username = os.getenv('USERNAME_1')
        self.pwd = os.getenv('PASSWORD_1')
        self.port_id = 5432
        self.conn = None

    def insert_data(self, table_name, create_script, insert_script, insert_values):
        try:
            with psycopg2.connect(
                        host = self.hostname,
                        dbname = self.database,
                        user = self.username,
                        password = self.pwd,
                        port = self.port_id) as conn:

                with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:

                    cur.execute(f'DROP TABLE IF EXISTS {table_name}')
                    cur.execute(create_script)
                    for record in insert_values:
                        cur.execute(insert_script, record)
                    conn.commit()

                    cur.execute(f'SELECT * FROM {table_name}')
                    print(cur.fetchall())

        except Exception as error:
            print(error, "error")
        finally:
            if conn is not None:
                conn.close()


