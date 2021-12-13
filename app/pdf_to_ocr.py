import os
import psycopg2
import subprocess

from common import Globals


OCR_COMMANDS = "ocrmypdf -j 1 --skip-text --output-type pdf".split()


def get_data(user_id):
    conn = None
    sql = """SELECT path FROM Files WHERE user_id = %d;"""
    data = []
    try:
        conn = psycopg2.connect(
            host=os.environ['HOSTNAME'],
            database=os.environ['POSTGRES_DB'],
            user=os.environ['POSTGRES_USER'],
            password=os.environ['POSTGRES_PASSWORD']
        )
        
        # create a cursor
        cur = conn.cursor()
        # execute a statement
        cur.execute(sql, (user_id))
        # commit change
        conn.commit()

        # get Data
        data = cur.fetchall()

        # close communcation
        cur.close()
    except Exception as e:
        print(e)
    finally:
        if conn is not None:
            conn.close()
        return data

def insert_data(user_id, output_file, status):
    conn = None
    sql = """INSERT INTO Files(user_id, path, status)
             AVLUES(%d, %s, %d);"""
    try:
        conn = psycopg2.connect(
            host=os.environ['HOSTNAME'],
            database=os.environ['POSTGRES_DB'],
            user=os.environ['POSTGRES_USER'],
            password=os.environ['POSTGRES_PASSWORD']
        )
        
        # create a cursor
        cur = conn.cursor()
        # execute a statement
        cur.execute(sql, (user_id, output_file, status))
        # commit change
        conn.commit()
        # close communcation
        cur.close()
    except Exception as e:
        print(e)
    finally:
        if conn is not None:
            conn.close()

def pdf_to_ocr(user_id, input_file, lang="-l fra"):
    output_file = input_file.replace(Globals.INPUT_FOLDER, Globals.OUTPUT_FOLDER)

    cmd = OCR_COMMANDS +  lang.split() + [input_file, output_file]

    return_status = None
    try:
        subprocess.check_call(cmd)
        return_status = 0
    except subprocess.CalledProcessError as e:
        return_status = e.returncode
    # insert_data(user_id, output_file, return_status)
