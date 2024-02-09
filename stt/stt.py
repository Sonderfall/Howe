from google.cloud import speech_v2
from google.oauth2 import service_account

def listen(callback):
    credentials = service_account.Credentials.from_service_account_file('config/gcloud.json')
    # credentials = service_account.Credentials
    client = speech_v2.SpeechClient(credentials=credentials)

    # Initialize request argument(s)
    request = speech_v2.RecognizeRequest(
        content=b'content_blob',
        recognizer="recognizer_value",
    )

    # Synchronous speech recognition request
    response = client.recognize(request=request)

    for _, r in enumerate(response.results):
        for _, a in enumerate(r.alternatives):
            print(a.words)

    return response

if __name__ == "__main__":
    listen(None)