println("Starting the Spark job...")

import java.nio.file.{Files, Paths}
import scala.jdk.CollectionConverters._
import org.apache.spark.SparkConf
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._
import org.elasticsearch.spark.sql._

SparkSession.builder().getOrCreate().stop()

// Initialize SparkSession and SparkContext first
val conf = new SparkConf()
  .setAppName("Spark Elastic Search Integration")
  .set("es.index.auto.create", "true")
  .set("es.nodes", "http://ic4302-es-http:9200/")
  .set("es.net.http.auth.user", System.getenv("ELASTIC_USER"))
  .set("es.net.http.auth.pass", System.getenv("ELASTIC_PASS"))
  .set("es.port", "9200")
  .set("es.nodes.wan.only", "true")

val spark = SparkSession.builder.config(conf).getOrCreate()
println("SparkSession initialized successfully")

// Import spark.implicits._ after SparkSession is created
import spark.implicits._

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

val dirPath = System.getenv("XPATH")
val jsonFiles = Files.list(Paths.get(dirPath)).iterator().asScala.filter(_.toString.endsWith(".json")).toList
println(s"Found ${jsonFiles.length} JSON files in the directory: $dirPath")

jsonFiles.foreach { file =>
  try {
    val jsonContent = Files.readString(Paths.get(file.toString))
    val jsonOneLine = jsonContent.replaceAll("\n", "").replaceAll("\r", "")
    val apiDF = spark.read.json(Seq(jsonOneLine).toDS)
    // Read JSON file into a DataFrame
    // val apiDF = spark.read.json(file.toString)
    apiDF.createOrReplaceTempView("tmp")

    // Run the queries
    val dateDF = spark.sql(dateQuery)
    dateDF.show(false)
    dateDF.createOrReplaceTempView("tmp")
    val authorDF = spark.sql(authorQuery)
    authorDF.show(false)
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
    case e: org.apache.spark.sql.catalyst.parser.ParseException =>
      println(s"JSON parsing error in file: ${file.toString}")
      e.printStackTrace()
    case e: org.apache.spark.sql.AnalysisException =>
      println(s"Schema mismatch error in file: ${file.toString}")
      e.printStackTrace()
    case e: Exception =>
      println(s"Error processing file: ${file.toString}")
      e.printStackTrace()
  }
}

// Stop SparkSession after processing all files
spark.stop()
println("SparkSession stopped successfully")
