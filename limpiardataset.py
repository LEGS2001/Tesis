import pandas as pd
import spacy
import string
import re

puntuaciones = string.punctuation
def limpiar(oracion):
    oracion = re.sub(f'[."-,¡¿:{puntuaciones}]', "", str(oracion))
    oracion = oracion.strip()
    return oracion

data = pd.read_csv("dataset.csv", on_bad_lines='skip', engine="python")
print('Datos cargados...')

data['text'] = data['text'].apply(limpiar)

data.to_csv('datasetlimpio.csv', index=False)