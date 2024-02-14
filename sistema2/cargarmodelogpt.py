from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

def chatearGPT(prompt):
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system", 
                "content": """Tu trabajo es detectar si una oracion esta relacionada a una accion especifica, 
                              y responder con el numero correspondiente a la accion. Donde 1 equivale a abrir una aplicación,
                              2 equivale a cerrar una aplicación, 3 equivale a dar click del raton, 4 equivale a seleccionar
                              algo, 5 equivale a copiar algo, 6 equivale a pegar algo, y 0 equivale a que no es ninguna de
                              las anteriores. Siempre responde con un numero, nunca respondas con algo que no sea solo el numero de lo pedido"""},
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo-1106",
    )
    return chat_completion.choices[0].message.content

#def chatearGPT(instruccion):
 #   response = chat(instruccion)
 #   return response