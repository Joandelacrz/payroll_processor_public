import pytest
import smtplib
from unittest.mock import patch, MagicMock, mock_open
from app.email_sender import send_email

@pytest.fixture
def email_params():
    return {
        "recipient": "test@example.com",
        "pdf_path": "test.pdf"
    }

@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv("SENDER_EMAIL", "test_sender@example.com")
    monkeypatch.setenv("SENDER_PASSWORD", "testpassword")
    monkeypatch.setenv("SMTP_SERVER", "smtp.test.com")
    monkeypatch.setenv("SMTP_PORT", "587")

@patch("builtins.open", new_callable=mock_open, read_data=b"Fake PDF content")
@patch("app.email_sender.smtplib.SMTP", side_effect=smtplib.SMTPException("SMTP error"))
def test_send_email_failure(mock_smtp, mock_file, email_params, mock_env, capsys):
    """Test email sending failure due to SMTP error"""
    send_email(**email_params)
    
    # Capturar la salida estándar
    captured = capsys.readouterr()
    
    # Verificar si el mensaje de error esperado está en la salida
    assert "Error sending email to test@example.com: SMTP error" in captured.out
