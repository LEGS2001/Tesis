from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

def chatear_finetuning(prompt):
    client = OpenAI()
    response = client.chat.completions.create(
    model=os.environ.get("OPENAI_FINETUNING_MODEL"),
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
            ]
    )
    return response.choices[0].message.content
