import io
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def create_sample_csv():
    csv_content = "name,email,salary\nJohn Doe,john@example.com,5000\nJane Doe,jane@example.com,6000\n"
    return io.BytesIO(csv_content.encode('utf-8'))

def fake_send_email(recipient, pdf_file):
    return {"email": recipient, "timestamp": "2025-02-12T14:00:00Z"}

def test_process_valid_csv(client, monkeypatch):
    # Point monkeypatch to the correct location of send_email
    monkeypatch.setattr("app.email_sender.send_email", fake_send_email)

    data = {
        'file': (create_sample_csv(), 'payroll.csv')
    }
    response = client.post(
        '/process?country=do&credentials=user+pwd&company=atdev',
        data=data,
        content_type='multipart/form-data'
    )
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    json_data = response.get_json()
    assert "sent_emails" in json_data
    # We expect 2 emails (one per row in the CSV)
    assert len(json_data["sent_emails"]) == 2

def test_process_invalid_credentials(client):
    data = {
        'file': (create_sample_csv(), 'payroll.csv')
    }
    response = client.post(
        '/process?country=do&credentials=wrong+creds&company=atdev',
        data=data,
        content_type='multipart/form-data'
    )
    # Expect 401 when credentials are wrong
    assert response.status_code == 401, f"Expected 401, got {response.status_code}"

def test_process_missing_file(client):
    response = client.post(
        '/process?country=do&credentials=user+pwd&company=atdev',
        data={},  # No file provided
        content_type='multipart/form-data'
    )
    # Expect 400 when no file is uploaded
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
