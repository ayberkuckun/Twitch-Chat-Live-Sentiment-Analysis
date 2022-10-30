import matplotlib.pyplot as plt
from confluent_kafka import Consumer
import ast

c = Consumer({'bootstrap.servers': 'localhost:9092',
             'group.id': 'python-consumer', 'auto.offset.reset': 'earliest'})
print('[LOG] Consumer initialized')

print('Available topics to consume: ', c.list_topics().topics)
c.subscribe(['sentiment_scores'])


def receive_messages():
    """If there are no messages, wait. If an error occurs, display. Received messages are decoded to utf-8
    """
    counter = 0

    length = 5
    time_list = ["_"] * length
    value_list = [0] * length

    while True:
        msg = c.poll(1.0)  # timeout
        if msg is None:
            continue
        if msg.error():
            print('Error: {}'.format(msg.error()))
            continue
        data = msg.value().decode('utf-8')
        print(data)
        result_dict = ast.literal_eval(data)
        if counter < length:
            time_list[counter] = result_dict["window"]["end"][11:16]
            if counter > 0:
                value_list[counter] = 0.5 * value_list[counter - 1] + 0.5 * result_dict["value"]
            else:
                value_list[counter] = result_dict["value"]

            plt.bar(time_list, value_list, align='center')
            plt.title(f'{result_dict["topic"].capitalize()} Twitch Chat Sentiment Analysis')
            plt.xlabel("Time")
            plt.ylabel("Score")
            plt.show()

        else:
            time_list[:-1] = time_list[1:]
            value_list[:-1] = value_list[1:]

            time_list[-1] = result_dict["window"]["end"][11:16]
            value_list[-1] = 0.5 * value_list[-2] + 0.5 * result_dict["value"]
            plt.bar(time_list, value_list, align='center')
            plt.title(f'{result_dict["topic"].capitalize()} Twitch Chat Sentiment Analysis')
            plt.xlabel("Time")
            plt.ylabel("Score")
            plt.show()

        counter += 1
    c.close()


if __name__ == '__main__':
    receive_messages()
