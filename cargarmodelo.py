from sentence_transformers import SentenceTransformer

import pickle
import spacy
import string

def tokenizar(oracion):
    nlp = spacy.load("es_core_news_md")
    stop_words = nlp.Defaults.stop_words
    puntuaciones = string.punctuation
    
    # convierte la oracion en un objeto procesable por la clase nlp de la libreria spacy
    oracion_nlp = nlp(oracion)
    # separa cada palabra de la oración en una lista y las lematiza
    tokens = [ word.lemma_.lower().strip() for word in oracion_nlp ]
    # elimina las "stop words" y las puntuaciones
    tokens = [ word for word in tokens if word not in stop_words and word not in puntuaciones ]
    # vuelve a convertir la lista en un string con cada palabra separada por un espacio
    oracion_lematizada = " ".join(tokens)
    return oracion_lematizada

model = SentenceTransformer('all-MiniLM-L6-v2')
loaded_model = pickle.load(open('modelo.sav', 'rb'))

while True:
    instruccion = input('Escribe el comando necesario')
    test_text = model.encode(tokenizar(instruccion))
    y_pred_test = loaded_model.predict([test_text])
    print(y_pred_test)