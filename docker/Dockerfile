# This builds the binary inside an Alpine Linux container, which is small
# hadolint ignore=DL3007
FROM ghcr.io/opensafely-core/base-docker:latest as base

# we are going to use an apt cache on the host, so disable the default debian
# docker clean up that deletes that cache on every apt install
RUN rm -f /etc/apt/apt.conf.d/docker-clean

# install any additional system dependencies
COPY docker/dependencies.txt /tmp/dependencies.txt
RUN --mount=type=cache,target=/var/cache/apt \
    /root/docker-apt-install.sh /tmp/dependencies.txt
 
WORKDIR /
RUN wget -q -O honeytail https://honeycomb.io/download/honeytail/v1.6.0/honeytail-linux-amd64 && \
      echo 'ade48161cbf79173ed7e2e476a53c45d1c9962c3332f0774f8dca67a067e1e12  honeytail' | sha256sum -c && \
      chmod 755 ./honeytail

ENV HONEYCOMB_WRITE_KEY NULL
ENV DATASET NULL
# The target log file is mounted to this location when the container is run
ENV LOG_FILENAME /src/log_file.json

CMD [ "/bin/sh", "-c", \
            "[ $HONEYCOMB_WRITE_KEY = dummy-key ] && echo 'Dummy key found, nothing to do here.' || ./honeytail \
            --parser json \
            --writekey $HONEYCOMB_WRITE_KEY \
            --file $LOG_FILENAME \
            --dataset $DATASET \
            --backfill" ]

# finally, tag with build information. These will change regularly, therefore
# we do them as the last action.
ARG BUILD_DATE=unknown
LABEL org.opencontainers.image.created=$BUILD_DATE
ARG GITREF=unknown
LABEL org.opencontainers.image.revision=$GITREF
