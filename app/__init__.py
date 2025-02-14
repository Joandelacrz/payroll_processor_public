from flask import Flask, request, jsonify
from .email_sender import send_email  # Adjust if your file or function name differs

app = Flask(__name__)

@app.route("/process", methods=["POST"])
def process_payroll():
    # 1) Check credentials
    credentials = request.args.get("credentials")
    if credentials != "user pwd":
        return jsonify({"error": "Invalid credentials"}), 401

    # 2) Check if a file was uploaded
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    # 3) Process the file (simplified for the example)
    #    - In reality, you'd parse the CSV, generate PDFs, etc.
    uploaded_file = request.files["file"]
    # Do something with uploaded_file...

    # 4) Use your email-sending function (this will be monkeypatched in tests)
    #    We'll pretend we send emails to 2 employees:
    sent_emails = [
        send_email("john@example.com", None),
        send_email("jane@example.com", None)
    ]

    # 5) Return a JSON response with sent_emails
    return jsonify({"sent_emails": sent_emails}), 200
