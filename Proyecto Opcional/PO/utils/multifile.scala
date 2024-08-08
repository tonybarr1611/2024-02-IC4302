// https://stackoverflow.com/questions/21964709/how-to-set-or-change-the-default-java-jdk-version-on-macos
//export JAVA_HOME=$(/usr/libexec/java_home -v 1.8)
val data = spark.read.option("delimiter", ",").option("header", true).csv("/Users/nereo/Documents/TEC/02/articles/*.csv")