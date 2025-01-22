FROM ghcr.io/seravo/ubuntu:noble

ARG APT_PROXY

RUN sed -i 's/main$/main universe/g' /etc/apt/sources.list && \
    apt-setup && \
    apt-get --assume-yes install \
      yamllint && \
    apt-cleanup

RUN useradd user && \
    mkdir -p /workdir

USER user

WORKDIR /workdir

ENTRYPOINT ["/usr/bin/yamllint"]
CMD ["-f", "github"]
