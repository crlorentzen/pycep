FROM python:3.8.3-alpine3.12

WORKDIR /opt/pycep

COPY . /tmp/pycep

RUN apk update
RUN apk upgrade && apk add libstdc++
RUN  apk add --no-cache -t build_req \
        gcc \
        g++ \
        tiff-dev \
        jpeg-dev \
        openjpeg \
        zlib-dev \
        freetype-dev \
        lcms2-dev \
        libwebp-dev \
        tcl-dev \
        harfbuzz-dev \
        python3-dev \
        zlib  \
        harfbuzz \
   && adduser -DH -s /sbin/nologin pycep \
   && chown -R pycep:pycep /opt/pycep \
   && cd /tmp/pycep/ \
   && export PIP_NO_CACHE_DIR=off \
   && export PIP_DISABLE_PIP_VERSION_CHECK=on \
   && pip install --upgrade pip \
   && pip install setuptools \
   && pip install wheel \
   && pip install -r requirements.txt \
   && python setup.py install \
   && rm -rf /tmp/pycep \
   && apk del --purge build_req

VOLUME ["/opt/pycep"]
USER pycep
ENTRYPOINT ["cepcli.py"]
CMD ["--help"]
