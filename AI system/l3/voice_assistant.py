from __future__ import annotations
import datetime
import sys
import webbrowser
import os
import tempfile

import pyttsx3
import speech_recognition as sr

# ---------- TTS (pyttsx3, офлайн) ----------
def say(text: str, rate: int = 160, volume: float = 0.8, prefer_voice_substr: str | None = None) -> None:
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)
    engine.setProperty('volume', volume)

    if prefer_voice_substr:
        voices = engine.getProperty('voices')
        for v in voices:
            if prefer_voice_substr.lower() in (v.name or "").lower():
                engine.setProperty('voice', v.id)
                break

    engine.say(text)
    engine.runAndWait()

def list_voices():
    print("Доступные голоса (pyttsx3):")
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for v in voices:
        print("------")
        print(f"Имя: {getattr(v, 'name', 'Unknown')}")
        print(f"ID: {getattr(v, 'id', 'Unknown')}")
        print(f"Язык(и): {getattr(v, 'languages', 'Unknown')}")
        print(f"Пол: {getattr(v, 'gender', 'Unknown')}")
        print(f"Возраст: {getattr(v, 'age', 'Unknown')}")

def recognize_once(prompt_tts: bool = True, prefer_voice_substr: str | None = None) -> str:
    r = sr.Recognizer()
    with sr.Microphone() as source:
        if prompt_tts:
            say("Говорите!", prefer_voice_substr=prefer_voice_substr)
        else:
            print("Говорите!")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio, language="ru-RU").lower()
        print("Вы сказали:", text)
        say("Вы сказали: " + text, prefer_voice_substr=prefer_voice_substr)
        return text
    except sr.UnknownValueError:
        say("Не понимаю Вас!", prefer_voice_substr=prefer_voice_substr)
        return ""
    except sr.RequestError as e:
        print(f"[ASR] Ошибка запроса к сервису: {e}")
        say("Ошибка распознавания речи.", prefer_voice_substr=prefer_voice_substr)
        return ""

def time_to_text(now: datetime.datetime | None = None) -> str:
    if now is None:
        now = datetime.datetime.now()
    h = now.hour
    m = now.minute

    dict_hours = {
        0: 'часов', 1: 'час', 2: 'часа', 3: 'часа', 4: 'часа',
        5: 'часов', 6: 'часов', 7: 'часов', 8: 'часов', 9: 'часов',
        10: 'часов', 11: 'часов', 12: 'часов', 13: 'часов', 14: 'часов',
        15: 'часов', 16: 'часов', 17: 'часов', 18: 'часов', 19: 'часов',
        20: 'часов', 21: 'час', 22: 'часа', 23: 'часа'
    }

    dict_minutes = {
        'минута': [1, 21, 31, 41, 51],
        'минуты': [2, 3, 4, 22, 23, 24, 32, 33, 34, 42, 43, 44, 52, 53, 54],
        'минут':  [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                   25, 26, 27, 28, 29, 30,
                   35, 36, 37, 38, 39, 40,
                   45, 46, 47, 48, 49, 50,
                   55, 56, 57, 58, 59]
    }

    res = f"{h} {dict_hours[h]} "
    for word, nums in dict_minutes.items():
        if m in nums:
            res += f"{m} {word}"
            break
    if m == 0:
        res += "ровно"
    return res

def handle_command(cmd: str, prefer_voice_substr: str | None = None) -> bool:
    """
    Возвращает True если следует продолжать, False — если завершать.
    """
    if not cmd:
        return True

    if "открой почту" in cmd or "open mail" in cmd:
        say("Открываю почту.", prefer_voice_substr=prefer_voice_substr)
        webbrowser.open("https://mail.ru")
    elif "сколько времени" in cmd or "который час" in cmd or "сколько время" in cmd:
        say(time_to_text(), prefer_voice_substr=prefer_voice_substr)
    elif "как тебя зовут" in cmd or "как твоё имя" in cmd or "кто ты" in cmd:
        say("Меня зовут Даша! А как зовут тебя?", prefer_voice_substr=prefer_voice_substr)
    elif "стоп" in cmd or "выход" in cmd or "stop" in cmd:
        say("Хорошо, заканчиваем разговор. До встречи!", prefer_voice_substr=prefer_voice_substr)
        return False
    else:
        say("Команда не распознана.", prefer_voice_substr=prefer_voice_substr)

    return True

def main():
    # Показать доступные голоса в консоли
    list_voices()

    preferred = "Dasha-Rus"

    say("Привет, меня зовут Даша! Давай поговорим!", prefer_voice_substr=preferred)

    while True:
        cmd = recognize_once(prefer_voice_substr=preferred)
        if not handle_command(cmd, prefer_voice_substr=preferred):
            break
        say("Поговорим ещё?", prefer_voice_substr=preferred)

if __name__ == "__main__":
    main()
