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

def comandos(label, nombre_modelo, watermark):
    # 0 = no existe
    if label == 0:
        watermark.config(text=f'{nombre_modelo}: [EL COMANDO NO EXISTE]')
        watermark.after(2000, lambda: watermark.config(text=f'{nombre_modelo}: [ESCUCHANDO]'))
    # 1 = abrir app
    if label == 1:
        #print('Que aplicación desea abrir?')
        watermark.config(text=f'{nombre_modelo}: [¿QUE APLICACIÓN DESEA ABRIR?]')
        app = speech()
        try:
            open(app, match_closest=True, throw_error=True)
            watermark.config(text=f'{nombre_modelo}: [ABRIENDO]')
        except:
           watermark.config(text=f'{nombre_modelo}: [LA APLICACIÓN NO EXISTE]') 
        finally:
            watermark.after(2000, lambda: watermark.config(text=f'{nombre_modelo}: [ESCUCHANDO]'))
    # 2 = cerrar app
    if label == 2:
        watermark.config(text=f'{nombre_modelo}: [¿QUE APLICACIÓN DESEA CERRAR?]')
        app = speech()
        try:
            close(app, match_closest=True, throw_error=True)
            watermark.config(text=f'{nombre_modelo}: [CERRANDO]')
        except:
            watermark.config(text=f'{nombre_modelo}: [LA APLICACIÓN NO EXISTE]') 
        finally:
            watermark.after(2000, lambda: watermark.config(text=f'{nombre_modelo}: [ESCUCHANDO]'))
    # 3 = clickear
    if label == 3:
        pyautogui.click()
        watermark.config(text=f'{nombre_modelo}: [CLICKEANDO]')
        watermark.after(2000, lambda: watermark.config(text=f'{nombre_modelo}: [ESCUCHANDO]'))
    # 4 = seleccionar
    if label == 4:
        pyautogui.hotkey('ctrl', 'a')
        watermark.config(text=f'{nombre_modelo}: [SELECCIONANDO]')
        watermark.after(2000, lambda: watermark.config(text=f'{nombre_modelo}: [ESCUCHANDO]'))
    # 5 = copiar
    if label == 5:
        pyautogui.hotkey('ctrl', 'c')
        watermark.config(text=f'{nombre_modelo}: [COPIANDO]')
        watermark.after(2000, lambda: watermark.config(text=f'{nombre_modelo}: [ESCUCHANDO]'))
    # 6 = pegar
    if label == 6:
        pyautogui.hotkey('ctrl', 'v')
        watermark.config(text=f'{nombre_modelo}: [PEGANDO]')
        watermark.after(2000, lambda: watermark.config(text=f'{nombre_modelo}: [ESCUCHANDO]'))

def correr_modelo(num_modelo, nombre_modelo, root_watermark, watermark):
    corriendo_modelo = True
    while corriendo_modelo:
        prompt = unidecode(speech())
        print(f'Comando: {prompt}')
        if 'salir' in prompt.lower():
            corriendo_modelo = False
            break
        try:
            if num_modelo == 1:
                resp = int(chatear(prompt)[0])
            if num_modelo == 2:
                resp = int(chatearGPT(prompt))
            if num_modelo == 3:
                resp = int(chatear_finetuning(prompt))
            comandos(resp, nombre_modelo, watermark)      
        except Exception as e:
            print(f"Error {e}")
    
    activar_botones()   
    root_watermark.destroy()

def crear_watermark(root, nombre_modelo):
    root_watermark = tk.Toplevel(root)
    root_watermark.wm_overrideredirect(True)
    root_watermark.geometry(f"+10+10")  
    root_watermark.attributes('-topmost', True) 

    watermark = tk.Label(root_watermark, text=f'{nombre_modelo}: [ESCUCHANDO]', font=("Helvetica", 20))  # Cambiar el tamaño de la fuente
    watermark.pack(padx=10, pady=10) 

    return root_watermark, watermark

def manejar_threads(root, nombre_modelo, num_modelo):
    desactivar_botones()
    root_watermark, watermark = crear_watermark(root, nombre_modelo)
    threading.Thread(target=correr_modelo, args=(num_modelo, nombre_modelo, root_watermark, watermark)).start()

botones = []
def desactivar_botones():
    for boton in botones:
        boton.config(state="disabled")
def activar_botones():
    for boton in botones:
        boton.config(state="normal")

def menu_principal():

    root = ttk.Window(themename="darkly")
    root.title("Asistente Virtual")
    root.geometry("600x300")

    boton_opcion1 = tk.Button(root, text="Modelo 1 - Regresión Logística y Árboles de Decisión", command=lambda: manejar_threads(root, 'Modelo 1', 1))
    boton_opcion1.pack(pady=10)
    botones.append(boton_opcion1)

    boton_opcion2 = tk.Button(root, text="Modelo 2 - GPT Turbo 3.5", command=lambda: manejar_threads(root, 'Modelo 2', 2))
    boton_opcion2.pack(pady=10)
    botones.append(boton_opcion2)

    boton_opcion3 = tk.Button(root, text="Modelo 3 - GPT Fine Tuning", command=lambda: manejar_threads(root, 'Modelo 3', 3))
    boton_opcion3.pack(pady=10)
    botones.append(boton_opcion3)

    root.mainloop()
    
if __name__ == "__main__":
    menu_principal()