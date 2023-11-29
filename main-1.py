import speech_recognition as sr
import time
import os
import openai
import threading
from pathlib import Path
from gtts import gTTS
import playsound
my_file = Path("C:\\Users\\Surface\\Downloads\\data")
number_count = 1
def recognize_speech():
    # Khởi tạo đối tượng nhận dạng giọng nói
    recognizer = sr.Recognizer()

    # Tạo bộ lọc tiếng ồn
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)

    # Nhận dạng giọng nói
    audio = recognizer.listen(source)

    # Trả về kết quả nhận dạng
    try:
        return recognizer.recognize_google(audio, language='vi-VN')
    except sr.UnknownValueError:
        return None

def call_chatgpt(text):
    # Tạo đối tượng API ChatGPT
    from openai import OpenAI

    # Khởi tạo đối tượng OpenAI
    api = OpenAI("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")

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
    return response.choices[0].text

def play_sound(text):
    # Tạo đối tượng tạo âm thanh
    from gtts import gTTS

    # Tạo đối tượng âm thanh
    tts = gTTS(text, lang="vi")
    # Lưu âm thanh vào file
    # tts.save("audio.mp3")
    # # Phát âm thanh
    # playsound("audio.mp3")

    global number_count
    number_count = number_count + 1
    path_file_temp = str("C:\\Users\\Surface\\Downloads\\data\\" + str(number_count) + "-sound.mp3")
    print(path_file_temp)
    while os.path.isfile(path_file_temp):
        number_count = number_count + 1
        path_file_temp = str("C:\\Users\\Surface\\Downloads\\data\\" + str(number_count) + "-sound.mp3")

    tts.save(str(path_file_temp))

    playsound(text)


def main():
    # Khởi tạo biến
    is_speaking = False

    # Tạo luồng nhận dạng giọng nói
    thread_recognize = threading.Thread(target=recognize_speech)
    thread_recognize.daemon = True
    thread_recognize.start()

    # Vòng lặp chính
    while True:
        # Nếu đang phát âm thanh thì tắt micro
        if is_speaking:
            with sr.Microphone() as source:
                source.stop_listening()

        # Nếu không đang phát âm thanh thì bật micro
        if not is_speaking:
            with sr.Microphone() as source:
                source.start_listening()

        # Kiểm tra nếu có kết quả nhận dạng giọng nói
        text = recognize_speech()
        if text is not None:
            # Gọi API ChatGPT
            response = call_chatgpt(text)

            # Viết kết quả gọi API vào file
            with open("C:\\Users\\Surface\\Downloads\\sound.mp3\\output.txt", "a", encoding="utf-8") as f:
                f.write(response + "\n")

            # Phát âm thanh
            play_sound(response)

            # Chuyển trạng thái đang phát âm thanh
            is_speaking = True

        # Ngủ 1 giây
        time.sleep(1)