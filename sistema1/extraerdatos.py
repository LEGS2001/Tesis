from sentence_transformers import SentenceTransformer
from csv import writer

import pandas as pd
import numpy as np
import string
import spacy
import os

# carga las librerias necesarias para poder lematizar las oraciones de los datasets
nlp = spacy.load("es_core_news_md")
#model = SentenceTransformer('all-MiniLM-L6-v2')
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

    return oracion_lematizada

# calcula en que linea se quedo para seguir desde ahi
with open('sistema1/dataset.csv', 'r', encoding="utf8") as indicefile:
    indice = (len(indicefile.readlines())) + 1 # se le suma + 1 para anular el header

# carga el dataset que se va a usar para el entrenamiento
datasets = os.listdir('sistema1/datasets')
with open(f'sistema1/datasets/{datasets[0]}','r', encoding="utf8") as file:
    datos = file.readlines()[indice:]
    print('Datos cargados...')

with open('sistema1/dataset.csv', 'a', encoding="utf8", newline='') as outputfile:
    writer_object = writer(outputfile)
    # recorre cada linea los datasets y las limpia
    for linea in datos:
        linea = linea.strip()
        linea_lematizada = lematizar(linea)

        #embedding = model.encode(linea_lematizada)
        #embedding_str = ', '.join(map(str, embedding))

        # recorre cada linea de los datasets lematizados, y si encuentra el lema del label lo clasifica con su respectivo label
        # 0 = no existe; 1 = abrir; 2 = cerrar; 3 = clickear; 4 = seleccionar; 5 = copiar; 6 = pegar
        if 'abrir' in linea_lematizada or 'abre' in linea_lematizada:
            label = '1'
        elif 'cerrar' in linea_lematizada or 'cierra' in linea_lematizada:
            label = '2'
        elif 'clickear' in linea_lematizada or 'click' in linea_lematizada or 'clic' in linea_lematizada:
            label = '3'
        elif 'seleccionar' in linea_lematizada or 'seleccion' in linea_lematizada or 'selección' in linea_lematizada:
            label = '4'
        elif 'copiar' in linea_lematizada or 'copia' in linea_lematizada:
            label = '5'
        elif 'pegar' in linea_lematizada or 'pega' in linea_lematizada:
            label = '6'
        else:
            label = '0'
        
        writer_object.writerow([linea,label])

# NOTAS: 1) extraerdatos.py, 2) analisardataset.py, 3) entrenarmodelo.py, 4) cargarmodelo.py