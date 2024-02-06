from AppOpener import open, close
import pyautogui
import speech_recognition
import pyttsx3
import tkinter as tk
import ttkbootstrap as ttk
import threading

from sistema1.cargarmodelo import chatear
from sistema2.cargarmodelogpt import chatearGPT


# función encargada de la detección de voz para realizar comandos
def speech():
    recognizer = speech_recognition.Recognizer()
    print('[Escuchando Audio]')
    escuchando = True
    while escuchando:
        try:
            #mic_list = speech_recognition.Microphone.list_microphone_names()
            #print(mic_list)
            with speech_recognition.Microphone(1) as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.5)
                audio = recognizer.listen(mic)
                text = recognizer.recognize_google(audio, language="es-EC") #es-ES
                text = text.lower()
                if text != None:
                    return text
        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            continue
        except KeyboardInterrupt:
            break;

def comandos(label):
    # TODO: actualizar la version de python y utilizar un match case
    # 0 = no existe; 1 = abrir; 2 = cerrar; 3 = clickear; 4 = seleccionar; 5 = copiar; 6 = pegar
    # no existe
    if label == 0:
        print('El comando utilizado no existe')
    # abrir app
    if label == 1:
        print('Que aplicación desea abrir?')
        app = speech()
        open(app, match_closest=True)
    # cerrar app
    if label == 2:
        print('Que aplicación desea cerrar?')
        app = speech()
        close(app, match_closest=True)
    # clickear
    if label == 3:
        pyautogui.click()
    # seleccionar
    if label == 4:
        pyautogui.hotkey('ctrl', 'a')
        print('Seleccionando')
    # copiar
    if label == 5:
        pyautogui.hotkey('ctrl', 'c')
    # pegar
    if label == 6:
        pyautogui.hotkey('ctrl', 'v')

def modelo1():
    while True:
        prompt = speech()
        print(f'Comando: {prompt}')
        if 'salir' in prompt.lower():
            print('Saliendo...')
            break
        try:
            resp = chatear(prompt)
            print(resp)
        except:
            print("Error")

def modelo2():
    while True:
        prompt = speech()
        print(f'Comando: {prompt}')
        if 'salir' in prompt.lower():
            print('Saliendo...')
            break
        try:
            resp = chatearGPT(prompt)
            comandos(int(resp))
            print(resp)
        except:
            print("Error")

def modelo3():
    pass
    # Función para la opción 3 del menú principal
    #ventana_opcion3 = tk.Toplevel(root)
    #ventana_opcion3.title("Menú Opción 3")
    # Aquí puedes agregar los elementos del menú opción 3

def thread_modelo(model_func):
        threading.Thread(target=model_func).start()

def menu():
    # Crear la ventana principal
    root = ttk.Window(themename="darkly")
    root.title("Asistente Virtual")
    root.geometry("600x300")

    # Crear los botones del menú principal
    boton_opcion1 = tk.Button(root, text="Modelo 1 - Regresión Logística y Árboles de Decisión", command=lambda: thread_modelo(modelo1))
    boton_opcion1.pack(pady=10)

    boton_opcion2 = tk.Button(root, text="Modelo 2 - GPT Turbo 3.5", command=lambda: thread_modelo(modelo2))
    boton_opcion2.pack(pady=10)

    boton_opcion3 = tk.Button(root, text="Modelo 3 - GPT Fine Tuning", command=lambda: thread_modelo(modelo3))
    boton_opcion3.pack(pady=10)

    root.mainloop()

threading.Thread(target=menu).start()


# TODO:
# HACER QUE EL MODELO 1 SOLO SE CARGUE CUANDO SE CLIQUEA EL PRIMER BOTON (TALVEZ?)
# PAGAR OPENAI PARA EL FINETUNING
# CONECTAR EL ASISTENTE VIRTUAL CON CADA UNO DE LOS MODELOS