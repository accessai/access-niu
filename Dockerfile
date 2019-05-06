FROM python:3.6-slim

SHELL ["/bin/bash", "-c"]

RUN apt-get update -qq && \
  apt-get install -y --no-install-recommends && \
  build-essential  && \
  mkdir access-niu

ADD . /access-niu
WORKDIR /access-niu

RUN mkdir templates
RUN python setup.py sdist
RUN pip install dist/access-niu*

VOLUME ["templates"]

EXPOSE 8000

ENTRYPOINT ["access-niu"]

CMD ["help"]
