import openai
import os
from gtts import gTTS
import speech_recognition as sr
from playsound import playsound
from pydub import AudioSegment
from pydub.playback import play
import time
from pathlib import Path
from time import strftime
openai.api_key = "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"
def speak(data):
    global is_speaking
    try:
        # Chuyển đổi văn bản thành giọng nói
        audio = gTTS(remove_word(remove_word(data, "Thomas"), "thomas"), lang='vi')
        global number_count
        number_count = number_count + 1
        path_file_temp = str(os.path.join(os.getcwd(), "temp") + str(number_count) + "-sound.mp3")

        while os.path.isfile(path_file_temp):
            number_count = number_count + 1
            path_file_temp = str(os.path.join(os.getcwd(), "temp") + str(number_count) + "-sound.mp3")
        print(path_file_temp)
        audio.save(str(path_file_temp))

        output_file = str(os.path.join(os.getcwd(), "temp") + str(number_count) + "-output_audio_telephone.wav")
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

my_file = os.path.join(os.getcwd(), "data")
number_count = 1
is_speaking = False

def hello(name):
    day_time = int(strftime('%H'))
    if day_time < 12:
        speak("Chào buổi sáng {}. Chúc bạn một ngày tốt lành.".format(name))
    elif 12 <= day_time < 18:
        speak("Chào buổi chiều  {}. Bạn đã dự định gì cho chiều nay chưa.".format(name))
    else:
        speak("Chào buổi tối {}. Bạn đã ăn tối chưa nhỉ.".format(name))

# def fm():

def takeCommand():
    r = sr.Recognizer()
    global is_speaking
    if not is_speaking:
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source)

    # Nếu không đang phát âm thanh thì bật micro
    if is_speaking:
        with sr.Microphone() as source:
            source.stop_listening()

    try:
        if not is_speaking:
            print("Recognising...")
            return r.recognize_google(audio, language='vi-VN')
        return "---"
    except sr.UnknownValueError:
        print("No Human...")

    return "---"


def remove_word(text, word):
    # Thay thế tất cả các lần xuất hiện của từ "anh" bằng ""
    return text.replace(word, "")


def check_word(text, word):
    if str(word) == str(text):
        playsound(os.path.join(os.getcwd(), "data")+"\\come.mp3")
        speak("Xin chào")
        hello("Anh hàng xóm")
        return False;
    # Phân tách đoạn văn thành các từ
    words = text.split()

    # Kiểm tra xem từ "anh" có nằm trong danh sách các từ hay không
    for w in words:
        if w == word:
            playsound(os.path.join(os.getcwd(), "data")+"\\come.mp3")
            return True
    else:
        return False


def check_time_saving(file_path):
    while not os.path.exists(file_path):
        time.sleep(1)

    return True


def check_name(data):
    if check_word(data, "thomas") == 1:
        return True;
    if check_word(data, "Thomas") == 1:
        return True;
    return False

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
    play(modified_audio)

def call_chatgpt(text):
    # Gọi API ChatGPT
    # response = api.engine("chatGPT").create(prompt=text)
    response = openai.completions.create(
        model="text-davinci-003",
        prompt=text,
        temperature=0.9,
        max_tokens=350,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
    )

    # Trả về kết quả gọi API
    return str(response.choices[0].text)


while True:
    query = takeCommand().lower()
    print(query)
    print(os.path.join(os.getcwd(), "temp"))

    if query != "---" and check_name(query):
        playsound(os.path.join(os.getcwd(), "temp")+"\mid.mp3")
        data = call_chatgpt(query)
        print(data)
        speak(data)

    # data = call_chatgpt("thomas thủ đô nước việt nam ở đâu")
    # print(data)
    # speak(data)
