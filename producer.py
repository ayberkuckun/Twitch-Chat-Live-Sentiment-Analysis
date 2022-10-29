from confluent_kafka import Producer
import json
import time


def init_producer(ip='localhost', port=9092):
    socket_address = ip + ":" + str(port)
    producer = Producer({'bootstrap.servers': socket_address})
    print('[LOG] Producer initialized')
    return producer


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
        print('[Producer]', message)


def send_message(producer, msg):
    data = {
        'chat_content': msg}
    m = json.dumps(data)
    producer.poll(1)
    producer.produce('twitch_chat', m.encode('utf-8'), callback=receipt)
    producer.flush()


if __name__ == '__main__':
    chat_message = "Hello World!"
    producer = init_producer()
    send_message(producer, chat_message)
