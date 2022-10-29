import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

list_scores=[0]
list_seconds=[0]

def update(new_score):
    running_average = list_scores[-1] * 0.75 + new_score * 0.25
    list_scores.append(running_average)
    list_seconds.append(list_seconds[-1]+1)

def visualize():
    plt.plot(list_seconds,list_scores)
    plt.xlabel('Message Count')
    plt.ylabel('Twitch Chat Sentiment')
    plt.title("Sentiment Graph")
    plt.show()