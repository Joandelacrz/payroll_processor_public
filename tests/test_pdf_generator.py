import os
import tempfile
import pytest
from app.pdf_generator import generate_paystub

@pytest.fixture
def sample_row():
    return {
        "full_name": "John Doe",
        "email": "john@example.com",
        "position": "Engineer",
        "gross_salary": "5000",
        "gross_payment": "4800",
        "net_payment": "4500",
        "health_discount_amount": "200",
        "social_discount_amount": "100",
        "taxes_discount_amount": "150",
        "other_discount_amount": "50",
        "period": "January 2025"
    }

@pytest.fixture(autouse=True)
def ensure_tmp_dir(monkeypatch):
    tmp_dir = "/tmp"
    if not os.path.exists(tmp_dir):
        try:
            os.makedirs(tmp_dir, exist_ok=True)
        except Exception as e:
            pytest.skip(f"Skipping test because cannot create directory {tmp_dir}: {e}")

def test_generate_paystub_creates_file(sample_row, monkeypatch):
    import os
    # Save the original os.path.exists function
    original_exists = os.path.exists
    # Monkeypatch os.path.exists so that when the logo file is checked, it returns False,
    # but for any other path, it calls the original os.path.exists.
    monkeypatch.setattr("os.path.exists", lambda path: False if "atdev.png" in path else original_exists(path))
    
    pdf_path = generate_paystub(sample_row, "do", "TestCompany")
    # Check that the PDF file was created.
    assert os.path.exists(pdf_path)
    # Optionally, remove the created PDF file.
    os.remove(pdf_path)

