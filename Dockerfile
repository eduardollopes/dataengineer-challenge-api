FROM ubuntu:latest

WORKDIR /app

RUN apt-get update && \
    apt-get install -y openjdk-8-jdk wget python3 python3-pip

ARG SPARK_VERSION=3.4.2
ENV HADOOP_VERSION=3

RUN wget https://downloads.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
    tar -xvzf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
    mv spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} /usr/local/spark && \
    rm spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

ENV SPARK_HOME /usr/local/spark
ENV PATH $PATH:$SPARK_HOME/bin

COPY . .
RUN pip3 install --no-cache-dir -r requirements.txt

RUN rm -rf /app/data/*

CMD ["/usr/local/spark/bin/spark-submit", "--master", "local", "main.py"] && \
    cp /app/data/*.csv $PWD/data
