import os
import pyaudio
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from backend.speech_recognizer import SpeechRecognitionService
from backend.translator import TranslatorService
from backend.tts import TextToSpeechService


# noinspection PyAttributeOutsideInit
class KivyGui(App):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.speech_service = SpeechRecognitionService()
		self.translator_service = TranslatorService()
		self.tts_service = TextToSpeechService()

		self.input_language = None
		self.output_language = None
		self.voice_name = None

		self.languages = {
			'English': 'en-US',
			'Spanish': 'es-US',
			'Bosnian': 'sr-RS',
		}

		self.voice_languages = {
			'English': 'Neural2-H',
			'Spanish': 'Neural2-A',
			'Bosnian': 'Standard-A',
		}

	def build(self):
		self.root = BoxLayout(orientation='vertical', padding=10, spacing=10)

		self.label = Label(text="", size_hint=(1, 0.2))
		self.text_output = TextInput(readonly=True, size_hint=(1, 0.5), multiline=True)

		self.input_language_selector = Spinner(
			text="Select Your Spoken Language",
			values=list(self.languages.keys()),
			size_hint=(1, 0.1)
		)

		self.translation_language_selector = Spinner(
			text="Select Your Translation Language",
			values=list(self.languages.keys()),
			size_hint=(1, 0.1)
		)

		self.set_languages_button = Button(
			text="Set Your Spoken and Translation Languages",
			size_hint=(1, 0.1)
		)
		self.set_languages_button.bind(on_press=self.select_languages)

		self.start_translation_service_button = Button(
			text="Start Translating",
			size_hint=(1, 0.1),
			disabled=True
		)
		self.start_translation_service_button.bind(on_press=self.translate_speech)

		self.reset_button = Button(
			text="Restart Translator",
			size_hint=(1, 0.1)
		)
		self.reset_button.bind(on_press=self.reset_app)

		self.exit_button = Button(
			text="Exit",
			size_hint=(1, 0.1)
		)
		self.exit_button.bind(on_press=self.stop)

		self.root.add_widget(self.label)
		self.root.add_widget(self.text_output)
		self.root.add_widget(self.input_language_selector)
		self.root.add_widget(self.translation_language_selector)
		self.root.add_widget(self.set_languages_button)
		self.root.add_widget(self.start_translation_service_button)
		self.root.add_widget(self.reset_button)
		self.root.add_widget(self.exit_button)

		return self.root

	def select_languages(self, instance):
		input_lang = self.input_language_selector.text
		output_lang = self.translation_language_selector.text

		if input_lang not in self.languages or output_lang not in self.languages:
			self.label.text = "Please select valid languages!"
			return

		self.input_language = self.languages[input_lang]
		self.output_language = self.languages[output_lang]
		self.voice_name = self.voice_languages[output_lang]

		self.label.text = f"Translating {input_lang} to {output_lang}. Begin speaking after the beep!"
		self.start_translation_service_button.disabled = False
		self.input_language_selector.disabled = True
		self.translation_language_selector.disabled = True
		self.set_languages_button.disabled = True
		self.translate_speech(instance)

	def translate_speech(self, instance):
		text, error = self.speech_service.recognize_speech(language=self.input_language)
		if error:
			self.label.text = f"Error: {error}"
			return

		target_lang_code = self.output_language[:2]
		translated_text = self.translator_service.translated_text(target_lang_code, text)
		if translated_text is None:
			self.label.text = "Error in translation!"
			return

		self.text_output.text = translated_text[0]
		self.speak_text(self.output_language)

	def speak_text(self, language_code):
		text = self.text_output.text
		if not text.strip():
			self.label.text = "No text to speak!"
			return

		audio_file, error = self.tts_service.speak_text(text, language_code, name=self.voice_name)
		if error:
			self.label.text = f"Error: {error}"
			return

		self.play_audio(audio_file)

	# noinspection PyMethodMayBeStatic
	def play_audio(self, audio_file):
		p = pyaudio.PyAudio()
		with open(audio_file, 'rb') as wave_file:
			stream = p.open(format=pyaudio.paInt16, channels=1, rate=24000, output=True)
			data = wave_file.read(1024)
			while data:
				stream.write(data)
				# noinspection PyUnresolvedReferences
				data = wave_file.read(1024)
			stream.stop_stream()
			stream.close()
		p.terminate()
		os.remove(audio_file)

	def reset_app(self, instance):
		self.input_language_selector.text = "Select Your Spoken Language"
		self.translation_language_selector.text = "Select Your Translation Language"
		self.label.text = ""
		self.text_output.text = ""
		self.start_translation_service_button.disabled = True
		self.input_language_selector.disabled = False
		self.translation_language_selector.disabled = False
		self.set_languages_button.disabled = False

if __name__ == "__main__":
	KivyGui().run()
