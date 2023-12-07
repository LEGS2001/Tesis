from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

def chat(prompt):
    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system", 
                "content": """Tu trabajo es detectar si una oración está relacionada a una acción específica, 
                              y responder con el número correspondiente a la acción. Donde 1 equivale a abrir una aplicación,
                              2 equivale a cerrar una aplicación, 3 equivale a dar click del ratón, 4 equivale a seleccionar
                              algo, 5 equivale a copiar algo, 6 equivale a pegar algo, y 0 equivale a que no es ninguna de
                              las anteriores. Siempre responde con un número"""},
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",
    )
    return chat_completion.choices[0].message.content
    
if __name__ == "__main__":
    while True:
        instruccion = input('Escribe tu instruccion \n')
        if instruccion.lower() == 'salir':
            break
        response = chat(instruccion)
        print(response)