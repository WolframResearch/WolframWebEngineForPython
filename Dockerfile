FROM wolframresearch/wolframengine:latest

USER root

RUN apt-get update -y && \
  apt-get install -y python3 python3-pip

RUN pip3 install wolframclient

COPY . /tmp/build
RUN pip3 install /tmp/build && \
  rm -r /tmp/build && \
  chown -R wolframengine /srv

USER wolframengine
EXPOSE 18000

ENTRYPOINT ["/usr/bin/python3", "-m", "wolframwebengine", "--domain", "0.0.0.0"]
CMD ["/srv"]