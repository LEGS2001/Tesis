from AppOpener import open, close
from unidecode import unidecode

import pyautogui
import speech_recognition
import tkinter as tk
import ttkbootstrap as ttk
import threading

from sistema1.cargarmodelo import chatear
from sistema2.cargarmodelogpt import chatearGPT
from sistema3.cargarmodelofinetuning import chatear_finetuning

corriendo_modelo = False
# función encargada de la detección de voz para realizar comandos
def speech():
    recognizer = speech_recognition.Recognizer()
    while True:
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
    print('Sigo sin esucchar')
def comandos(label):
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

def clickear_watermark():
    #global corriendo_modelo
    #corriendo_modelo = False    
    print("Boton cliqueado")

def crear_watermark():
    root_watermark = tk.Tk()
    root_watermark.wm_overrideredirect(True)
    root_watermark.geometry(f"+10+10")  
    root_watermark.attributes('-topmost', True) 
    root_watermark.bind("<Button-1>", lambda evt: clickear_watermark())
    
    watermark = tk.Label(root_watermark, text='[ESCUCHANDO]', font=("Helvetica", 20))  # Cambiar el tamaño de la fuente
    watermark.pack(padx=10, pady=10) 
    
    while corriendo_modelo:
        root_watermark.update()

def modelo1():
    global corriendo_modelo
    while corriendo_modelo:
        prompt = speech()
        # quita tildes y otros acentos
        prompt = unidecode(prompt)
        print(f'Comando: {prompt}')
        if 'salir' in prompt.lower():
            corriendo_modelo = False
            break
        try:
            resp = chatear(prompt)
            comandos(int(resp[0]))
        except:
            print("Error")

def modelo2():
    global corriendo_modelo
    while corriendo_modelo:
        prompt = speech()
        # quita tildes y otros acentos
        prompt = unidecode(prompt)
        print(f'Comando: {prompt}')
        if 'salir' in prompt.lower():
            corriendo_modelo = False
            break
        try:
            resp = chatearGPT(prompt)
            comandos(int(resp))
        except:
            print("Error")

def modelo3():
    global corriendo_modelo
    while corriendo_modelo:
        prompt = speech()
        # quita tildes y otros acentos
        prompt = unidecode(prompt)
        print(f'Comando: {prompt}')
        if 'salir' in prompt.lower():
            corriendo_modelo = False
            break
        try:
            resp = chatear_finetuning(prompt)
            comandos(int(resp))
        except:
            print("Error")

def manejar_threads(modelo):
    global corriendo_modelo
    corriendo_modelo = True
    modelo_thread = threading.Thread(target=modelo).start()
    watermark_thread = threading.Thread(target=crear_watermark).start()
 
def menu_principal():
    # Crear la ventana principal
    root = ttk.Window(themename="darkly")
    root.title("Asistente Virtual")
    root.geometry("600x300")

    # Crear los botones del menú principal
    boton_opcion1 = tk.Button(root, text="Modelo 1 - Regresión Logística y Árboles de Decisión", command=lambda: manejar_threads(modelo1))
    boton_opcion1.pack(pady=10)

    boton_opcion2 = tk.Button(root, text="Modelo 2 - GPT Turbo 3.5", command=lambda: manejar_threads(modelo2))
    boton_opcion2.pack(pady=10)

    boton_opcion3 = tk.Button(root, text="Modelo 3 - GPT Fine Tuning", command=lambda: manejar_threads(modelo3))
    boton_opcion3.pack(pady=10)

    root.mainloop()

# este thread siempre tiene que estar activo, no necesita flag
if __name__ == "__main__":
    menu_principal()

# TODO:
# se intento hacer que clickeando el watermark funcione, pero generaba problemas con la libreria de voz
# el problema es que no se puede interrumpir el thread hasta que termine de escuchar por voz
# lo mejor es usar salir como comando ya que finaliza al escuchar la instruccion