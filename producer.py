from confluent_kafka import Producer
import json
import time


producer = Producer({'bootstrap.servers': 'localhost:9092'})
print('[LOG] Producer initialized')


def receipt(err, msg):
    """Used to acknowleding new messages or errors. Valid messages will be decoded to utf-8 & printed

    Args:
        err (_type_): _description_
        msg (_type_): _description_
    """
    if err is not None:
        print('Error: {}'.format(err))
    else:
        message = 'Topic: {} / Value: {}\n'.format(
            msg.topic(), msg.value().decode('utf-8'))
        # logger.info(message)
        print(message)


def send_messages():
    chat_message = "Hello World!"
    for i in range(100):
        data = {
            'chat_content': chat_message + ' ' + str(i)}
        m = json.dumps(data)
        producer.poll(1)
        producer.produce('twitch_chat', m.encode('utf-8'), callback=receipt)
        producer.flush()
        time.sleep(3)


if __name__ == '__main__':
    send_messages()
