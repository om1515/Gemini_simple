from RealtimeSTT import AudioToTextRecorder
import google.generativeai as genai
import simpleaudio as sa
import requests

# Configure Gemini API
genai.configure(api_key="AIzaSyAG0o2KrxbXbsdqeyZ5rz9NpWDIRTk8Rtc")

def get_audio_response(text):
    model = genai.GenerativeModel("models/gemini-2.0-flash-exp")
    response = model.generate_content(
        text,
        generation_config={
            "responseModalities": ["audio"],
            "speechConfig": {
                "voiceConfig": {"prebuiltVoiceConfig": {"voiceName": "Kore"}}
            },
        },
    )
    
    audio_url = response.audio  # Assuming the API returns an audio URL
    if audio_url:
        audio_data = requests.get(audio_url).content
        with open("response.wav", "wb") as audio_file:
            audio_file.write(audio_data)
        play_audio("response.wav")


def play_audio(filename):
    wave_obj = sa.WaveObject.from_wave_file(filename)
    play_obj = wave_obj.play()
    play_obj.wait_done()


def process_text(text):
    print("User said:", text)
    get_audio_response(text)


if __name__ == "__main__":
    recorder = AudioToTextRecorder()
    while True:
        recorder.text(process_text)
