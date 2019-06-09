import os
import json
import numpy as np
import pandas as pd

from joblib import dump, load
from random import random, randint

from sklearn.model_selection import *
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer

illnesses = ['anxiety', 'depression', 'ptsd']
csv1 = 'status/warning.csv'
csv2 = 'status/displacement.csv'
warn = pd.read_csv(csv1)
disp = pd.read_csv(csv2)
data = []
data_labels = []
for illness in illnesses:
    for i in range(len(warn)):
        for j in range(warn['participants'][i]):
            data.append('warn ' + warn['length_of_warning'][i])
            a = random()
            if a < warn[illness][i]:
                this_label = illness
            else:
                this_label = 'no symptoms'
            data_labels.append(this_label)
    for i in range(len(disp)):
        for j in range(disp['participants'][i]):
            data.append('disp ' + disp['duration (months)'][i])
            this_label = []
            a = random()
            if a < disp[illness][i]:
                this_label = illness
            else:
                this_label = 'no symptoms'
            data_labels.append(this_label)

    vectorizer = TfidfVectorizer(min_df=5, max_df=0.8, sublinear_tf=True,
                                 use_idf=True, decode_error='ignore', analyzer="word", lowercase=False)

    vect_data = vectorizer.fit_transform(data)
    vect_data_n = vect_data.toarray()
    enc = OneHotEncoder(categories='auto')
    enc.fit(vect_data_n)

    state = randint(1, 10000)
    X_train, X_test, y_train, y_test = train_test_split(
        vect_data_n, data_labels, train_size=0.8, random_state=state)
    illness_model = LogisticRegression()
    illness_model = illness_model.fit(X=X_train, y=y_train)

    dump(illness_model, 'illness_model_' + illness + '.joblib')


def check_illness_risks(new_data, illness_model):
    new_data = vectorizer.transform(new_data).toarray()
    new_labels = illness_model.predict(new_data)
    return [new_labels[i] for i in range(len(new_labels))]
