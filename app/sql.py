import psycopg2
import os
from errors import DatabaseError, ObjectNotFound

HOST = os.environ['HOSTNAME']
DB = os.environ['POSTGRES_DB']
USER = os.environ['POSTGRES_USER']
PASS = os.environ['POSTGRES_PASSWORD']

def make_select(sql_cmd, parameters=None):
    """ query parts from the parts table """
    create_tables()
    conn = None
    data = None
    try:
        conn = psycopg2.connect(
            host=HOST,
            database=DB,
            user=USER,
            password=PASS
        )        
        cur = conn.cursor()
        cur.execute(sql_cmd, (parameters,))
        rows = cur.fetchall()
        data =  [ row for row in rows]
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        raise DatabaseError("Error during SELECT in database : " + str(error))
    finally:
        if conn is not None:
            conn.close()
    if not data:
        raise ObjectNotFound("No data corresponding in the database")
    return data

def make_insert(sql_cmd, parameters=None):
    """ insert a new vendor into the vendors table """
    create_tables()
    conn = None
    id = None
    try:
        conn = psycopg2.connect(
            host=HOST,
            database=DB,
            user=USER,
            password=PASS
        )        
        cur = conn.cursor()
        cur.execute(sql_cmd, parameters,)
        id = cur.fetchone()[0]
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        raise DatabaseError("Error during INSERT in database : " + str(error))
    finally:
        if conn is not None:
            conn.close()
    return id

def insert_file(user_name, input_file, output_file, return_status):
    commands = (
        """INSERT INTO file(user_name, input_file, output_file, return_status) 
            VALUES(%s, %s, %s, %s) RETURNING file_id;
        """
    )
    parameters = (user_name, input_file, output_file, return_status)
    return make_insert(commands, parameters)

def insert_user(user_name, user_mail):
    commands = (
        """INSERT INTO user_pdf(user_name, user_mail)
            VALUES(%s, %s) RETURNING user_name;
        """
    )
    parameters = (user_name, user_mail)
    return make_insert(commands, parameters)

def get_user(user_name):
    commands = (
        """SELECT * FROM user_pdf 
            WHERE user_name = %s;
        """
    )
    parameters = (user_name)
    return make_select(commands, parameters)

def get_file(user_name):
    commands = (
        """SELECT * FROM file 
            WHERE user_name = %s;
        """
    )
    parameters = (user_name)
    return make_select(commands, parameters)

def create_tables():
    """ create tables in the PostgreSQL database"""
    sql_cmd = (
        """
        CREATE TABLE IF NOT EXISTS user_pdf (
            user_name VARCHAR(255) PRIMARY KEY,
            user_mail VARCHAR(255) NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS file (
                file_id SERIAL PRIMARY KEY ,
                user_name VARCHAR(255) NOT NULL ,
                input_file VARCHAR(255) NOT NULL,
                output_file VARCHAR(255) NOT NULL,
                return_status INTEGER NOT NULL,
                FOREIGN KEY (user_name)
                    REFERENCES user_pdf (user_name)
        );
        """)
    try : 
        conn = psycopg2.connect(
            host=HOST,
            database=DB,
            user=USER,
            password=PASS
        )
        cur = conn.cursor()
        for cmd in sql_cmd:
            cur.execute(cmd)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        raise DatabaseError("Error during TABLE CREATION : " + str(error))
    finally:
        if conn is not None:
            conn.close()