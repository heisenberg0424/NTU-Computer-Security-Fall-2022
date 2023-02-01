FROM python:3.10

RUN pip3 install flask

COPY readflag.c /readflag.c
COPY flag /flag
RUN chmod 0400 /flag && chown root:root /flag
RUN chmod 0444 /readflag.c && gcc /readflag.c -o /readflag
RUN chown root:root /readflag && chmod 4555 /readflag


WORKDIR /app
COPY --chown=nobody:nogroup src .
RUN chown nobody:nogroup /app

USER nobody
CMD ["python3", "app.py"]
