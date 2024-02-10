from google.cloud import speech
from google.oauth2 import service_account

def listen():
    # Create credentials
    credentials = service_account.Credentials.from_service_account_file('config/gcloud.json')

    client = speech.SpeechClient(credentials=credentials)

    with open('output.mp3', 'rb') as f:
        data = f.read()

    audio = speech.RecognitionAudio(content=data)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=16000,
        language_code="fr-FR",
    )

    # Synchronous speech recognition request
    response = client.recognize(config=config, audio=audio)

    print(response)

    for result in response.results:
        print(f"Transcript: {result.alternatives[0].transcript}")

if __name__ == "__main__":
    listen()