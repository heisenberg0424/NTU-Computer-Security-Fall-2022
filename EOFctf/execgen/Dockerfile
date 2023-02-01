FROM ubuntu:22.04
MAINTAINER HexRabbit

RUN apt-get update && \
    echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections && \
    apt-get install -qy xinetd

RUN useradd -m chal
RUN chown -R root:root /home/chal
RUN chmod -R 755 /home/chal

CMD ["/usr/sbin/xinetd", "-dontfork"]
