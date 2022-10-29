from kafka import KafkaConsumer
from kafka import TopicPartition
consumer = KafkaConsumer(bootstrap_servers='localhost:1234')
consumer.assign([TopicPartition('', 2)])
msg = next(consumer)
