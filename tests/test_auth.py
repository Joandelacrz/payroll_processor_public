# tests/test_auth.py
import pytest
from app.auth import check_auth

def test_check_auth_valid(monkeypatch):
    monkeypatch.setenv("API_USER", "user")
    monkeypatch.setenv("API_PWD", "pwd")
    assert check_auth("user", "pwd") is True

def test_check_auth_invalid(monkeypatch):
    monkeypatch.setenv("API_USER", "user")
    monkeypatch.setenv("API_PWD", "pwd")
    assert check_auth("wrong", "creds") is False
