import openai 

API_KEY = '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'

def chat(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user","content": prompt}]
    )

    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    while True:
        instruccion = input('Escribe tu instruccion')
        response = chat(instruccion)
        print(response)