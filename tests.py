import pandas as pd
import timeit
import sys

from sistema1.cargarmodelo import chatear
from sistema2.cargarmodelogpt import chatearGPT
from sistema3.cargarmodelofinetuning import chatear_finetuning

def timear_modelo(num_modelo, prompts, expected_results):
    contador = 0
    for prompt, expected_result in zip(prompts, expected_results):
        try:
            if num_modelo == 1:
                resp = int(chatear(prompt)[0])
            if num_modelo == 2:
                resp = int(chatearGPT(prompt))
            if num_modelo == 3:
                resp = int(chatear_finetuning(prompt))
                
            if int(resp) == int(expected_result):
                contador += 1
        except Exception as e:
            print(f"Error {e}")
    
    tasa_eficiencia = (contador/len(prompts)) * 100
    print(f'Correctas: {contador}/{len(contador)}')
    print(tasa_eficiencia)

df = pd.read_csv('testing_dataset.csv')

prompts = df['prompt'].tolist()
expected_results = df['expected_result'].tolist()

print('[Comenzando timeo]')
print(timeit.timeit(lambda: timear_modelo(1, prompts, expected_results), number=100)) 
#10 => 0.06 100 => 0.028 1000 => 0.023