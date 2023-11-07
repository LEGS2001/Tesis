from sentence_transformers import SentenceTransformer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn import metrics

import pandas as pd
import numpy as np
import spacy
import string
import pickle


model = SentenceTransformer('all-MiniLM-L6-v2')
data = pd.read_csv("dataset.csv", on_bad_lines='skip', engine="python")
np.random.seed(2023)

nlp = spacy.load("es_core_news_md")
stop_words = nlp.Defaults.stop_words
puntuaciones = string.punctuation

def tokenizar(oracion):
    # convierte la oracion en un objeto procesable por la clase nlp de la libreria spacy
    oracion_nlp = nlp(oracion)
    # separa cada palabra de la oración en una lista y las lematiza
    tokens = [ word.lemma_.lower().strip() for word in oracion_nlp ]
    # elimina las "stop words" y las puntuaciones
    tokens = [ word for word in tokens if word not in stop_words and word not in puntuaciones ]
    # vuelve a convertir la lista en un string con cada palabra separada por un espacio
    oracion_lematizada = " ".join(tokens)
    return oracion_lematizada

print('Comenzando tokenización del dataset')
data['tokenize'] = data['text'].apply(tokenizar)
data['embeddings'] = data['tokenize'].apply(model.encode)
X = data['embeddings'].to_list()
y = data['label'].to_list()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,stratify=y)

print('Comenzando Regresión Logística')
LR = LogisticRegression()
LR.fit(X_train,y_train)

predicted = LR.predict(X_test)
print("Logistic Regression Accuracy:",metrics.accuracy_score(y_test, predicted))
print("Logistic Regression Precision:",metrics.precision_score(y_test, predicted))
print("Logistic Regression Recall:",metrics.recall_score(y_test, predicted))

test_text = model.encode(tokenizar('Quiero que seas capaz de abrir la aplicacion'))
test = LR.predict([test_text])
print(test)

print('Comenzando Árbol de Decisión')
y_pred = LR.predict(X_train)
decision_tree = DecisionTreeRegressor()
decision_tree.fit(X_train, y_pred)
pickle.dump(decision_tree, open('modelo.sav', 'wb'))

test_text = model.encode(tokenizar('Quiero que no me abras la aplicacion'))
y_pred_test = decision_tree.predict([test_text])
print(y_pred_test)