FROM ubuntu:latest

WORKDIR /app

RUN apt-get update && \
    apt-get install -y openjdk-8-jdk wget python3 python3-pip

RUN wget https://downloads.apache.org/spark/spark-3.2.0/spark-3.2.0-bin-hadoop2.7.tgz && \
    tar -xvzf spark-3.2.0-bin-hadoop2.7.tgz && \
    mv spark-3.2.0-bin-hadoop2.7 /usr/local/spark && \
    rm spark-3.2.0-bin-hadoop2.7.tgz

ENV SPARK_HOME /usr/local/spark
ENV PATH $PATH:$SPARK_HOME/bin

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["/usr/local/spark/bin/spark-submit", "--master", "local", "main.py"]
