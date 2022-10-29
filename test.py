from pyspark.sql import SparkSession
import os
# os.environ['HADOOP_HOME'] = 'C://Users//altan//Desktop//winutils-master//hadoop-2.6.0'
os.environ["JAVA_HOME"] = "C://Program Files//Java//jdk-19"
os.environ["PYSPARK_PYTHON"] = "python"
spark_version = '3.3.1'
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-sql-kafka-0-10_2.12:{} test.py'.format(spark_version)
spark = (
    SparkSession.builder.appName("TwitchChatSentiment")
    .master("local[*]")
    .getOrCreate()
)
spark.sparkContext.setLogLevel('WARN')

df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "localhost:9092") \
  .option("subscribe", "twitch_chat") \
  .option("startingOffsets", "earliest") \
  .load()
print("CHECKPOINT - 1")
df = df \
    .writeStream \
    .outputMode('append') \
    .format('console') \
    .start().awaitTermination()
print("CHECKPOINT - 2")
