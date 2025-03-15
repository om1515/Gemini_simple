

from google import genai
from google.genai import types
import cv2
import PIL.Image
import numpy as np
import time
import sys
import os



# Initialize Google AI client
client = genai.Client(api_key="AIzaSyAG0o2KrxbXbsdqeyZ5rz9NpWDIRTk8Rtc")

# Get the user's question
user_question = input("What would you like to ask about the image? ")

# Get the image path directly
image_path = "/Users/pikachu/Desktop/everything/create/public_docs/WhatsApp Image 2025-02-20 at 21.09.54.jpeg"

# Check if the file exists
if not os.path.isfile(image_path):
    print("Error: File does not exist.")
    sys.exit(1)

# Load the image
frame = cv2.imread(image_path)

# Check if image was successfully loaded
if frame is None:
    print("Error: Could not read the image.")
    sys.exit(1)

# Display the image
cv2.imshow('Image', frame)

# Convert BGR to RGB
rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
# Convert to PIL Image
pil_image = PIL.Image.fromarray(rgb_frame)

# Generate content with Gemini using user's question
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=[user_question, pil_image]
)

print(response.text)

# Add a small delay to prevent overwhelming the API
time.sleep(2)

# Wait for user to press a key to close the window
cv2.waitKey(0)
cv2.destroyAllWindows()