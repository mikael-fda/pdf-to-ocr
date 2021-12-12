FROM python:3.8

COPY requirements.txt ./

RUN pip3 install -r requirements.txt

RUN pip3 install flask-restx==0.2.0
RUN pip3 install Flask==1.1.2

WORKDIR /app

COPY app/ /app/

ENTRYPOINT ["python3", "-m", "flask", "run", "--host", "0.0.0.0", "--port", "5000"]