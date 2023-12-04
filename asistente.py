from AppOpener import open, close
import pyautogui
import speech_recognition
import pyttsx3

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