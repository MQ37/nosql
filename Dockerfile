FROM alpine:latest
COPY ./webapp /webapp
COPY ./requirements.txt /requirements.txt

# Python3
RUN \
    apk add python3 && \
    apk add py3-pip
# Flask deps
RUN \
    pip3 install -r /requirements.txt

ENTRYPOINT flask --app webapp.flaskr run --host 0.0.0.0
EXPOSE 5000

