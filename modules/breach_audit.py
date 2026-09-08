"""
OSINT Cyber Guardian - HaveIBeenPwned Breach Audit
Memeriksa kebocoran data email/nomor via HIBP API v3
"""
import requests
import time
from typing import List, Dict, Optional


HIBP_BASE_URL = "https://haveibeenpwned.com/api/v3"
HIBP_HEADERS = {
    "User-Agent": "OSINT-CyberGuardian-AntiDoxing/1.0",
}


def check_email_breaches(email: str, api_key: str) -> Dict:
    """
    Cek apakah email pernah terlibat dalam kebocoran data via HIBP API.
    
    Returns:
        dict berisi 'breaches' (list) atau 'error' (str)
    """
    if not api_key:
        return {
            "success": False,
            "error": "HIBP API Key belum dikonfigurasi",
            "breaches": [],
            "demo_mode": True,
        }
    if not email or "@" not in email:
        return {"success": False, "error": "Format email tidak valid", "breaches": []}

    headers = {**HIBP_HEADERS, "hibp-api-key": api_key}
    url = f"{HIBP_BASE_URL}/breachedaccount/{email}"
    params = {"truncateResponse": "false"}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)

        if response.status_code == 200:
            breaches = response.json()
            return {
                "success": True,
                "breaches": [
                    {
                        "name": b.get("Name", "Unknown"),
                        "title": b.get("Title", "Unknown Service"),
                        "domain": b.get("Domain", ""),
                        "breach_date": b.get("BreachDate", ""),
                        "pwn_count": b.get("PwnCount", 0),
                        "data_classes": b.get("DataClasses", []),
                        "description": b.get("Description", ""),
                        "is_sensitive": b.get("IsSensitive", False),
                        "is_verified": b.get("IsVerified", True),
                    }
                    for b in breaches
                ],
                "total_breaches": len(breaches),
            }
        elif response.status_code == 404:
            return {
                "success": True,
                "breaches": [],
                "total_breaches": 0,
                "message": "Email tidak ditemukan dalam database kebocoran (Aman!)",
            }
        elif response.status_code == 401:
            return {"success": False, "error": "HIBP API Key tidak valid.", "breaches": []}
        elif response.status_code == 429:
            retry_after = response.headers.get("Retry-After", "60")
            return {
                "success": False,
                "error": f"Rate limit HIBP. Coba lagi dalam {retry_after} detik.",
                "breaches": [],
            }
        else:
            return {
                "success": False,
                "error": f"HIBP Error {response.status_code}: {response.text[:200]}",
                "breaches": [],
            }
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Koneksi timeout ke HIBP API.", "breaches": []}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Tidak dapat terhubung ke HIBP API.", "breaches": []}
    except Exception as e:
        return {"success": False, "error": f"Error: {str(e)}", "breaches": []}


def check_password_pwned(password_hash_prefix: str, api_key: str = "") -> Dict:
    """
    Cek apakah password (prefix SHA-1) ada di Pwned Passwords.
    Menggunakan k-anonymity - tidak mengirim password penuh.
    """
    url = f"https://api.pwnedpasswords.com/range/{password_hash_prefix[:5].upper()}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return {"success": True, "data": response.text}
        return {"success": False, "error": f"Error {response.status_code}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_all_breaches(api_key: str) -> Dict:
    """Ambil daftar semua breach yang ada di HIBP database."""
    headers = {**HIBP_HEADERS, "hibp-api-key": api_key}
    url = f"{HIBP_BASE_URL}/breaches"
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            return {"success": True, "breaches": response.json()}
        return {"success": False, "error": f"Error {response.status_code}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_mock_breaches(email: str) -> Dict:
    """Data mock untuk demo tanpa API key."""
    return {
        "success": True,
        "demo_mode": True,
        "breaches": [
            {
                "name": "Adobe",
                "title": "Adobe",
                "domain": "adobe.com",
                "breach_date": "2013-10-04",
                "pwn_count": 152445165,
                "data_classes": ["Email addresses", "Password hints", "Passwords", "Usernames"],
                "description": "Contoh data demo: Kebocoran Adobe 2013.",
                "is_sensitive": False,
                "is_verified": True,
            },
            {
                "name": "LinkedIn",
                "title": "LinkedIn",
                "domain": "linkedin.com",
                "breach_date": "2012-05-05",
                "pwn_count": 164611595,
                "data_classes": ["Email addresses", "Passwords"],
                "description": "Contoh data demo: Kebocoran LinkedIn 2012.",
                "is_sensitive": False,
                "is_verified": True,
            },
        ],
        "total_breaches": 2,
        "message": "⚠️ INI DATA DEMO. Masukkan HIBP API Key untuk hasil nyata.",
    }


def format_pwn_count(count: int) -> str:
    """Format angka korban kebocoran menjadi readable."""
    if count >= 1_000_000_000:
        return f"{count / 1_000_000_000:.1f}M"
    elif count >= 1_000_000:
        return f"{count / 1_000_000:.1f}Jt"
    elif count >= 1_000:
        return f"{count / 1_000:.0f}Rb"
    return str(count)


def get_severity_from_data_classes(data_classes: List[str]) -> str:
    """Tentukan tingkat keparahan berdasarkan jenis data yang bocor."""
    critical_data = {"passwords", "credit cards", "bank account numbers", "passport numbers", "social security numbers", "nik"}
    high_data = {"phone numbers", "physical addresses", "dates of birth", "geographic locations"}
    
    classes_lower = {d.lower() for d in data_classes}
    
    if classes_lower.intersection(critical_data):
        return "critical"
    elif classes_lower.intersection(high_data):
        return "high"
    return "medium"
