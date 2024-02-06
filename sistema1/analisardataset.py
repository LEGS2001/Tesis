from sentence_transformers import SentenceTransformer

import pandas as pd
import spacy
import string

nlp = spacy.load("es_core_news_md")
model = SentenceTransformer('all-MiniLM-L6-v2')
stop_words = nlp.Defaults.stop_words
puntuaciones = f'."-,¡¿:{string.punctuation}'

def lematizar(oracion):
    # convierte la oracion en un objeto procesable por la clase nlp de la libreria spacy
    oracion_nlp = nlp(oracion)
    # separa cada palabra de la oración en una lista y las lematiza
    tokens = [ word.lemma_.lower().strip() for word in oracion_nlp ]
    # elimina las "stop words" y las puntuaciones
    tokens = [ word for word in tokens if word not in stop_words and word not in puntuaciones ]
    # vuelve a convertir la lista en un string con cada palabra separada por un espacio
    oracion_lematizada = " ".join(tokens)
    embedding = model.encode(oracion_lematizada)
    embedding_str = ', '.join(map(str, embedding))

    return embedding_str

data = pd.read_csv("sistema1/dataset.csv", on_bad_lines='skip', engine="python")

rows_to_remove = data[data['label'] == 0]
num_rows_to_remove = len(rows_to_remove) - 80000
data = data.drop(rows_to_remove.sample(num_rows_to_remove).index)
data = data.reset_index(drop=True)

print(data['label'].value_counts())

for index, row in data.iterrows():
    data.at[index, 'embedding'] = lematizar(row['text'])

data.to_csv('sistema1/dataset_embeddings.csv', index=False)
print('Finalizado!')