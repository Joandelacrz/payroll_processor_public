# 📑 Payroll Processor API  
A **Dockerized Flask Web API** for processing payroll data from a CSV file, generating **paystub PDFs**, and sending them via **email**.

## 🚀 Features
- 🔐 **User authentication** (via credentials in query parameters).
- 📂 **CSV file upload** containing payroll data.
- 📄 **Dynamic PDF generation** with company logo.
- 🌎 **Multi-language support** (`do` for Spanish, `USA` for English).
- ✉️ **Emailing generated paystubs** to employees.
- 🐳 **Dockerized environment** (no manual setup required).

---

## 🛠️ Installation & Setup

### **1️⃣ Clone the Repository**
git clone https://github.com/Joandelacrz/payroll_processor_public 
cd payroll_processor

2️⃣ Set Up Environment Variables
Create a .env file in the root of the project with:
SMTP_SERVER=smtp.example.com
SMTP_PORT=587
SMTP_USERNAME=your-email@example.com
SMTP_PASSWORD=yourpassword
EMAIL_FROM=your-email@example.com

Build & Run with Docker
Build the Docker Image
- docker build -t payroll-api .

Run the Container
- docker run -it --rm -p 3000:3000 --env-file .env payroll-api

🔐 Authentication
Username: user
Password: pwd
Authentication is required for all API requests using the credentials query parameter.

API request
curl.exe -F "file=@payroll.csv" "http://localhost:3000/process?country=do&credentials=user+pwd&company=atdev"

Response example
{
  "sent_emails": [
    {"email": "user@example.com", "timestamp": "2025-02-12T14:00:00Z"},
    {"email": "another@example.com", "timestamp": "2025-02-12T14:02:00Z"}
  ]
}

📖 API Workflow
1️⃣ User Uploads CSV

Sends a POST request with payroll data.
2️⃣ API Processes the CSV

Extracts payroll details.
Generates a paystub PDF for each employee.
3️⃣ Email Sent

PDF is attached and sent to the employee’s email.
4️⃣ JSON Response

Returns a list of successfully sent emails.
🛠️ Technologies Used
🐍 Python (Flask) – Web API
📜 ReportLab – PDF generation
🐳 Docker – Containerization
✉️ Flask-Mail – Sending emails
📊 Pandas – Processing CSV files
