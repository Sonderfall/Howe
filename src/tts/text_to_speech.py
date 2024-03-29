from google.cloud import texttospeech
from google.oauth2 import service_account

from player import play_in_browser, play

# Available voices
# https://cloud.google.com/text-to-speech/docs/voices?hl=fr
__VOICE_GOOGLE_1 = {
    "name": "fr-FR-Wavenet-B",
    "gender": texttospeech.SsmlVoiceGender.MALE,
}


def say(utterance: str, mode: str = "sound_only"):
    if utterance is None:
        return

    filepath = "output.mp3"

    __synthesize(utterance, __VOICE_GOOGLE_1, filepath)

    if mode == "display":
        play_in_browser()
    elif mode == "sound_only":
        play(filepath)


def __synthesize(utterance: str, voice: dict, output: str):
    # Create credentials
    credentials = service_account.Credentials.from_service_account_file(
        "config/gcloud.json"
    )

    # Instantiates a client
    client = texttospeech.TextToSpeechClient(credentials=credentials)

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=utterance)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code="fr-FR",
        ssml_gender=voice["gender"],
        name=voice["name"],
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(output, "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)


if __name__ == "__main__":
    say("Bonjour, je m'appelle trololololo")
