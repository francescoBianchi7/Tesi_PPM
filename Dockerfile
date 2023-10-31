FROM ubuntu:latest
LABEL authors="bianc"

ENTRYPOINT ["top", "-b"]
FROM python:3.9
WORKDIR /Tesi

COPY ./requirements.txt /Tesi/requirements.txt
RUN pip install -r requirements.txt

COPY . /Tesi

CMD ["python","./app.py"]