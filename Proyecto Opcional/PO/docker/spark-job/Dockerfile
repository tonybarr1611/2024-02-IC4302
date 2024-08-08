FROM spark:3.5.1-scala2.12-java11-ubuntu
# https://stackoverflow.com/questions/27717379/spark-how-to-run-spark-file-from-spark-shell

WORKDIR /app

COPY app/app.scala .
COPY app/elasticsearch-spark-30_2.12-8.14.3.jar /opt/spark/jars/

#CMD [ "tail", "-f", "/dev/null" ]
CMD ["ls", "-l", "/tmp"]