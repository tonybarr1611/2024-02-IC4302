import spark.implicits._
import java.nio.file.{Files, Paths}
import scala.collection.JavaConverters._
import org.apache.spark.SparkConf
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._
import org.elasticsearch.spark.sql._

val dateQuery = """
  SELECT *, 
         date_format(`message`.`indexed`.`date-time`, 'MM-dd-yyyy') AS `message.indexed.date`, 
         date_format(`message`.`created`.`date-time`, 'MM-dd-yyyy') AS `message.created.date`
  FROM tmp
"""

val authorQuery = """
  SELECT *,
    concat_ws(', ', 
      transform(`message`.`author`, author -> concat(author.`family`, ', ', author.`given`))
    ) AS `message.author_names`
  FROM tmp
"""

val conf = new SparkConf()
  .set("es.index.auto.create", "true")
  .set("es.nodes", System.getenv("ELASTIC_URL"))
  .set("es.net.http.auth.user", System.getenv("ELASTIC_USER"))
  .set("es.net.http.auth.pass", System.getenv("ELASTIC_PASS"))
  .set("es.port", "9200")
  .set("es.nodes.wan.only", "true")

// Initialize SparkSession and SparkContext once
val spark = SparkSession.builder.config(conf).appName("Spark Elastic Search Integration").getOrCreate()
val sc = spark.sparkContext
val sqlContext = spark.sqlContext

val dirPath = System.getenv("XPATH")
val jsonFiles = Files.list(Paths.get(dirPath)).iterator().asScala.filter(_.toString.endsWith(".json")).toList

jsonFiles.foreach { file =>
  try {
    // Read JSON file into a DataFrame
    val apiDF = spark.read.json(file.toString)
    apiDF.createOrReplaceTempView("tmp")

    // Run the queries
    val dateDF = spark.sql(dateQuery)
    dateDF.createOrReplaceTempView("tmp")
    val authorDF = spark.sql(authorQuery)
    authorDF.createOrReplaceTempView("tmp")

    // Placeholder for the third query
    val thirdQuery = """
      SELECT * FROM tmp
    """
    val thirdDF = spark.sql(thirdQuery)

    // Write the final DataFrame to Elasticsearch
    thirdDF.saveToEs("data")

    println(s"Successfully processed file: ${file.toString}")
    // Delete the file after processing
    Files.delete(Paths.get(file.toString))
  } catch {
    case e: Exception =>
      println(s"Error processing file: ${file.toString}")
      e.printStackTrace()
  }
}

// Stop SparkSession after processing all files
spark.stop()
