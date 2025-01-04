import os
import pyaudio

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt
from backend.speech_recognizer import SpeechRecognitionService
from backend.translator import TranslatorService
from backend.tts import TextToSpeechService
from frontend.config import Languages, Voice_Languages
from resources.styles import LABEL_STYLE, BUTTON_STYLE, COMBOBOX_STYLE, TEXT_EDIT_STYLE
from PyQt5.QtWidgets import QComboBox, QHBoxLayout, QPushButton, QLabel, QTextEdit, QVBoxLayout, QWidget


# noinspection PyUnresolvedReferences,PyAttributeOutsideInit
class PyQtGui(QMainWindow):
	def __init__(self):
		super().__init__()
		# Initialize Services
		self.speech_service = SpeechRecognitionService()
		self.translator_service = TranslatorService()
		self.tts_service = TextToSpeechService()

		self.init_ui()

		self.recognition_language = 'en-US'
		self.input_language = None
		self.output_language = None
		self.voice_name = None

		self.languages = Languages
		self.voice_languages = Voice_Languages

	def init_ui(self):
		self.label = QLabel("", self)
		self.label.setAlignment(Qt.AlignCenter)

		self.text_output = QTextEdit(self)
		self.text_output.setReadOnly(True)

		self.input_language_selector = QComboBox(self)
		self.input_language_selector.addItem("")
		for language in Languages.keys():
			self.input_language_selector.addItem(language)
		"""self.input_language_selector.addItem("English")
		self.input_language_selector.addItem("Spanish")
		self.input_language_selector.addItem("Bosnian")"""

		self.translation_language_selector = QComboBox(self)
		self.translation_language_selector.addItem("")
		for language, code in Languages.items():
			self.translation_language_selector.addItem(language, code)
		"""self.translation_language_selector.addItem("English", "en-US")
		self.translation_language_selector.addItem("Spanish", "es-US")
		self.translation_language_selector.addItem("Bosnian", "sr-RS")"""

		self.input_language_selector.setCurrentIndex(0)
		self.input_language_selector.setItemText(0, "Select Your Spoken Language")
		self.translation_language_selector.setCurrentIndex(0)
		self.translation_language_selector.setItemText(0, "Select Your Translation Language")

		self.reset_app_button = QPushButton("Restart Translator", self)
		self.set_input_output_languages_button = QPushButton("Set Your Spoken and Translation Languages", self)
		self.set_input_output_languages_button.clicked.connect(self.select_languages)
		self.start_translation_service_button = QPushButton("Start Translating", self)
		self.start_translation_service_button.clicked.connect(self.translate_speech)
		self.start_translation_service_button.hide()
		self.exit_button = QPushButton("Exit", self)
		self.exit_button.clicked.connect(self.close)

		button_layout = QHBoxLayout()
		button_layout.addWidget(self.reset_app_button)
		button_layout.addWidget(self.set_input_output_languages_button)
		button_layout.addWidget(self.start_translation_service_button)
		button_layout.addWidget(self.exit_button)

		layout = QVBoxLayout()
		layout.addWidget(self.label)
		layout.addWidget(self.text_output)
		layout.addWidget(self.input_language_selector)
		layout.addWidget(self.translation_language_selector)
		layout.addLayout(button_layout)
		self.setLayout(layout)

		container = QWidget()
		container.setLayout(layout)
		self.setCentralWidget(container)

		self.configure_widget_stylesheets()

	def configure_widget_stylesheets(self):
		self.label.setStyleSheet(LABEL_STYLE)
		self.text_output.setStyleSheet(TEXT_EDIT_STYLE)
		self.input_language_selector.setStyleSheet(COMBOBOX_STYLE)
		self.translation_language_selector.setStyleSheet(COMBOBOX_STYLE)
		self.set_input_output_languages_button.setStyleSheet(BUTTON_STYLE)
		self.start_translation_service_button.setStyleSheet(BUTTON_STYLE)
		self.exit_button.setStyleSheet(BUTTON_STYLE)
		self.reset_app_button.setStyleSheet(BUTTON_STYLE)

	def update_text_output(self):
		input_language = self.input_language_selector.currentText()
		output_language = self.translation_language_selector.currentText()

		self.text_output.setText(f"Translate {input_language} to {output_language}\nBegin Speaking After The Beep!")

	def set_languages(self, input_lang, output_lang):
		self.input_language = self.languages[input_lang]
		self.output_language = self.languages[output_lang]
		self.voice_name = self.voice_languages[output_lang]
		self.update_text_output()

	def select_languages(self):
		input_lang = self.input_language_selector.currentText()
		output_lang = self.translation_language_selector.currentText()

		if input_lang not in self.languages or output_lang not in self.languages:
			if input_lang not in self.languages:
				self.text_output.setText("Please Select Your Spoken Language")
			elif output_lang not in self.languages:
				self.text_output.setText("Please Select Your Translation Language")
			return

		self.input_language_selector.hide()
		self.translation_language_selector.hide()
		self.set_languages(input_lang, output_lang)

		self.set_input_output_languages_button.hide()
		self.start_translation_service_button.show()
		"""# INPUT ENGLISH
		if input_lang == "English" and output_lang == "Spanish":
			self.input_language_selector.hide()
			self.translation_language_selector.hide()
			self.set_languages(input_lang, output_lang)
		elif input_lang == "English" and output_lang == "Bosnian":
			self.input_language_selector.hide()
			self.translation_language_selector.hide()
			self.set_languages(input_lang, output_lang)
		# INPUT SPANISH
		elif input_lang == "Spanish" and output_lang == "English":
			self.input_language_selector.hide()
			self.translation_language_selector.hide()
			self.set_languages(input_lang, output_lang)
		elif input_lang == "Spanish" and output_lang == "Bosnian":
			self.input_language_selector.hide()
			self.translation_language_selector.hide()
			self.set_languages(input_lang, output_lang)
		# INPUT BOSNIAN
		elif input_lang == "Bosnian" and output_lang == "English":
			self.input_language_selector.hide()
			self.translation_language_selector.hide()
			self.set_languages(input_lang, output_lang)
		elif input_lang == "Bosnian" and output_lang == "Spanish":
			self.input_language_selector.hide()
			self.translation_language_selector.hide()
			self.set_languages(input_lang, output_lang)
		else:
			self.text_output.setText("Please Select Your Input and/or Output Language To Continue!")"""


	def translate_speech(self):
		# Recognize speech using the input language
		text, error = self.speech_service.recognize_speech(language=self.input_language)

		# If there's an error in speech recognition, display the error message
		if error:
			self.label.setText(f"Error: {error}")
			return print("program errored out")# Exit if there was an error

		# Translate the recognized speech
		# Extract the first two characters from the output language (e.g., 'en' from 'en-US')
		target_lang_code = self.output_language[:2]
		# Use the dynamically selected output language for translation
		translated_text = self.translator_service.translated_text(target_lang_code, text)
		# If there's an error in translation, display the error message
		if error:
			self.label.setText(f"Error translating text: {error}")
			return

		# Update the text output with the translated text
		self.text_output.setText(translated_text[0])

		# Now, call the speak_text with the translated text
		self.speak_text(self.output_language) # Automatically trigger speech synthesis


	def speak_text(self, language_code):
		text = self.text_output.toPlainText()
		if not text.strip():
			self.label.setText("No text to speak!")
			return

		# Use the TTS service to generate speech
		audio_file, error = self.tts_service.speak_text(text, language_code, name=self.voice_name)
		if error:
			self.label.setText(f"Error: {error}")
			return # Exit if there's an error in speech synthesis

		# Automatically play the generated audio once speech synthesis is complete
		self.play_audio(audio_file) # Trigger the play_audio function

	# noinspection PyMethodMayBeStatic
	def play_audio(self, audio_file):
		"""Play the generated audio file."""
		p = pyaudio.PyAudio()
		with open(audio_file, 'rb') as audio:
			stream = p.open(format=pyaudio.paInt16,
				            channels=1,
				            rate=24000,
				            output=True)
			data = audio.read(1024)
			while data:
				stream.write(data)
				data = audio.read(1024)
			stream.stop_stream()
			stream.close()
		p.terminate()
		os.remove(audio_file)


	def run(self):
		self.show()

	def exit(self):
		self.close()

if __name__ == '__main__':
	app = QApplication([])
	window = PyQtGui()
	window.run()
	app.exec_()
