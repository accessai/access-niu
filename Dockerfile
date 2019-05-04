FROM wrwrwr/flask-scipy

ADD . /access-niu
WORKDIR /access-niu
RUN pip install /access-niu

EXPOSE 8000

