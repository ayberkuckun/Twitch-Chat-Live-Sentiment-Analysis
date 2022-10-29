import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import words
from nltk.metrics.distance import jaccard_distance
from nltk.util import ngrams

nltk.download('omw-1.4')
nltk.download('punkt')
nltk.download('words')

correct_words = words.words()

text = 'happppppy azmaing intelliengt helpppppp GayPride'


def correct_string(text):
    """Function to correct spelling of a given string. We aim to correct words like caaaar -> car, or amaizng -> amazing

    Args:
        text (String): Input String

    Returns:
        String: Corrected String
    """
    tokens_incorrect = nltk.word_tokenize(text)

    correct_tokens = []
    for word in tokens_incorrect:
        # Based on jaccard distance find correct spellings (e.g. caaaaar -> car, amainzg -> amazing)
        temp = [(jaccard_distance(set(ngrams(word, 2)),
                                  set(ngrams(w, 2))), w)
                for w in correct_words if w[0] == word[0]]
        corrected_word = sorted(
            temp, key=lambda val: val[0])[0][1]
        correct_tokens.append(corrected_word)

    wn_model = WordNetLemmatizer()
    out_string = ''
    for w in correct_tokens:
        out_string += wn_model.lemmatize(w) + ' '
        # print("{} --> {}".format(w, wn_model.lemmatize(w)))
    return out_string


correct_string = correct_string(text)
print('Input:', text)
print('Output', correct_string)
