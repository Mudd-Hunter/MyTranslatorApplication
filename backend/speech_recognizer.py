import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play

class SpeechRecognitionService:
    def __init__(self):
        self.speech_recognizer = sr.Recognizer()
        self.language = None

    def recognize_speech(self, language):
        self.language = language

        if not self.language:
            return None, "Language Not Set!"

        recognizer = self.speech_recognizer
        with sr.Microphone() as source:
            beep_sound = AudioSegment.from_file('./resources/beep1.wav', 'rb')
            start_sound = beep_sound.get_sample_slice(1000, 8000)
            play(start_sound)

            audio = recognizer.listen(source, timeout=5)
            # noinspection PyUnresolvedReferences
            text = recognizer.recognize_google(audio, language=self.language)
            return text, None