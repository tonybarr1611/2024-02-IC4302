FROM apache/spark:3.4.3-scala2.12-java11-python3-r-ubuntu
# https://stackoverflow.com/questions/27717379/spark-how-to-run-spark-file-from-spark-shell

WORKDIR /opt/spark/work-dir

COPY app/app.scala .
COPY app/elasticsearch-spark-30_2.12-8.14.3.jar /opt/spark/jars/

CMD [ "tail", "-f", "/dev/null" ]
# CMD ["ls", "-l", "/tmp"]
CMD ["/opt/spark/bin/spark-shell", "--jars", "/opt/spark/jars/elasticsearch-spark-30_2.12-8.14.3.jar", "-i", "app.scala"]