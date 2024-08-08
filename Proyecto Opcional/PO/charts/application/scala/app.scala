import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.SparkSession._
import org.elasticsearch.spark.sql
import org.elasticsearch.spark.sql._
import org.elasticsearch.spark._ 

sc.stop()
spark.stop()

val conf = new SparkConf()
var espass = System.getenv("ELASTIC_PASS")
conf.set("es.index.auto.create", "true")
conf.set("es.nodes", "http://ic4302-es-http:9200/")
conf.set("es.net.http.auth.user", "elastic")
conf.set("es.net.http.auth.pass", espass)
conf.set("es.port", "9200")
conf.set("es.nodes.wan.only", "true")


val sc = new SparkContext(conf)

val spark = SparkSession.builder.config(sc.getConf).getOrCreate()

val sqlcontext = new org.apache.spark.sql.SQLContext(sc)

val options = Map("es.read.field.as.array.include" -> "data")

val tmp_data = spark.read.json("/data")
tmp_data.createOrReplaceTempView("tmp")

tmp_data.printSchema

spark.sql("SELECT * FROM tmp").count
spark.sql("SELECT * FROM tmp").show(false)

spark.sql("SELECT split(split(msg, ' ')[0], ':')[0] AS hour, split(split(msg, ' ')[0], ':')[1] AS minute, split(split(msg, ' ')[0], ':')[2] AS second  FROM tmp").show(false)

spark.sql("SELECT split(split(msg, ' ')[0], ':')[0] AS hour, split(split(msg, ' ')[0], ':')[1] AS minute, split(split(msg, ' ')[0], ':')[2] AS second  FROM tmp").saveToEs("data")

