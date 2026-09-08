"""
OSINT Cyber Guardian - Modul Manajemen API Key & Konfigurasi
"""
import os
import streamlit as st
from dotenv import load_dotenv
from pathlib import Path

# Path absolut ke file .env di folder project
_PROJECT_DIR = Path(__file__).parent.parent
_ENV_FILE = _PROJECT_DIR / ".env"

# Load .env saat modul pertama kali diimport
load_dotenv(dotenv_path=str(_ENV_FILE), override=False)


def load_keys_from_env():
    """Load API keys dari file .env ke session state.
    Hanya mengisi jika session state benar-benar belum diisi
    (bukan setelah user menyimpan secara manual).
    """
    # Re-load .env agar nilai terbaru terbaca
    load_dotenv(dotenv_path=str(_ENV_FILE), override=True)

    defaults = {
        "google_api_key": os.getenv("GOOGLE_API_KEY", ""),
        "google_cx": os.getenv("GOOGLE_CX", ""),
        "hibp_api_key": os.getenv("HIBP_API_KEY", ""),
        "serp_api_key": os.getenv("SERP_API_KEY", ""),
    }
    for key, val in defaults.items():
        if key not in st.session_state or not st.session_state[key]:
            st.session_state[key] = val


def get_api_key(key_name: str) -> str:
    """Ambil API key dari session state."""
    return st.session_state.get(key_name, "")


def has_google_api() -> bool:
    return bool(get_api_key("google_api_key") and get_api_key("google_cx"))


def has_hibp_api() -> bool:
    return bool(get_api_key("hibp_api_key"))


def save_api_keys(google_api_key: str, google_cx: str, hibp_api_key: str, serp_api_key: str):
    """Simpan API key ke session state."""
    st.session_state["google_api_key"] = google_api_key.strip()
    st.session_state["google_cx"] = google_cx.strip()
    st.session_state["hibp_api_key"] = hibp_api_key.strip()
    st.session_state["serp_api_key"] = serp_api_key.strip()


def save_to_env_file(google_api_key: str, google_cx: str, hibp_api_key: str, serp_api_key: str):
    """Tulis API keys ke file .env lokal (path absolut, permanen)."""
    env_content = f"""# OSINT Cyber Guardian - API Configuration
GOOGLE_API_KEY={google_api_key.strip()}
GOOGLE_CX={google_cx.strip()}
HIBP_API_KEY={hibp_api_key.strip()}
SERP_API_KEY={serp_api_key.strip()}
"""
    try:
        with open(str(_ENV_FILE), "w", encoding="utf-8") as f:
            f.write(env_content)

        # Reload agar session langsung pakai nilai baru
        load_dotenv(dotenv_path=str(_ENV_FILE), override=True)
        os.environ["GOOGLE_API_KEY"] = google_api_key.strip()
        os.environ["GOOGLE_CX"] = google_cx.strip()
        os.environ["HIBP_API_KEY"] = hibp_api_key.strip()
        os.environ["SERP_API_KEY"] = serp_api_key.strip()

        # Simpan ke session state sekaligus
        save_api_keys(google_api_key, google_cx, hibp_api_key, serp_api_key)

        return True, f"✅ API keys berhasil disimpan ke {_ENV_FILE}"
    except Exception as e:
        return False, f"Gagal menyimpan .env: {str(e)}"


def get_api_status() -> dict:
    """Kembalikan status konfigurasi setiap API."""
    return {
        "Real OSINT Scraper": True,  # Selalu aktif gratis (DuckDuckGo + Bing)
        "Google API (Opsional)": has_google_api(),
        "HIBP API (Opsional)": has_hibp_api(),
    }
