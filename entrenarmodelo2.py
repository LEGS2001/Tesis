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

model = SentenceTransformer('all-MiniLM-L6-v2')
#data = pd.read_csv("dataset.csv", on_bad_lines='skip', engine="python")
data = pd.read_csv("dataset.csv", on_bad_lines='skip', engine="python")
np.random.seed(2023)

X = data['embedding'].to_list()
y = data['label'].to_list()

# Convert string representations to NumPy arrays
X = [np.fromstring(embedding_str, sep=',') for embedding_str in X]

# Convert lists to NumPy arrays
X = np.array(X)
y = np.array(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,stratify=y)

print('Comenzando Regresión Logística')
LR = LogisticRegression()
LR.fit(X_train,y_train)
predicted = LR.predict(X_test)

print('Comenzando Árbol de Decisión')
y_pred = LR.predict(X_train)
decision_tree = DecisionTreeRegressor()
decision_tree.fit(X_train, y_pred)

pickle.dump(decision_tree, open('modelo.sav', 'wb'))