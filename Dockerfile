FROM python:3.6-slim as builder

RUN python3 -m venv /venv

RUN apt-get -qy update && apt-get -qy install build-essential && \
    rm -rf /var/cache/apt/* /var/lib/apt/lists/*

WORKDIR /build

# layer caching since dependencies don't change much
COPY requirements.txt .
RUN /venv/bin/pip install -r requirements.txt

COPY . /build
RUN /venv/bin/pip install /build

FROM python:3.6-alpine3.9 AS release
COPY --from=builder /venv /usr/local

WORKDIR /app

VOLUME ["templates"]

EXPOSE 8000

ENTRYPOINT ["access_niu"]

CMD ["help"]
