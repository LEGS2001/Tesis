from AppOpener import open, close
import pyautogui
import speech_recognition
import pyttsx3
import tkinter as tk
import ttkbootstrap as ttk
import threading

from sistema2.cargarmodelogpt import chatearGPT, handle_response

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
                print(f'Comando de voz: {text}')      
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
        app = str(input('Que aplicación desea abrir?'))
        open(app, match_closest=True)
    
    # cerrar app
    if label == 2:
        app = str(input('Que aplicación desea cerrar?'))
        close(app, match_closest=True)

    # clickear
    if label == 3:
        pyautogui.click()

    # seleccionar
    if label == 4:
        pyautogui.hotkey('ctrl', 'a')

    # copiar
    if label == 5:
        pyautogui.hotkey('ctrl', 'c')

    # pegar
    if label == 6:
        pyautogui.hotkey('ctrl', 'v')

def modelo1():
    # Función para la opción 1 del menú principal
    ventana_opcion1 = tk.Toplevel(root)
    ventana_opcion1.title("Menú Opción 1")
    # Aquí puedes agregar los elementos del menú opción 1

def modelo2():
    # Función para la opción 2 del menú principal
    #ventana_opcion2 = tk.Toplevel(root)
    #ventana_opcion2.title("Menú Opción 2")
    # Aquí puedes agregar los elementos del menú opción 2
    while True:
        prompt = input("Escribe la instrucción deseada \n")
        if prompt.lower() == 'salir':
            break
        try:
            resp = chatearGPT(prompt)
            print(resp)
            #thread = threading.Thread(target=chatearGPT, args=(prompt, handle_response)).start()
            #thread.join()
        except:
            print("Error")

def modelo3():
    # Función para la opción 3 del menú principal
    ventana_opcion3 = tk.Toplevel(root)
    ventana_opcion3.title("Menú Opción 3")
    # Aquí puedes agregar los elementos del menú opción 3

# Crear la ventana principal
root = ttk.Window(themename="darkly")
root.title("Asistente Virtual")
root.geometry("600x300")

# Crear los botones del menú principal
boton_opcion1 = tk.Button(root, text="Modelo 1 - Regresión Logística y Árboles de Decisión", command=modelo1)
boton_opcion1.pack(pady=10)

boton_opcion2 = tk.Button(root, text="Modelo 2 - GPT Turbo 3.5", command=modelo2)
boton_opcion2.pack(pady=10)

boton_opcion3 = tk.Button(root, text="Modelo 3 - GPT Fine Tuning", command=modelo3)
boton_opcion3.pack(pady=10)

root.mainloop()

# SI SE SIGUE CONGELANDO AL COMPRAR OPENAI INTENTAR HACIENDOLO SEPARANDO EN UN THREAD APARTE EL GUI