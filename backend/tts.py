import os
import tempfile
from google.cloud import texttospeech

# Set up the Google Cloud Credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(os.path.dirname(__file__),
                                                            '../my-translation-app-credentials.json')


# noinspection PyTypeChecker
class TextToSpeechService:
	def __init__(self):
		self.tts_client = texttospeech.TextToSpeechClient()

	def speak_text(self, text, language_code, name):
		"""Convert text to speech and return the audio file path."""
		if not text.strip():
			return None, "No text to speak!"

		try:
			synthesis_input = texttospeech.SynthesisInput(text=text)
			voice = texttospeech.VoiceSelectionParams(
					language_code=language_code,
					name=f"{language_code}-{name}",
					ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
					)

			audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.LINEAR16)

			# Generate speech from text
			response = self.tts_client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

			# Save the generated audio to a temporary file
			with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_wave:
				tmp_wave.write(response.audio_content)
				tmp_wave_path = tmp_wave.name

			return tmp_wave_path, None

		except Exception as e:
			return None, f"Error Generating Speech: {e}"
