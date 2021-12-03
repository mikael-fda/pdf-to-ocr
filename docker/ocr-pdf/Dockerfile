FROM python:3.8

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

WORKDIR /app
COPY app/ /app

ENTRYPOINT ["python3", "-m", "rq.cli", "worker", "--url", "redis://redis", "ocr"]
