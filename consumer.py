from confluent_kafka import Consumer

c = Consumer({'bootstrap.servers': 'localhost:9092',
             'group.id': 'python-consumer', 'auto.offset.reset': 'earliest'})
print('[LOG] Consumer initialized')

print('Available topics to consume: ', c.list_topics().topics)
c.subscribe(['sentiment_scores'])


def receive_messages():
    """If there are no messages, wait. If an error occurs, display. Received messages are decoded to utf-8
    """
    while True:
        msg = c.poll(1.0)  # timeout
        if msg is None:
            continue
        if msg.error():
            print('Error: {}'.format(msg.error()))
            continue
        data = msg.value().decode('utf-8')
        print(data)
    c.close()


if __name__ == '__main__':
    receive_messages()
