FROM python:3.6-slim as builder
RUN python3 -m venv /venv

#SHELL ["/bin/bash", "-c"]


RUN apt-get -qy update && apt-get -qy install build-essential && \
    rm -rf /var/cache/apt/* /var/lib/apt/lists/*

WORKDIR /build

# layer caching since dependencies don't change much
COPY requirements.txt .
RUN /venv/bin/pip install -r requirements.txt

COPY . /build
RUN /venv/bin/pip install /build

RUN ls /venv
RUN pwd
#RUN pip install --user .

FROM python:3.6-alpine3.9 AS release
COPY --from=builder /venv /usr/local

WORKDIR /app


#ENV PATH=/root/.local/bin:$PATH

VOLUME ["templates"]

EXPOSE 8000

#ENTRYPOINT ["access-niu"]

#CMD ["help"]
