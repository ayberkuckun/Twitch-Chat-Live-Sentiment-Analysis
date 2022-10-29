
package sparkstreaming

import java.util.HashMap
import org.apache.kafka.clients.consumer.ConsumerConfig
import org.apache.kafka.common.serialization.StringDeserializer
import org.apache.spark.SparkConf
import org.apache.spark.streaming._
import org.apache.spark.streaming.kafka010._
import org.apache.spark.storage.StorageLevel
import java.util.{Date, Properties}
import scala.util.Random

object KafkaSpark {
  def main(args: Array[String]) {

    //val kafkaParams = Map[String, String]("bootstrap.servers" -> "localhost:9092")
    val kafkaParams = Map[String, Object](
      ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG -> "localhost:9092",
      ConsumerConfig.GROUP_ID_CONFIG -> "kth",
      ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG -> classOf[StringDeserializer],
      ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG -> classOf[StringDeserializer])

    val sparkConf = new SparkConf().setAppName("KafkaWordCount").setMaster("local[2]")
    val ssc = new StreamingContext(sparkConf, Seconds(2))
    ssc.checkpoint("checkpoint")

    //val messages = KafkaUtils.createDirectStream[String, String](ssc, kafkaParams, Set("avg"))
    val messages = KafkaUtils.createDirectStream[String, String](
      ssc,
      LocationStrategies.PreferConsistent,
      ConsumerStrategies.Subscribe[String, String](Set("avg"), kafkaParams))

    val values = messages.map(_.value)
    val pairs = values.map(_.split(",")).map(x => (x(0), x(1).toInt))

    def mappingFunc(key: String, value: Option[Int], state: State[(Int, Double)]): (String, (Int, Double)) = {
      val newVal:Int = value.getOrElse(0)
      val (acc, oldVal) = state.getOption.getOrElse((0, 0.0))
      val avg = (acc + 1, (oldVal * acc + newVal) / (acc + 1))
      state.update(avg)
      (key, avg)
    }

    val stateDstream = pairs.mapWithState(StateSpec.function(mappingFunc _))
    stateDstream.print()

    ssc.start()
    ssc.awaitTermination()
  }
}





