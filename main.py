import csv
import datetime
from flask import Flask, request, jsonify, abort
from app.pdf_generator import generate_paystub
from app.email_sender import send_email
from app.auth import check_auth

app = Flask(__name__)

@app.route("/process", methods=["POST"])
def process_payroll():
    """Processes the payroll CSV and sends emails with attached paystubs."""
    # Authentication check
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return jsonify({"error": "Unauthorized"}), 401

    # Ensure a file is uploaded
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    content = file.read().decode("utf-8").strip()  # Read and clean content
    csv_lines = content.splitlines()

    # Check if CSV is empty or contains only empty lines
    if not csv_lines or all(not line.strip() for line in csv_lines):
        abort(500, "Payroll CSV is empty. No valid data provided.")

    reader = csv.DictReader(csv_lines)
    rows = list(reader)

    # Ensure there are valid data rows (not just headers)
    if not rows or all(all(not (v and v.strip()) for v in row.values()) for row in rows):
        abort(500, "Payroll CSV has no valid data rows.")

    sent_emails = []
    for row in rows:
        pdf_path = generate_paystub(
            row,
            request.args.get("country", "do"),
            request.args.get("company", "default")
        )
        send_email(row.get("email"), pdf_path)
        sent_emails.append({"email": row.get("email"), "sent_at": str(datetime.datetime.now())})

    return jsonify({"success": True, "emails_sent": sent_emails})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
