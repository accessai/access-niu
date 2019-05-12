FROM python:3.6 as base

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt


# --- Release with Alpine ----
FROM python:3.6-alpine AS release
# Create app directory
WORKDIR /app

COPY --from=base /app/requirements.txt ./
COPY --from=base /root/.cache /root/.cache

# Install app dependencies
RUN pip install -r requirements.txt
COPY --from=base /app/ ./
#CMD ["gunicorn", "--config", "./gunicorn_app/conf/gunicorn_config.py", "gunicorn_app:app"]



#SHELL ["/bin/bash", "-c"]

#RUN apt-get update -qq && \
#  apt-get install -y --no-install-recommends && \
#  build-essential  && \
#  mkdir access-niu

# ADD . /access-niu
# WORKDIR /access-niu

# RUN mkdir templates
#RUN python setup.py sdist
#RUN pip install dist/access-niu*

#VOLUME ["templates"]

#EXPOSE 8000

#ENTRYPOINT ["access-niu"]

#CMD ["help"]
