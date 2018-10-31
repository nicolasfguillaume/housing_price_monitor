FROM joyzoursky/python-chromedriver:3.6-alpine3.7-selenium

RUN apk add --no-cache \
            --allow-untrusted \
            --repository \
             http://dl-3.alpinelinux.org/alpine/edge/testing \
            hdf5 \
            hdf5-dev && \
    apk add --no-cache \
        build-base

# RUN pip install --no-cache-dir --no-binary :all: tables pandas numpy
RUN pip install --no-binary :all: tables pandas numpy

# ADD runs only if the referenced file changed since the last time it was executed
ADD requirements.txt /usr/workspace/requirements.txt
RUN pip install -r /usr/workspace/requirements.txt

RUN apk --no-cache del build-base

# COPY . /usr/workspace/

WORKDIR /usr/workspace/
