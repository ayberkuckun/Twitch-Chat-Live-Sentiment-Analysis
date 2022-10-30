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



print(f"Dummy Score: {sentimentAnalyzeSentence(['Dummy', 'Starting', 'Point'])} Model is Loaded.")

# os.environ['HADOOP_HOME'] = 'C://Users//altan//Desktop//winutils-master//hadoop-2.6.0'
# os.environ["JAVA_HOME"] = "C://Program Files//Java//jdk-19"
# os.environ["PYSPARK_PYTHON"] = "python"
spark_version = '3.3.1'
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-sql-kafka-0-10_2.12:{} test.py'.format(spark_version)
spark = (
    SparkSession.builder.appName("TwitchChatSentiment")
    .master("local[*]")
    .getOrCreate()
)
spark.sparkContext.setLogLevel('ERROR')

TWITCH_USERNAME_LIST = 'riotgames, hasanabi'

df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "localhost:9092") \
  .option("subscribe", TWITCH_USERNAME_LIST) \
  .option("startingOffsets", "latest") \
  .load()
print("CHECKPOINT - 1")

df = df.withColumn('message', my_udf('value'))
df = df.drop('value')
df = df.withColumn('sentiment_score', my_udf2('message'))

df = (df 
    .withWatermark("timestamp", "1 minute")
    .groupBy([F.window('timestamp', '2 minute', '1 minute')])
    .agg(
         {'sentiment_score': 'mean'}
    )
)

df = df \
    .filter(F.col("sentiment_score") != 0.0) \
    .writeStream \
    .outputMode('append') \
    .format('console') \
    .start().awaitTermination()

# .option('truncate', False) \
print("CHECKPOINT - 2")
