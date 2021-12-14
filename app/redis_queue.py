from redis import Redis
from rq import Queue
from pdf_to_ocr import pdf_to_ocr

redis = Redis(host="redis")
queue = Queue(name="ocr", connection=redis)

def redis_pdf_to_ocr(user_name, input_file):
    queue.enqueue(pdf_to_ocr, args=(user_name, input_file, "-l fra"))