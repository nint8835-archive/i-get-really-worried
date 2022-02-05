FROM python:3.9-slim-bullseye

RUN apt-get -y update && \
    apt-get install -y --fix-missing \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev && \
    apt-get clean && \
    rm -rf /tmp/* /var/tmp/*

WORKDIR /bot
COPY . /bot
RUN pip install -r requirements.txt

CMD [ "python", "bot.py" ]
