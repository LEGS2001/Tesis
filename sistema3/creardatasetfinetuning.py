# -*- coding: utf-8 -*-
import pandas as pd
import json

data_list = []
df = pd.read_csv('sistema3/fine_tuning_labels.csv')
SYSTEM_CONTENT = "Tu trabajo es detectar si una oracion esta relacionada a una accion especifica, y responder con el numero correspondiente a la accion. Donde 1 equivale a abrir una aplicacion, 2 equivale a cerrar una aplicacion, 3 equivale a dar click del raton, 4 equivale a seleccionar algo, 5 equivale a copiar algo, 6 equivale a pegar algo, y 0 equivale a que no es ninguna de las anteriores. Siempre responde con un numero, nunca respondas con algo que no sea solo el numero de lo pedido"
for index, row in df.iterrows():
    fine_tuning_data = {"messages":[{"role":"system","content":SYSTEM_CONTENT},{"role":"user","content":row['instruccion']}, {"role":"assistant","content":str(row['label'])}]}
    data_list.append(fine_tuning_data)

with open("sistema3/dataset_tuning.jsonl", 'w') as jsonl_file:
    for data in data_list:
        json_line = json.dumps(data)
        jsonl_file.write(json_line + '\n')

print(f"Se ha terminado de crear el dataset para el tuning")
