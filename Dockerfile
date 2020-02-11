FROM python:3.7-alpine AS pycep

WORKDIR /opt/pycep

COPY . /tmp/pycep

RUN apk update \
   && apk upgrade \
   &&  apk add --no-cache -t build_req \
        gcc \
        g++ \
   && adduser -DH -s /sbin/nologin pycep \
   && chown -R pycep:pycep /opt/pycep \
   && cd /tmp/pycep/ \
   && export PIP_NO_CACHE_DIR=off \
   && export PIP_DISABLE_PIP_VERSION_CHECK=on \
   && pip install -r requirements.txt \
   && python setup.py install \
   && rm -rf /tmp/pycep \
   && apk del --purge build_req

VOLUME ["/opt/pycep"]
USER pycep
ENTRYPOINT ["cepcli.py"]
CMD ["--help"]
