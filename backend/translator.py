import os
from google.cloud import translate_v2 as translate

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(os.path.dirname(__file__),
                                                            '../my-translation-app-credentials.json')

class TranslatorService:
	def __init__(self):
		# Initialize the Google Translate client
		self.translate_client = translate.Client()

	def translated_text(self, target_lang, spoken_text):
		"""Translate text to the target language."""
		if not spoken_text.strip():
			return None, "No Text to Translate!"

		try:
			translation = self.translate_client.translate(spoken_text, target_language=target_lang)
			return translation['translatedText'], None
		except Exception as e:
			return None, f"Error Translating Text: {e}"