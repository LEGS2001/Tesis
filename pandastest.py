import pandas as pd
import os
import spacy
import string
from csv import writer

# carga las librerias necesarias para poder lematizar las oraciones de los datasets
nlp = spacy.load("es_core_news_md")
stop_words = nlp.Defaults.stop_words
puntuaciones = string.punctuation

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

datasets = os.listdir('datasets')
# TODO: Hacer que recorra la lista de datasets y que pase por cada uno de los archivos
# lee cada uno de los archivos de la carpeta de datasets para obtener el dataset final procesado

with open(f'datasets/{datasets[23]}','r', encoding="utf8") as file:
    # Esta linea se debe descomentar cada vez que se vuelve a crear el dataset
    # writer_object.writerow(['text', 'label'])    
    datos = file.readlines()
    df = pd.DataFrame({'text':datos[:1000000]})
    print('Datos cargados...')
    print(df)

# recorre cada linea los datasets y las limpia
def agregar_label(linea):
    print(linea.name)
    linea = linea['text']
    linea = linea.rstrip()
    linea_lematizada = lematizar(linea)
    # recorre cada linea de los datasets lematizados, y si encuentra el lema del label lo clasifica con su respectivo label
    # 0 = no existe; 1 = abrir; 2 = cerrar; 3 = cerrar ultima; 4 = clickear; 5 = seleccionar; 6 = copiar; 7 = pegar
    if 'abrir' in linea_lematizada or 'abre' in linea_lematizada:
        return("1")
    elif 'cerrar' in linea_lematizada or 'cierra' in linea_lematizada:
        return("2")
    elif 'clickear' in linea_lematizada or 'click' in linea_lematizada or 'clic' in linea_lematizada:
        return("3")
    elif 'seleccionar' in linea_lematizada or 'seleccion' in linea_lematizada or 'selección' in linea_lematizada:
        return("4")
    elif 'copiar' in linea_lematizada or 'copia' in linea_lematizada:
        return("5")
    elif 'pegar' in linea_lematizada or 'pega' in linea_lematizada:
        return("6")
    else:
        return("0")

# TODO: seguir haciendo pruebas con pandas para ver si se mejora la eficiencia
df['label'] = df.apply(lambda row: agregar_label(row), axis=1)
print(df)