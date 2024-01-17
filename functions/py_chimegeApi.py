import requests, datetime, pyaudio, wave, pygame
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play

# яриаг бичвэрт хөрвүүлэх
def transcribe(filename):
    with open(filename, 'rb') as f:
        audio = f.read()

    print(audio)
    print(type(audio))
    r = requests.post("https://api.chimege.com/v1.2/transcribe", data=audio, headers={
        'Content-Type': 'application/octet-stream',
        'Punctuate': 'true',
        'Token': '47c59cc7d497544cbbc3a81287072b2005a857d15642c65e5457a9c53e68e0cb'
    })

    return r.content.decode("utf-8")

# бичвэрийг ярианд хөрвүүлэх
def synthesize(text):
    url = "https://api.chimege.com/v1.2/synthesize"
    headers = {
        'Content-Type': 'plain/text',
        'Token': '67d13a314527c3f40f0817a7bdb1cb1fbe69296ce94276e6cb9eb978c86e0708'
    }

    r = requests.post(
        url, data=text.encode('utf-8'), headers=headers)

    # файл болгон хангалах
    # with open("Enkhee.wav", 'wb') as out:
    #     out.write(r.content)

    # Аудиог файлд хөрвүүлэлгүй шууд тоглуулах
    if r.status_code == 200 :
        audio_content = BytesIO(r.content)
        audio_segment = AudioSegment.from_file(audio_content, format="wav")

        pygame.mixer.init()

        # Аудио сегментийг pygame холигч руу ачааллана
        pygame.mixer.music.load(audio_segment.export(format="wav"))

        # Аудио тоглуулаална
        pygame.mixer.music.play()

        # Аудио тоглуулж дуустал хүлээнэ
        pygame.time.wait(int(audio_segment.duration_seconds * 10300))

        print("Аудиог тоглуулалсан.")
    else :
        print(f"Алдаа {r.status_code} : {r.text}")

# Алдаа засагч. Тоог бичвэрт хөрвүүлэх
def normalize(text):
    url = "https://api.chimege.com/v1.2/normalize-text"
    headers = {
        'Content-Type': 'plain/text',
        'Token': '67d13a314527c3f40f0817a7bdb1cb1fbe69296ce94276e6cb9eb978c86e0708',
    }

    r = requests.post(
        url, data=text.encode('utf-8'), headers=headers)

    return r.content.decode("utf-8")


# current_date = datetime.date.today()
# date_string = current_date.strftime("%Y-%m-%d")
# text = 'Сайн байна уу? Оройн мэнд. Өнөөдөр '+date_string
# synthesize(normalize(text))

# voiceRecord()
# transcribe("output.wav")
print(transcribe('Altanchimeg 1.mp3'))
