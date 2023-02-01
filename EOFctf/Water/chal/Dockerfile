FROM ubuntu:latest

RUN apt-get update && apt-get install -y clang socat

COPY flag /flag
COPY chal.c /chal.c
COPY run.sh /run.sh
#RUN clang /chal.c -o /chal -no-pie -fno-stack-protector
COPY chal /chal

ENV ASAN_OPTIONS="detect_leaks=0"
CMD ["socat", "TCP-LISTEN:9000,fork,reuseaddr", "EXEC:/run.sh"]
