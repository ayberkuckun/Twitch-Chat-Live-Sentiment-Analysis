from pyspark.sql import SparkSession
import os
import pyspark.sql.functions as F
import pyspark.sql.types as T
from sentiment import sentimentAnalyzeSentence


def byteToString(byte):
    return (byte.decode('utf-8', errors="replace")[18:])[:-2]


# if we assume that my_func returns a string
my_udf = F.UserDefinedFunction(byteToString, T.StringType())
my_udf2 = F.UserDefinedFunction(sentimentAnalyzeSentence, T.DoubleType())

spark_version = '3.3.1'
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-sql-kafka-0-10_2.12:{} analyzer.py'.format(
    spark_version)
spark = (
    SparkSession.builder.appName("TwitchChatSentiment")
    .master("local[*]")
    .getOrCreate()
)
spark.conf.set("spark.sql.streaming.checkpointLocation", "checkpoint/")
spark.sparkContext.setLogLevel('ERROR')

TWITCH_USERNAME_LIST = 'redbull'

df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", TWITCH_USERNAME_LIST) \
    .option("startingOffsets", "latest") \
    .load()

df = df.withColumn('message', my_udf('value'))
df = df.drop('value')
df = df.withColumn('sentiment_score', my_udf2('message'))
df = df.filter(F.col("sentiment_score") != 0.0)

df = (df
      .withWatermark("timestamp", "1 minute")
      .groupBy(F.window('timestamp', '2 minute', '1 minute'),
               df.topic
               )
      .agg(F.mean('sentiment_score').alias('value')
           )
      )

df = (df.select(F.to_json(F.struct([F.col(c).alias(c) for c in df.columns]).alias("value")).alias("value")).alias("value")
      .selectExpr("CAST(value AS STRING)")
      .writeStream
      .format("kafka")
      .option("kafka.bootstrap.servers", "localhost:9092")
      .option("topic", "sentiment_scores")
      .start().awaitTermination()
      )
