import os
import psycopg2
import subprocess
from sql import insert_file
from common import Globals

OCR_COMMANDS = "ocrmypdf -q -j 1 --skip-text --output-type pdf".split()


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
