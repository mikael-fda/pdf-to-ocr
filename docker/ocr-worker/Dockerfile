# https://hub.docker.com/r/jbarlow83/ocrmypdf/dockerfile
FROM jbarlow83/ocrmypdf

COPY requirements.txt ./
RUN apt update && \
    apt install -y python3-distutils && \
    pip3 install -r requirements.txt 

WORKDIR /app
COPY app/sql.py app/pdf_to_ocr.py app/common.py /app/

ENTRYPOINT ["python3", "-m", "rq.cli", "worker", "--url", "redis://redis", "ocr"]
