FROM python:stretch

COPY . /app
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip
#RUN pip install flask
RUN pip install -r requirements.txt

ENTRYPOINT ["gunicorn","-b",":8080", "main:APP"]

