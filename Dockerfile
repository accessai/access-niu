FROM python:3.6-slim

RUN apt-get -qy update && apt-get -qy install build-essential && \
    rm -rf /var/cache/apt/* /var/lib/apt/lists/*

WORKDIR /access-niu

# layer caching since dependencies don't change much
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python setup.py install

VOLUME ["access-niu"]

EXPOSE 8000

CMD ["python -m access_niu"]
