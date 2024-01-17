import speech_recognition as sr

def continuous_listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")

        while True:
            try:
                # audio = recognizer.listen(source, timeout=5)
                # text = recognizer.recognize_google(audio)

                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                text = recognizer.recognize_sphinx(audio, language="mn")

                if text.lower() == "stop listening":
                    print("Stopping listening.")
                    break

                print("You said:", text)

            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))