import os
import psycopg2
import subprocess
from sql import insert_file
from common import Globals
from redis import Redis
from rq import Queue

OCR_COMMANDS = "ocrmypdf -j 1 --skip-text --output-type pdf".split()


def pdf_to_ocr(user_name, input_file, lang="-l fra"):
    output_file = input_file.replace(Globals.INPUT_FOLDER, Globals.OUTPUT_FOLDER)

    cmd = OCR_COMMANDS +  lang.split() + [input_file, output_file]

    return_status = None
    try:
        subprocess.check_call(cmd)
        return_status = 0
    except subprocess.CalledProcessError as e:
        return_status = e.returncode
    insert_file(user_name, input_file, output_file, return_status)

redis = Redis(host="redis")
queue = Queue(name="ocr", connection=redis)

def redis_pdf_to_ocr(user_name, input_file):
    queue.enqueue(pdf_to_ocr, args=(user_name, input_file, "-l fra"))