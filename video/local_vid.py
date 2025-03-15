import os
import time
from google import genai
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Initialize Gemini API client
client = genai.Client(api_key=api_key)

# Path to the local video file
video_path = "/Users/pikachu/Desktop/everything/create/Gemini_simple/video/test_video.mp4"  # Replace with the actual file path

# Upload the video file
print("Uploading file...")
video_file = client.files.upload(file=video_path)
print(f"Completed upload: {video_file.uri}")

# Wait until the file is processed
while video_file.state.name == "PROCESSING":
    print('.', end='', flush=True)
    time.sleep(1)
    video_file = client.files.get(name=video_file.name)

if video_file.state.name == "FAILED":
    raise ValueError("File upload failed.")

print("\nFile is ready for inference.")

# Prompt Gemini to summarize the video
response = client.models.generate_content(
    model="gemini-1.5-pro",
    contents=[
        video_file,
        "Summarize this video in a concise and informative way."
    ]
)

print("\nVideo Summary:")
print(response.text)
