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

// Read all files from the directory
val dirPath = System.getenv("XPATH")
val jsonFiles = Files.list(Paths.get(dirPath)).iterator().asScala.filter(_.toString.endsWith(".json")).toList
println(s"Found ${jsonFiles.length} JSON files in the directory: $dirPath")

try {
  println(s"Processing file: ${dirPath}")
  val apiDF = spark.read.json(dirPath)
    // Read JSON file into a DataFrame
    // val apiDF = spark.read.json(file.toString)
    apiDF.createOrReplaceTempView("tmp")
    apiDF.printSchema
    println("Files read successfully")

    // Run the queries
    println("First query")
    val dateDF = spark.sql(dateQuery)
    dateDF.show(false)
    println("Second query")
    dateDF.createOrReplaceTempView("tmp")
    val authorDF = spark.sql(authorQuery)
    authorDF.show(false)
    authorDF.createOrReplaceTempView("tmp")

    // Third query
  
    // println("Third query")
    // val titleDF = spark.sql("SELECT `message`.`DOI`, `message`.`title` FROM tmp")
    // println("Title DataFrame")
    // titleDF.show(false)

    println("Result dataframe")

    var result = authorDF.withColumn("message.reference_title", 
      coalesce(
        when(col("`message`.`reference`").isNotNull, 
          expr("filter(transform(`message`.`reference`, x -> coalesce(x.DOI, null)), x -> x is not null)")
        ),
        lit(null)
      )
    )
    
    result.show(false)
        
    var standardizedDF = result
    try{
      standardizedDF = result.withColumn("message.assertion.value", col("message.assertion.value").cast("string"))
    } catch {
      case e: Exception =>
        println("Did not require assertion")
    }
    println("Standardized DataFrame")
    standardizedDF.show(false)

    // Write the final DataFrame to Elasticsearch
    standardizedDF.saveToEs("data")
} catch {
  case e: org.apache.spark.sql.catalyst.parser.ParseException =>
    println(s"JSON parsing error in file: ${dirPath}")
    e.printStackTrace()
  case e: org.apache.spark.sql.AnalysisException =>
    println(s"Schema mismatch error in file: ${dirPath}")
    e.printStackTrace()
  case e: Exception =>
    println(s"Error processing file: ${dirPath}")
    e.printStackTrace()
}

// Delete all JSON files after processing
jsonFiles.foreach { file =>
  try {
    Files.delete(file)
  } catch {
    case e: Exception =>
      println(s"Error deleting file: ${file}")
      e.printStackTrace()
  }
}

// Stop SparkSession after processing all files
spark.stop()
println("SparkSession stopped successfully")
