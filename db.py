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


    def insert_data(self, data):
        try:
            with psycopg2.connect(
                        host = self.hostname,
                        dbname = self.database,
                        user = self.username,
                        password = self.pwd,
                        port = self.port_id) as conn:

                with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:

                    cur.execute('DROP TABLE IF EXISTS pinnacle')

                    create_script = ''' CREATE TABLE IF NOT EXISTS pinnacle (
                                            id      serial PRIMARY KEY,
                                            home    varchar(40) NOT NULL,
                                            away    varchar(40) NOT NULL,
                                            H       real NOT NULL,
                                            D       real NOT NULL,
                                            A       real NOT NULL) '''
                    cur.execute(create_script)

                    insert_script  = 'INSERT INTO pinnacle (home, away, H, D, A) VALUES (%s, %s, %s, %s, %s)'
                    # print(data)
                    insert_values = []
                    for match in data:
                        insert_values.append((match['home_team'], match['away_team'], match['H'], match['D'], match['A']))
                    for record in insert_values:
                        cur.execute(insert_script, record)
                    conn.commit()


                    cur.execute('SELECT * FROM pinnacle')
                    print(cur.fetchall())
                    
        except Exception as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()


