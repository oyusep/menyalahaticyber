"""
OSINT Cyber Guardian - Modul Autentikasi & Manajemen Akses Admin (Internal)
Menyediakan fitur login screen, enkripsi password, sesi login, dan otorisasi role internal.
"""

import hashlib
import os
import streamlit as st
from datetime import datetime
from typing import Dict, Tuple, Optional

# Hash password menggunakan SHA-256 dengan salt standar
SALT = "OSINT_CYBER_GUARDIAN_SECURE_SALT_2026"


def hash_password(password: str) -> str:
    """Enkripsi password menggunakan SHA-256 + Salt."""
    salted = f"{SALT}:{password}"
    return hashlib.sha256(salted.encode("utf-8")).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifikasi kecocokan password polos dengan hash."""
    return hash_password(plain_password) == hashed_password


def is_authenticated() -> bool:
    """Cek apakah pengguna saat ini sudah terautentikasi sebagai Admin."""
    return bool(st.session_state.get("authenticated_user"))


def get_current_user() -> Optional[Dict]:
    """Ambil data admin yang sedang aktif di sesi."""
    return st.session_state.get("authenticated_user")


def login_user(user_dict: Dict):
    """Simpan status login ke session state."""
    st.session_state["authenticated_user"] = {
        "id": user_dict.get("id"),
        "username": user_dict.get("username"),
        "full_name": user_dict.get("full_name", "Admin Internal"),
        "role": user_dict.get("role", "operator"),
        "login_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def logout_user():
    """Hapus status login dari session state."""
    if "authenticated_user" in st.session_state:
        del st.session_state["authenticated_user"]
    st.rerun()


def render_login_screen():
    """
    Render Halaman Login Admin Internal (Cyber Glassmorphism Theme).
    Menghalangi seluruh akses aplikasi sebelum terautentikasi.
    """
    st.markdown("""
    <style>
    .login-container {
        max-width: 440px;
        margin: 60px auto 20px auto;
        background: #1E293B;
        border: 1px solid #334155;
        border-top: 3px solid #2563EB;
        border-radius: 12px;
        padding: 32px 28px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        text-align: center;
    }
    .login-badge {
        display: inline-block;
        background: rgba(37, 99, 235, 0.1);
        border: 1px solid rgba(37, 99, 235, 0.3);
        color: #60A5FA;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 1px;
        padding: 4px 12px;
        border-radius: 6px;
        margin-bottom: 16px;
        text-transform: uppercase;
    }
    .login-title {
        font-size: 1.4rem;
        font-weight: 800;
        color: #F8FAFC;
        margin-bottom: 6px;
    }
    .login-sub {
        font-size: 0.82rem;
        color: #94A3B8;
        margin-bottom: 24px;
        line-height: 1.4;
    }
    </style>
    """, unsafe_allow_html=True)

    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        st.markdown("""
        <div class="login-container">
            <div class="login-badge">🔒 Akses Khusus Internal</div>
            <div class="login-title">Menyalahati Cyber Intelligence</div>
            <div class="login-sub">Sistem Pendampingan Korban Doxing & Forensic Intelligence</div>
        </div>
        """, unsafe_allow_html=True)

        with st.form("form_admin_login", clear_on_submit=False):
            username_input = st.text_input(
                "👤 Username Admin",
                placeholder="Masukkan username...",
                key="login_user_input"
            )
            password_input = st.text_input(
                "🔑 Password",
                type="password",
                placeholder="Masukkan password...",
                key="login_pass_input"
            )

            st.markdown("<br>", unsafe_allow_html=True)
            btn_login = st.form_submit_button("🔓 Masuk ke Dashboard Admin", type="primary", use_container_width=True)

            if btn_login:
                if not username_input.strip() or not password_input.strip():
                    st.error("❌ Username dan Password wajib diisi!")
                else:
                    import modules.database as db
                    user = db.get_admin_user(username_input.strip())
                    if user and verify_password(password_input.strip(), user.get("password_hash", "")):
                        login_user(user)
                        db.update_admin_login_time(user["id"])
                        st.toast(f"✅ Selamat datang, {user.get('full_name', username_input)}!", icon="🔓")
                        st.rerun()
                    else:
                        st.error("❌ Username atau Password salah! Akses ditolak.")
