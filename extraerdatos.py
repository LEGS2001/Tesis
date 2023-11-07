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
    with open('dataset.csv', 'w', encoding="utf8", newline='') as outputfile:
        writer_object = writer(outputfile)
        writer_object.writerow(['text', 'label'])

        # recorre cada linea los datasets y las limpia
        for linea in file:
            linea = linea.rstrip()
            linea_lematizada = lematizar(linea)
            
            # recorre cada linea de los datasets lematizados, y si encuentra el lema del label lo clasifica con su respectivo label
            # 0 = no existe; 1 = abrir; 2 = cerrar; 3 = cerrar ultima; 4 = clickear; 5 = seleccionar; 6 = copiar; 7 = pegar
            if 'abrir' in linea_lematizada:
                writer_object.writerow([linea, '1'])
            elif 'cerrar' in linea_lematizada:
                writer_object.writerow([linea, '2'])
            # elif '' in linea_lematizada: #TODO: ver como seleccionar ultima app abierta
            #     writer_object.writerow([linea, '3'])
            elif 'clickear' in linea_lematizada or 'click' in linea_lematizada or 'clic' in linea_lematizada:
                writer_object.writerow([linea, '4'])
            elif 'seleccionar' in linea_lematizada or 'seleccion' in linea_lematizada or 'selección' in linea_lematizada:
                writer_object.writerow([linea, '5'])
            elif 'copiar' in linea_lematizada or 'copia' in linea_lematizada:
                writer_object.writerow([linea, '6'])
            elif 'pegar' in linea_lematizada:
                writer_object.writerow([linea, '7'])
            else:
                writer_object.writerow([linea, '0'])