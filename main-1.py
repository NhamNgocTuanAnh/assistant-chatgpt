import openai
import os
from gtts import gTTS
import speech_recognition as sr
from playsound import playsound
from pydub import AudioSegment
from pydub.playback import play
import time
from time import strftime
import requests
import yaml
with open("config.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.Loader)
number_count = 1
is_speaking = False
import os
from decimal import Decimal
import time
import pytz

UTC = pytz.timezone('UTC')  # utc
from datetime import datetime as dt

now = dt.now(pytz.timezone('Asia/Ho_Chi_Minh'))

import threading, queue
import multiprocessing

def remove_word(text, word):
    # Thay thế tất cả các lần xuất hiện của từ "anh" bằng ""
    return text.replace(word, "")



def apply_telephone_effect(input_file, output_file):
    # Load the audio file
    audio = AudioSegment.from_file(input_file)

    # Simulate reduced frequency range (equalization)
    audio = audio.low_pass_filter(2000)

    # Simulate distortion
    audio = audio + 10  # Increase volume (amplify)

    # Export the modified audio
    audio.export(output_file, format="wav")

    # Play the original and modified audio for comparison
    # play(audio)
    modified_audio = AudioSegment.from_file(output_file)
    os.remove(input_file)
    os.remove(output_file)
    play(modified_audio)

def takeCommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:

        print("Recognising...")
        return r.recognize_google(audio, language='vi-VN')
    except sr.UnknownValueError:
        print("No Human...")

    return "---"

def speak(data):
    global is_speaking
    try:
        # Chuyển đổi văn bản thành giọng nói
        audio = gTTS(remove_word(remove_word(data, "Thomas"), "thomas"), lang='vi')
        global number_count
        if number_count > 9999:
            number_count = 0
        number_count = number_count + 1
        path_file_temp = str(os.path.join(os.getcwd(), "temp") + "\\" + str(number_count) + "-sound.mp3")

        while os.path.isfile(path_file_temp):
            number_count = number_count + 1
            path_file_temp = str(os.path.join(os.getcwd(), "temp") + "\\" + str(number_count) + "-sound.mp3")
        print(path_file_temp)
        audio.save(str(path_file_temp))

        output_file = str(os.path.join(os.getcwd(), "temp") + "\\" + str(number_count) + "-output_audio_telephone.wav")
        playsound(os.path.join(os.getcwd(), "data")+"\\mid.mp3")
        is_speaking = True
        apply_telephone_effect(str(path_file_temp), output_file)
        # playsound(path_file_temp)
        is_speaking = False
        time.sleep(3)

    except Exception as e:
        print(e)
    finally:
        print("Chuyển đổi văn bản thành giọng nói")

    return True

def Main():
    print("Số lượng cpu : ", multiprocessing.cpu_count())

    tReadFile = threading.Thread(target=takeCommand)
    tProcessingFile = threading.Thread(target=speak)

    tReadFile.start()
    tProcessingFile.start()

    tProcessingFile.join()
    tReadFile.join()
    print("Bye !!!")