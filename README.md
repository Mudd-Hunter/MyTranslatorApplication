# Speech Translation Application

This is a Python-based application that allows users to speak in one language, have the speech recognized, translated into another language, and then converted into speech in the target language. The application uses Google Cloud services for translation and text-to-speech, along with speech recognition libraries for capturing and processing spoken input.

## Features

- **Speech Recognition**: Recognize speech in multiple languages.
- **Translation**: Translate recognized speech into a specified target language.
- **Text-to-Speech**: Convert the translated text into speech, with multiple voice options.
- **Multi-Language Support**: Select input and output languages from a configurable list.
- **PyQt5 GUI**: A user-friendly interface to interact with the application.

## Requirements

Ensure the following dependencies are installed via `pip`:

```bash
google~=3.0.0
protobuf~=5.29.2
SpeechRecognition~=3.13.0
pydub~=0.25.1
PyQt5~=5.15.11
PyAudio~=0.2.14
Kivy~=2.3.1
```
You can install them with:

```bash
pip install -r requirements.txt
```

## Setup

### Google Cloud API Credentials

Before running the application, you need to set up Google Cloud API credentials. Make sure you have the appropriate credentials for the following services:
(See the GOOGLECREDENTIALSSETUP.md file int the backend directory)

### Google Cloud Translation API

### Google Cloud Text-to-Speech API

Set the credentials in the my-translation-app-credentials.json file and update the environment variable in the backend code:

## Python Code To Set The Credentials 
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(os.path.dirname(__file__), '../my-translation-app-credentials.json')

### Language Configuration
You can modify the language settings in the frontend/config.py file:

### Speech Recognition Languages: 
A list of supported languages for speech recognition.

Google TTS Voices: A list of available voices for text-to-speech conversion.

Both lists are also available in the resources directory. You can reference them to add any languages or voices to the configuration as desired.

### Running the Application
Run the main application using:

```bash
python main.py
```

This will launch the PyQt5 GUI, allowing you to select input and output languages, start the translation process, and hear the translated speech.

## GUI Overview
### Language Selection: 
Choose the language you will speak (input language) and the language into which you want to translate (output language).

### Translate Button: 
Start translating your speech after selecting languages.

### Restart Button: 
Reset the translator for new input/output language selection.

## Contribution
Feel free to fork this repository, open issues, and create pull requests. Contributions are welcome!
