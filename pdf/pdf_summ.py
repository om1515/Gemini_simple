API_KEY = "AIzaSyAG0o2KrxbXbsdqeyZ5rz9NpWDIRTk8Rtc"



# from google import genai
# from google.genai import types
# import pathlib

# # Set your API key

# # Initialize the Gemini client
# client = genai.Client(api_key=API_KEY)

# # Path to your locally stored PDF
# pdf_path = "/Users/pikachu/Desktop/everything/create/public_docs/DBMS-Lec3.pdf"

# # Read the PDF file
# pdf_file = pathlib.Path(pdf_path)

# while True:
#     # Prompt the user for a question
#     user_input = input("Ask a question about the PDF (or type 'exit' to quit): ")
    
#     # Exit condition
#     if user_input.lower() == "exit":
#         print("Exiting program...")
#         break
    
#     # Generate content using Gemini API
#     response = client.models.generate_content(
#         model="gemini-1.5-flash",
#         contents=[
#             types.Part.from_bytes(
#                 data=pdf_file.read_bytes(),
#                 mime_type='application/pdf',
#             ),
#             user_input
#         ]
#     )
    
#     # Print the response
#     print("Response:", response.text)





import os
import pathlib
import logging
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Set up Flask app
app = Flask(__name__)

# Configure file upload folder
UPLOAD_FOLDER = "/Users/pikachu/Desktop/everything/create/Era/google/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize Gemini AI API
if not API_KEY:
    raise ValueError("API key not found. Set GEMINI_API_KEY in .env file.")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Store uploaded PDFs
uploaded_pdfs = []

@app.route("/", methods=["GET", "POST"])
def index():
    global uploaded_pdfs

    if request.method == "POST":
        if "pdf" in request.files:
            pdf_file = request.files["pdf"]
            if pdf_file.filename != "":
                filename = secure_filename(pdf_file.filename)
                pdf_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                pdf_file.save(pdf_path)
                uploaded_pdfs.append(filename)  # Store the filename

    return render_template("index.html", pdf_uploaded=bool(uploaded_pdfs), uploaded_pdfs=uploaded_pdfs)


@app.route("/remove/<filename>", methods=["POST"])
def remove_file(filename):
    """Delete a file from the uploads folder and update the list."""
    global uploaded_pdfs

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    if os.path.exists(file_path):
        os.remove(file_path)  # Delete file
        uploaded_pdfs.remove(filename)  # Remove from list

    return redirect(url_for("index"))


@app.route("/ask", methods=["POST"])
def ask():
    """Handles AI-based question answering from the last uploaded PDF."""
    global uploaded_pdfs

    if not uploaded_pdfs:
        return "No PDF uploaded yet.", 400

    user_question = request.form["question"]

    # Process the latest uploaded PDF
    latest_pdf = os.path.join(app.config["UPLOAD_FOLDER"], uploaded_pdfs[-1])  # Get the last uploaded file
    pdf_file = pathlib.Path(latest_pdf)

    # Generate response using Gemini AI
    try:
        response = model.generate_content([
            {
                "mime_type": "application/pdf",
                "data": pdf_file.read_bytes(),
            },
            user_question
        ])
        return response.text if response.text else "No relevant answer found."

    except Exception as e:
        logging.error(f"Error while processing AI response: {e}")
        return "Error processing your request.", 500


if __name__ == "__main__":
    app.run(debug=True)
