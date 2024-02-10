import wave
import struct

from google.cloud import speech
from google.oauth2 import service_account
from pvrecorder import PvRecorder


def listen() -> str:
    filepath = "input.mp3"

    record(filepath)

    return transcript(filepath)


def record(filepath: str):
    for index, device in enumerate(PvRecorder.get_available_devices()):
        print(f"[{index}] {device}")

    recorder = PvRecorder(device_index=-1, frame_length=512)
    audio = []

    try:
        recorder.start()

        while True:
            frame = recorder.read()
            audio.extend(frame)
    except KeyboardInterrupt:
        recorder.stop()

        with wave.open(filepath, "w") as f:
            f.setparams((1, 2, 16000, 512, "NONE", "NONE"))
            f.writeframes(struct.pack("h" * len(audio), *audio))

    finally:
        recorder.delete()


def transcript(filepath: str) -> str:
    # Create credentials
    credentials = service_account.Credentials.from_service_account_file(
        "config/gcloud.json"
    )

    client = speech.SpeechClient(credentials=credentials)

    with open(filepath, "rb") as f:
        data = f.read()

    audio = speech.RecognitionAudio(content=data)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
        sample_rate_hertz=16000,
        language_code="fr-FR",
    )

    # Synchronous speech recognition request
    response = client.recognize(config=config, audio=audio)

    print(response)

    for result in response.results:
        utterance = result.alternatives[0].transcript

        if utterance is not None:
            return utterance

    return None


if __name__ == "__main__":
    utterance = listen()

    print(f"Result: {utterance}")
