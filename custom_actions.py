#speak and listen function to use in llms
import speech_recognition as sr
from gtts import gTTS
import os
import struct
from elevenlabs import generate, play
import pyaudio
import pvporcupine
from threading import Thread
import random
import config
from dotenv import load_dotenv
load_dotenv()
from elevenlabs import set_api_key as eleven_api_key
eleven_api_key(os.getenv("ELEVEN_LABS_API_KEY"))
PORCUPINE_KEY = os.getenv("PORCUPINE_API_KEY")
from openai import OpenAI
import openai
import warnings

# Ignore DeprecationWarning
warnings.filterwarnings("ignore", category=DeprecationWarning)



#----begin of speaking code------#
import time
from pygame import mixer


def playaudio(filename):
    #os.system('ffplay -nodisp -autoexit -loglevel quiet '+filename)  # Play 
    mixer.init()
    mixer.music.load(filename)
    mixer.music.play()
    while mixer.music.get_busy():  # wait for music to finish playing
        time.sleep(0.5)



def speak(text): #no need api key
    response=("/tmp/response.mp3")
    response_mod='/tmp/response_mod.wav'
    tts = gTTS(text=text, lang=config.language,slow = False)
    tts.save(response)

    playaudio(response) #changed from ffmpeg to pygame play audio mp3;

    #os.system('ffmpeg -loglevel quiet -i /tmp/response.wav -af "asetrate=44100*0.5,atempo=1.8" /tmp/response_mod.wav')
    #os.system('ffplay -nodisp -autoexit -loglevel quiet '+response_mod)  # Play 
    #os.remove(response_mod)
    #os.remove(response)



def elevenspeak(text): #use with api key
    play(audio = generate(
        text=text,
        voice="Daniel",#"Matthew",
        model='eleven_multilingual_v1'
    ))


def ttsplay():
    response=("output.mp3")
    playaudio(response)

#tts openai
def tts(texto, nome_arquivo="output.mp3", modelo="tts-1", voz="alloy"):

  client = openai.OpenAI()

  response = client.audio.speech.create(
      model=modelo,
      voice=voz,
      input=texto,
  )

  response.stream_to_file(nome_arquivo)
  ttsplay()



def greating():
    if config.voice_engine == 1 and config.language == 'pt-BR':
        great = random.choice(['audio/Daniel_posso_ajudar.mp3','audio/Daniel_posso_ajudar2.mp3','audio/Daniel_posso_ajudar3.mp3'])
        playaudio(great)

    elif config.voice_engine == 2 and config.language == 'pt-BR':
        great = random.choice(['como posso te ajudar?', 'estou aqui para te ajudar','eu sempre estou aqui, como posso te ajudar?'])
        speak(great)

    elif config.voice_engine == 1 and config.language == 'en':
        great = random.choice(['how can I help you Sir?', 'I am at your service','I am always here, how can I help you?'])
        elevenspeak(great)

    elif config.voice_engine == 2 and config.language == 'en':
        great = random.choice(['how can I help you Sir?', 'I am at your service','I am always here, how can I help you?'])
        speak(great)
    else:
        print("System: Language not found, please check config.py file")


def talk(text):
    typevoice = config.voice_engine
    if typevoice == 1:
        elevenspeak(text)
    elif typevoice == 2:
        speak(text)
    elif typevoice == 3: #openai
        tts(text)
    else:
        print("System: Voice engine not found, please check config.py file")




def startup():

    #execute something on start-up --optional 
    
    #talk on start up
    if config.voice_engine == 1 and config.language == 'pt-BR':
        playaudio('audio/Daniel_iniciando.mp3')
        print('AI: Iniciando Sistemas')

    elif config.voice_engine == 2 and config.language == 'pt-BR':
        speak("Iniciando Sistemas")
        print('AI: Iniciando Sistemas')
    
    elif config.voice_engine == 1 and config.language == 'en':
        elevenspeak('Starting Systems')
        print('AI: Starting Systems')

    elif config.voice_engine == 2 and config.language == 'en':
        speak("Starting Systems")
        print('AI: Starting Systems')

    else:
        print("System: Voice engine or language  not found, please check config.py file")


def ready():
    #execute something on ready-up --optional

    #talk on ready
    if config.voice_engine == 1 and config.language == 'pt-BR':
        playaudio('audio/Daniel_pronto.mp3')
        print('System: Todos os sistemas calibrados e online')

    elif config.voice_engine == 2 and config.language == 'pt-BR':
        speak('Todos os sistemas calibrados e online')
        print('System: Todos os sistemas calibrados e online')

    elif config.voice_engine == 1 and config.language == 'en':
        elevenspeak('All systems online and calibrated')
        print('System: All systems online and calibrated')

    elif config.voice_engine == 2 and config.language == 'en': 
        speak('All systems online and calibrated')
        print('System: All systems online and calibrated')

    else:
        print("System: Voice engine or language  not found, please check config.py file")


def standby():
    #execute something on standby --optional

    #talk on standby
    if config.voice_engine == 1 and config.language == 'pt-BR':
        playaudio('audio/Daniel_Stand-by.mp3')
        print('System: Se precisar é só chamar meu nome, estarei no modo stand-by')

    elif config.voice_engine == 2 and config.language == 'pt-BR':
        speak('Se precisar é só chamar meu nome, estarei no modo stand-by')
        print('System: Se precisar é só chamar meu nome, estarei no modo stand-by')

    elif config.voice_engine == 1 and config.language == 'en':
        elevenspeak('Call my name if you need me. I will be in standby mode')
        print('System: Call my name if you need me. I will be in standby mode')

    elif config.voice_engine == 2 and config.language == 'en':
        speak('Call my name if you need me. I will be in standby mode')
        print('System: Call my name if you need me. I will be in standby mode')

    else:
        print("System: Voice engine or language  not found, please check config.py file")

#----end of speaking ------#

from faster_whisper import WhisperModel
def whispermodel(audio, idioma="pt", tamanho_modelo="tiny"):
    
    model = WhisperModel(tamanho_modelo, device="cpu", compute_type="int8")
    segments, _ = model.transcribe(audio, beam_size=5, vad_filter=True, 
                                 vad_parameters=dict(min_silence_duration_ms=500),
                                 language=idioma)
    transcricao = [segment.text for segment in segments]
    return transcricao

def whisperopenai(audio):
    client = openai.OpenAI()
    audio_file= open(audio, "rb")
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file
    )
    #print(transcription.text)
    return transcription.text


def listen():
    # Initialize speech recognizer
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 4000
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.8
    recog = False
    text = ""
    while(True):
        try: 
            with sr.Microphone() as source:
       
                print("System: Listening...:")
                audio = recognizer.listen(source,timeout=3)
                try:
                    with open("audio.mp3", "wb") as f:
                        f.write(audio.get_wav_data(convert_rate=16000))  # Converte para 16kHz para o Whisper
                        print("audio recorded audio.mp3")
                except Exception as e:
                    print("Erro ao gravar áudio:", e)

                
                print("System: Recognizing...")
                text = whispermodel("audio.mp3") #speak to text model
                #text = whisperopenai("audio.mp3")
                recog = True
                print("System: heard...")
                return text
        
        except sr.WaitTimeoutError:
            print("System: Timeout, no speak recognized")
            recog = False
            text = ""
            print("System: Stop Listening...")
            break 
        except sr.RequestError as e:
            print("System: No result in recognizing; {0}".format(e))
            recog = False
            text = ""
            print("System: Stop Listening...")
            break 
        except sr.UnknownValueError:
            print("System: Sorry, I didn't understand that")
            recog = False
            text = ""
            print("System: Stop Listening...")
            break 
    return text

# def listen():
#     # Initialize speech recognizer
#     recognizer = sr.Recognizer()
#     recognizer.energy_threshold = 4000
#     recognizer.dynamic_energy_threshold = True
#     recognizer.pause_threshold = 0.8
#     recog = False
#     text = ""
#     while(True):
#         try: 
#             with sr.Microphone() as source:
       
#                 print("System: Listening...:")
#                 audio = recognizer.listen(source,timeout=2)
#                 try:
#                     with open("audio.mp3", "wb") as f:
#                         f.write(audio.get_wav_data(convert_rate=16000))  # Converte para 16kHz para o Whisper
#                         print("audio recorded audio.mp3")
#                 except Exception as e:
#                     print("Erro ao gravar áudio:", e)

#                 print("System: Recognizing...")
#                 text = recognizer.recognize_google(audio, language=config.language)
#                 recog = True
#                 print("System: heard...")
#                 return text
        
#         except sr.WaitTimeoutError:
#             print("System: Timeout, no speak recognized")
#             recog = False
#             text = ""
#             print("System: Stop Listening...")
#             break 
#         except sr.RequestError as e:
#             print("System: No result in recognizing; {0}".format(e))
#             recog = False
#             text = ""
#             print("System: Stop Listening...")
#             break 
#         except sr.UnknownValueError:
#             print("System: Sorry, I didn't understand that")
#             recog = False
#             text = ""
#             print("System: Stop Listening...")
#             break 
#     return text


#print(listen())


class WakeWord:
    def __init__(self):
        self.wakeup = False
    def start_wake_thread(self):
        self.thread = Thread(target=self.wake)
        self.thread.daemon = True
        self.thread.start()
    def wake(self):    
        porcupine = None
        pa = None
        audio_stream = None
        try:
            porcupine = pvporcupine.create(access_key=PORCUPINE_KEY,keywords=["jarvis", "blueberry"])
            pa = pyaudio.PyAudio()
            audio_stream = pa.open(
                            rate=porcupine.sample_rate,
                            channels=1,
                            format=pyaudio.paInt16,
                            input=True,
                            frames_per_buffer=porcupine.frame_length)
            while True:
                self.wakeup =False
                pcm = audio_stream.read(porcupine.frame_length)
                pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
                keyword_index = porcupine.process(pcm)
                if keyword_index >= 0:
                    print("System: Hotword Detected")
                    self.wakeup = True
                    return self.wakeup
        finally:
            if porcupine is not None:  #todo stop thread ?
                porcupine.delete()
            if audio_stream is not None:
                audio_stream.close()
            if pa is not None:
                pa.terminate()
wake_word_instance = WakeWord()

#function to get system time and date, use to other function like history or database.
import datetime
import csv
import json
def get_system_time_date():
    #get system time
    now = datetime.datetime.now()
    return now


#function to save chat history. saving both each chat prompt and response. CSV format with date, time and prompt and response.
def save_database(prompt, answer):
    #get system time and date
    now = get_system_time_date()
    #save history
    with open('history.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([now, prompt, answer])

#function to get history from csv file and return as jason.dumps due to insert the prompt
def get_database():
    #todo - use a cloud database in the future
    #get history
    with open('history.csv', newline='') as file:
        reader = csv.reader(file)
        history = list(reader)
    #convert to json
    history = json.dumps(history)
    return history
