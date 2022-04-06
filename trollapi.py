from flask import *
import re
import nltk
from nltk.corpus import stopwords
import tensorflow as tf
from keras.preprocessing.text import Tokenizer
from sklearn.ensemble import RandomForestClassifier
import pickle
import joblib
import numpy as np
from nltk.stem import WordNetLemmatizer


def preprocess_text(sen):
    # lower the character
    sentence = sen.lower()

    # Remove punctuations and numbers
    sentence = re.sub('[^a-zA-Z]', ' ', sentence)

    # Single character removal
    sentence = re.sub(r"\s+[a-zA-Z]\s+", ' ', sentence)

    # Removing multiple spaces
    sentence = re.sub(r'\s+', ' ', sentence)

    stops = stopwords.words('english')

    for word in sentence.split():
        if word in stops:
            sentence = sentence.replace(word, '')

    sentence = re.sub(r"http\S+", "", sentence)
    lemmatizer = WordNetLemmatizer()
    for word in sentence.split():
        sentence = sentence.replace(word, lemmatizer.lemmatize(word))
    del(lemmatizer)

    return sentence


def padzero(lst):
    for i in range(250 - len(lst)):
        lst.insert(0, 0)

def id(val):
    if val==0:
        return 'it is not troll'
    else:
        return 'it is troll'
app = Flask(__name__)
app.secret_key = 'error123'
@app.route('/istroll', methods=['GET'])
def troll():
    if request.method == 'GET':
        with open('tokenizer.pickle', 'rb') as handle:
            tokenizer = pickle.load(handle)

        loaded_rf = joblib.load("random_forest.joblib")
        text=request.args.get('comment')
        text4=text
        text4=preprocess_text(text4)
        text2 = text4

        text4 = tokenizer.texts_to_sequences([text4])
        padzero(text4[0])
        var = loaded_rf.predict(text4)

        dic = {
            'comment': text,
            'istroll':int(var[0]),
            'troll': id(var[0])
        }
        return jsonify(dic)


if __name__ == '__main__':
    app.run(debug=True)