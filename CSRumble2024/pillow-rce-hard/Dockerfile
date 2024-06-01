FROM python:3.12-slim@sha256:5dc6f84b5e97bfb0c90abfb7c55f3cacc2cb6687c8f920b64a833a2219875997

RUN apt-get update && apt-get install -y socat
RUN useradd -UM chall
RUN pip install pillow==10.2.0

COPY . /app
RUN chmod 0400 /app/flag.txt && chmod 4755 /app/flag_dispenser

WORKDIR /app

CMD /app/socat.sh
