import cv2
import PIL.Image
import numpy as np
import time
import sys
from google import genai

# Initialize webcam
cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    print("Error: Could not open webcam")
    sys.exit(1)

print("Press 'C' to capture an image and analyze it.")
captured_image = None

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame from webcam")
        break
    
    cv2.imshow('Webcam Feed', frame)
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord('c') or key == ord('C'):
        print("Image captured!")
        captured_image = frame.copy()
        break
    
    if key == 27:  # Press 'Esc' to exit
        print("Exiting without capturing.")
        cap.release()
        cv2.destroyAllWindows()
        sys.exit(0)

cap.release()
cv2.destroyAllWindows()

# Check if an image was captured
if captured_image is None:
    print("No image captured.")
    sys.exit(1)

# Convert BGR to RGB
rgb_frame = cv2.cvtColor(captured_image, cv2.COLOR_BGR2RGB)

# Convert to PIL Image
pil_image = PIL.Image.fromarray(rgb_frame)

# Initialize Google AI client
client = genai.Client(api_key="AIzaSyAG0o2KrxbXbsdqeyZ5rz9NpWDIRTk8Rtc")

# Get the user's question
user_question = input("What would you like to ask about the image? ")

# Generate content with Gemini using user's question
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=[user_question, pil_image]
)

# Print the response
print("\nAI Response:")
print(response.text)