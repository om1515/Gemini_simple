import os
from google import genai
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Initialize Gemini API client
client = genai.Client(api_key=api_key)

# YouTube video URL
youtube_url = "https://www.youtube.com/watch?v=9hE5-98ZeCg"  # Replace with the actual YouTube URL

# Prompt Gemini to summarize the video
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=[
        "Can you summarize this video?",
        genai.types.Part(file_data=genai.types.FileData(file_uri=youtube_url))
    ]
)

print("\nYouTube Video Summary:")
print(response.text)
