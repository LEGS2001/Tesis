from sentence_transformers import SentenceTransformer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn import metrics

import pandas as pd
import numpy as np
import spacy
import pickle
import ast

np.random.seed(2023)
model = SentenceTransformer('all-MiniLM-L6-v2')
#data = pd.read_csv("dataset.csv", on_bad_lines='skip', engine="python")
data = pd.read_csv("sistema1/datasetsfinales/datasetconembeddings.csv", on_bad_lines='skip', engine="python")


# TODO: calcular un buen numero de filas que eliminar para prevenir el overfitting
percentage_to_remove = 95
rows_to_remove = data[data['label'] == 0]
num_rows_to_remove = int(len(rows_to_remove) * (percentage_to_remove / 100))
data = data.drop(rows_to_remove.sample(num_rows_to_remove).index)
data = data.reset_index(drop=True)

# crea arrays de numpy. "X" para los embeddings; "y" para los labels
X = data['embedding'].to_list()
y = data['label'].to_list()

X = [np.fromstring(embedding_str, sep=',') for embedding_str in X]

X = np.array(X)
y = np.array(y)

# separa el dataset en sets de entrenamiento y de pruebas
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,stratify=y)

print('Comenzando Regresión Logística')
LR = LogisticRegression(max_iter=999999999) # max_iter=None
LR.fit(X_train,y_train)
predicted = LR.predict(X_test)

print('Comenzando Árbol de Decisión')
y_pred = LR.predict(X_train)
decision_tree = DecisionTreeRegressor()
decision_tree.fit(X_train, y_pred)

pickle.dump(decision_tree, open('sistema1/modelo.sav', 'wb'))