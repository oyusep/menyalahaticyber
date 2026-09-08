"""
modules/database.py
Database layer menggunakan SQLite untuk menyimpan semua riwayat tracking forensik.
Tidak perlu install apapun - SQLite sudah built-in Python.
"""

import sqlite3
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

# Path database di folder utama project
DB_PATH = Path(__file__).parent.parent / "forensik_data.db"


def get_connection():
    """Buka koneksi ke database SQLite."""
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row  # Akses kolom dengan nama
    return conn


def init_database():
    """Inisialisasi database dan buat semua tabel jika belum ada."""
    conn = get_connection()
    c = conn.cursor()

    # Tabel riwayat Diagnosa Jejak Digital
    c.execute("""
        CREATE TABLE IF NOT EXISTS scan_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            target_name TEXT NOT NULL,
            target_phone TEXT,
            target_email TEXT,
            target_instagram TEXT,
            target_tiktok TEXT,
            target_facebook TEXT,
            target_twitter TEXT,
            target_linkedin TEXT,
            spouse_family TEXT,
            keywords TEXT,
            risk_score INTEGER,
            risk_category TEXT,
            risk_color TEXT,
            dork_found INTEGER DEFAULT 0,
            breach_count INTEGER DEFAULT 0,
            social_platforms TEXT,
            status TEXT DEFAULT 'selesai',
            scan_mode TEXT DEFAULT 'real',
            result_json TEXT,
            notes TEXT
        )
    """)

    # Tabel riwayat Investigasi Nomor DC
    c.execute("""
        CREATE TABLE IF NOT EXISTS dc_investigations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            dc_phone TEXT NOT NULL,
            operator TEXT,
            region TEXT,
            phone_type TEXT,
            truecaller_name TEXT,
            is_spam INTEGER DEFAULT 0,
            getcontact_count INTEGER DEFAULT 0,
            has_fraud_report INTEGER DEFAULT 0,
            phone_score INTEGER DEFAULT 0,
            status TEXT DEFAULT 'selesai',
            result_json TEXT,
            notes TEXT
        )
    """)

    # Tabel riwayat Removal Requests (Lama/Legacy)
    c.execute("""
        CREATE TABLE IF NOT EXISTS removal_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            target_name TEXT,
            target_url TEXT,
            word_term TEXT,
            removal_type TEXT,
            status TEXT DEFAULT 'draft',
            notes TEXT
        )
    """)

    # Tabel Case Pembersihan Data & Removal Tracking (Baru & Terintegrasi)
    c.execute("""
        CREATE TABLE IF NOT EXISTS removal_cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_code TEXT UNIQUE NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            client_name TEXT NOT NULL,
            client_phone TEXT,
            target_url TEXT NOT NULL,
            target_snippet TEXT,
            target_keyword TEXT,
            platform TEXT,
            removal_type TEXT DEFAULT 'Google Outdated Content',
            status TEXT DEFAULT 'Draft',
            progress_percent INTEGER DEFAULT 10,
            ai_guidance TEXT,
            legal_text TEXT,
            last_checked_at TEXT,
            http_status_code INTEGER,
            is_indexed INTEGER DEFAULT 1,
            notes TEXT
        )
    """)

    # Tabel Log Riwayat Penanganan Case
    c.execute("""
        CREATE TABLE IF NOT EXISTS removal_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_id INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            action_type TEXT NOT NULL,
            old_status TEXT,
            new_status TEXT,
            description TEXT,
            actor TEXT DEFAULT 'Operator/AI System',
            FOREIGN KEY(case_id) REFERENCES removal_cases(id) ON DELETE CASCADE
        )
    """)

    # Tabel Admin Users (Autentikasi Internal)
    c.execute("""
        CREATE TABLE IF NOT EXISTS admin_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT NOT NULL,
            role TEXT DEFAULT 'operator',
            created_at TEXT NOT NULL,
            last_login TEXT
        )
    """)

    # Tabel Data Klien (Tracking Portfolio 360)
    c.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_code TEXT UNIQUE NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            full_name TEXT NOT NULL,
            nik TEXT,
            phone TEXT,
            email TEXT,
            address TEXT,
            emergency_contact TEXT,
            status TEXT DEFAULT 'Aktif',
            notes TEXT,
            created_by TEXT DEFAULT 'admin'
        )
    """)

    conn.commit()

    # Inisialisasi default admin jika belum ada
    c.execute("SELECT COUNT(*) as n FROM admin_users")
    if (c.fetchone()["n"] or 0) == 0:
        # Default pass: admin123 (hash SHA-256)
        # SALT: "OSINT_CYBER_GUARDIAN_SECURE_SALT_2026"
        import hashlib
        salt = "OSINT_CYBER_GUARDIAN_SECURE_SALT_2026"
        def_pass_hash = hashlib.sha256(f"{salt}:admin123".encode("utf-8")).hexdigest()
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("""
            INSERT INTO admin_users (username, password_hash, full_name, role, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, ("admin", def_pass_hash, "Administrator Utama", "superadmin", now_str))
        conn.commit()

    conn.close()


# ═══════════════════════════════════════════════════════════
# SCAN HISTORY - DIAGNOSA JEJAK DIGITAL
# ═══════════════════════════════════════════════════════════

def save_scan(
    target_name: str,
    target_phone: str = "",
    target_email: str = "",
    risk_score: int = 0,
    risk_category: str = "",
    risk_color: str = "",
    dork_found: int = 0,
    breach_count: int = 0,
    social_platforms: list = None,
    scan_mode: str = "real",
    result_json: dict = None,
    target_instagram: str = "",
    target_tiktok: str = "",
    target_facebook: str = "",
    target_twitter: str = "",
    target_linkedin: str = "",
    spouse_family: str = "",
    keywords: str = "",
) -> int:
    """Simpan hasil scan diagnosa ke database. Return ID record baru."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        INSERT INTO scan_history (
            created_at, target_name, target_phone, target_email,
            target_instagram, target_tiktok, target_facebook, target_twitter, target_linkedin,
            spouse_family, keywords,
            risk_score, risk_category, risk_color, dork_found, breach_count,
            social_platforms, scan_mode, result_json, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        target_name, target_phone, target_email,
        target_instagram, target_tiktok, target_facebook, target_twitter, target_linkedin,
        spouse_family, keywords,
        risk_score, risk_category, risk_color, dork_found, breach_count,
        json.dumps(social_platforms or []),
        scan_mode,
        json.dumps(result_json or {}),
        "selesai",
    ))
    new_id = c.lastrowid
    conn.commit()
    conn.close()
    return new_id


def get_scan_history(limit: int = 100) -> list:
    """Ambil semua riwayat scan, terbaru di atas."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT id, created_at, target_name, target_phone, target_email,
               risk_score, risk_category, risk_color, dork_found, breach_count,
               social_platforms, scan_mode, status, notes
        FROM scan_history
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows


def get_scan_detail(record_id: int) -> dict:
    """Ambil detail lengkap satu record scan."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM scan_history WHERE id = ?", (record_id,))
    row = c.fetchone()
    conn.close()
    if row:
        d = dict(row)
        try:
            d["result_json"] = json.loads(d.get("result_json") or "{}")
        except Exception:
            d["result_json"] = {}
        try:
            d["social_platforms"] = json.loads(d.get("social_platforms") or "[]")
        except Exception:
            d["social_platforms"] = []
        return d
    return {}


def delete_scan(record_id: int):
    """Hapus satu record scan."""
    conn = get_connection()
    conn.execute("DELETE FROM scan_history WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()


def delete_all_scans():
    """Hapus semua record scan."""
    conn = get_connection()
    conn.execute("DELETE FROM scan_history")
    conn.commit()
    conn.close()


def update_scan_notes(record_id: int, notes: str):
    """Update catatan/notes untuk satu record scan."""
    conn = get_connection()
    conn.execute("UPDATE scan_history SET notes = ? WHERE id = ?", (notes, record_id))
    conn.commit()
    conn.close()


# ═══════════════════════════════════════════════════════════
# DC INVESTIGATIONS - INVESTIGASI NOMOR DC
# ═══════════════════════════════════════════════════════════

def save_dc_investigation(
    dc_phone: str,
    operator: str = "",
    region: str = "",
    phone_type: str = "",
    truecaller_name: str = "",
    is_spam: bool = False,
    getcontact_count: int = 0,
    has_fraud_report: bool = False,
    phone_score: int = 0,
    result_json: dict = None,
) -> int:
    """Simpan hasil investigasi DC ke database."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        INSERT INTO dc_investigations (
            created_at, dc_phone, operator, region, phone_type,
            truecaller_name, is_spam, getcontact_count, has_fraud_report,
            phone_score, status, result_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        dc_phone, operator, region, phone_type,
        truecaller_name, int(is_spam), getcontact_count, int(has_fraud_report),
        phone_score, "selesai",
        json.dumps(result_json or {}),
    ))
    new_id = c.lastrowid
    conn.commit()
    conn.close()
    return new_id


def get_dc_history(limit: int = 100) -> list:
    """Ambil semua riwayat investigasi DC."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT id, created_at, dc_phone, operator, region,
               truecaller_name, is_spam, getcontact_count, has_fraud_report,
               phone_score, status, notes
        FROM dc_investigations
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows


def get_dc_detail(record_id: int) -> dict:
    """Ambil detail lengkap satu record investigasi DC."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM dc_investigations WHERE id = ?", (record_id,))
    row = c.fetchone()
    conn.close()
    if row:
        d = dict(row)
        try:
            d["result_json"] = json.loads(d.get("result_json") or "{}")
        except Exception:
            d["result_json"] = {}
        return d
    return {}


def delete_dc(record_id: int):
    """Hapus satu record investigasi DC."""
    conn = get_connection()
    conn.execute("DELETE FROM dc_investigations WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()


def delete_all_dc():
    """Hapus semua record investigasi DC."""
    conn = get_connection()
    conn.execute("DELETE FROM dc_investigations")
    conn.commit()
    conn.close()


# ═══════════════════════════════════════════════════════════
# REMOVAL REQUESTS
# ═══════════════════════════════════════════════════════════

def save_removal(
    target_name: str = "",
    target_url: str = "",
    word_term: str = "",
    removal_type: str = "",
) -> int:
    """Simpan riwayat removal request."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        INSERT INTO removal_requests (created_at, target_name, target_url, word_term, removal_type, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        target_name, target_url, word_term, removal_type, "draft",
    ))
    new_id = c.lastrowid
    conn.commit()
    conn.close()
    return new_id


def get_removal_history(limit: int = 100) -> list:
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM removal_requests ORDER BY id DESC LIMIT ?", (limit,))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows


def delete_removal(record_id: int):
    conn = get_connection()
    conn.execute("DELETE FROM removal_requests WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()


def update_removal_status(record_id: int, status: str, notes: str = ""):
    conn = get_connection()
    conn.execute(
        "UPDATE removal_requests SET status = ?, notes = ? WHERE id = ?",
        (status, notes, record_id)
    )
    conn.commit()
    conn.close()


# ═══════════════════════════════════════════════════════════
# REMOVAL CASES & PROGRESS TRACKING (TERINTEGRASI)
# ═══════════════════════════════════════════════════════════

def create_removal_case(
    client_name: str,
    target_url: str,
    target_snippet: str = "",
    target_keyword: str = "",
    platform: str = "",
    removal_type: str = "Google Outdated Content",
    client_phone: str = "",
    status: str = "Draft",
    progress_percent: int = 10,
    ai_guidance: str = "",
    notes: str = "",
) -> tuple:
    """Buat Case Pembersihan Data baru dan buat log inisial."""
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Generasi kode case unik: RMV-YYYYMMDD-XXXX
    date_code = datetime.now().strftime("%Y%m%d")
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT COUNT(*) as n FROM removal_cases")
    seq = (c.fetchone()["n"] or 0) + 1
    case_code = f"RMV-{date_code}-{seq:03d}"

    c.execute("""
        INSERT INTO removal_cases (
            case_code, created_at, updated_at, client_name, client_phone,
            target_url, target_snippet, target_keyword, platform,
            removal_type, status, progress_percent, ai_guidance, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        case_code, now_str, now_str, client_name, client_phone,
        target_url, target_snippet, target_keyword, platform,
        removal_type, status, progress_percent, ai_guidance, notes
    ))
    case_id = c.lastrowid

    # Buat log pertama
    c.execute("""
        INSERT INTO removal_logs (case_id, created_at, action_type, old_status, new_status, description, actor)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        case_id, now_str, "Case Created", "-", status,
        f"Case pembersihan {case_code} baru berhasil dibuat dari Diagnosa/Input Manual.",
        "System/Operator"
    ))

    conn.commit()
    conn.close()
    return case_id, case_code


def get_removal_cases(status_filter: str = None, search_query: str = None, limit: int = 200) -> list:
    """Ambil daftar semua case pembersihan data beserta jumlah log."""
    conn = get_connection()
    c = conn.cursor()

    query = "SELECT * FROM removal_cases WHERE 1=1"
    params = []

    if status_filter and status_filter != "Semua Status":
        query += " AND status = ?"
        params.append(status_filter)

    if search_query and search_query.strip():
        sq = f"%{search_query.strip()}%"
        query += " AND (case_code LIKE ? OR client_name LIKE ? OR target_url LIKE ? OR target_keyword LIKE ?)"
        params.extend([sq, sq, sq, sq])

    query += " ORDER BY id DESC LIMIT ?"
    params.append(limit)

    c.execute(query, params)
    rows = [dict(r) for r in c.fetchall()]

    # Hitung log per case
    for r in rows:
        c.execute("SELECT COUNT(*) as n FROM removal_logs WHERE case_id = ?", (r["id"],))
        r["log_count"] = c.fetchone()["n"]

    conn.close()
    return rows


def get_removal_case_detail(case_id: int) -> dict:
    """Ambil detail lengkap satu case beserta seluruh riwayat log penanganannya."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM removal_cases WHERE id = ?", (case_id,))
    row = c.fetchone()
    if not row:
        conn.close()
        return {}

    case_dict = dict(row)
    c.execute("SELECT * FROM removal_logs WHERE case_id = ? ORDER BY id DESC", (case_id,))
    case_dict["logs"] = [dict(l) for l in c.fetchall()]
    conn.close()
    return case_dict


def update_removal_case_status(
    case_id: int,
    new_status: str,
    progress_percent: int = None,
    notes: str = "",
    actor: str = "Operator",
) -> bool:
    """Update status progress case pembersihan dan catat log perubahan."""
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT status, progress_percent FROM removal_cases WHERE id = ?", (case_id,))
    curr = c.fetchone()
    if not curr:
        conn.close()
        return False

    old_status = curr["status"]
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Tentukan progress_percent otomatis jika tidak diberikan
    if progress_percent is None:
        status_map = {
            "Draft": 10,
            "Diajukan": 35,
            "Dalam Peninjauan": 65,
            "Berhasil Dihapus": 100,
            "Ditolak": 40,
        }
        progress_percent = status_map.get(new_status, curr["progress_percent"])

    c.execute("""
        UPDATE removal_cases
        SET status = ?, progress_percent = ?, updated_at = ?, notes = CASE WHEN ? != '' THEN ? ELSE notes END
        WHERE id = ?
    """, (new_status, progress_percent, now_str, notes, notes, case_id))

    # Catat ke log
    desc = f"Status diubah dari '{old_status}' menjadi '{new_status}' (Progress: {progress_percent}%)."
    if notes:
        desc += f" Catatan: {notes}"

    c.execute("""
        INSERT INTO removal_logs (case_id, created_at, action_type, old_status, new_status, description, actor)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (case_id, now_str, "Status Update", old_status, new_status, desc, actor))

    conn.commit()
    conn.close()
    return True


def update_case_live_check(case_id: int, http_code: int, is_indexed: bool, actor: str = "AI Live Checker"):
    """Update status live check URL target di Google."""
    conn = get_connection()
    c = conn.cursor()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    c.execute("""
        UPDATE removal_cases
        SET http_status_code = ?, is_indexed = ?, last_checked_at = ?, updated_at = ?
        WHERE id = ?
    """, (http_code, 1 if is_indexed else 0, now_str, now_str, case_id))

    status_desc = "🔴 Terindeks di Google (HTTP 200)" if is_indexed else "🟢 TERHAPUS / De-indexed (HTTP 404/410)"
    log_desc = f"Live Check Google: Respon HTTP {http_code} - {status_desc}."

    c.execute("""
        INSERT INTO removal_logs (case_id, created_at, action_type, old_status, new_status, description, actor)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (case_id, now_str, "Live Index Check", "-", "-", log_desc, actor))

    conn.commit()
    conn.close()


def add_case_log(case_id: int, action_type: str, description: str, actor: str = "Operator"):
    """Tambah catatan log manual ke case pembersihan."""
    conn = get_connection()
    c = conn.cursor()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    c.execute("""
        INSERT INTO removal_logs (case_id, created_at, action_type, old_status, new_status, description, actor)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (case_id, now_str, action_type, "-", "-", description, actor))

    c.execute("UPDATE removal_cases SET updated_at = ? WHERE id = ?", (now_str, case_id))
    conn.commit()
    conn.close()


def delete_removal_case(case_id: int):
    """Hapus satu case pembersihan beserta seluruh log-nya."""
    conn = get_connection()
    conn.execute("DELETE FROM removal_logs WHERE case_id = ?", (case_id,))
    conn.execute("DELETE FROM removal_cases WHERE id = ?", (case_id,))
    conn.commit()
    conn.close()


# ═══════════════════════════════════════════════════════════
# POLICE REPORTS
# ═══════════════════════════════════════════════════════════

def save_police_report(
    reporter_name: str,
    reporter_nik: str = "",
    reporter_phone: str = "",
    dc_phone: str = "",
    incident_summary: str = "",
    filename: str = "",
) -> int:
    """Simpan metadata laporan polisi yang digenerate."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        INSERT INTO police_reports (
            created_at, reporter_name, reporter_nik, reporter_phone,
            dc_phone, incident_summary, filename, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        reporter_name, reporter_nik, reporter_phone,
        dc_phone, incident_summary[:300], filename, "generated",
    ))
    new_id = c.lastrowid
    conn.commit()
    conn.close()
    return new_id


def get_police_report_history(limit: int = 100) -> list:
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM police_reports ORDER BY id DESC LIMIT ?", (limit,))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows


def delete_police_report(record_id: int):
    conn = get_connection()
    conn.execute("DELETE FROM police_reports WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()


# ═══════════════════════════════════════════════════════════
# STATS - RINGKASAN UNTUK DASHBOARD
# ═══════════════════════════════════════════════════════════

def get_dashboard_stats() -> dict:
    """Ambil statistik ringkasan untuk ditampilkan di dashboard."""
    conn = get_connection()
    c = conn.cursor()

    stats = {}

    c.execute("SELECT COUNT(*) as n FROM scan_history")
    stats["total_scans"] = c.fetchone()["n"]

    c.execute("SELECT COUNT(*) as n FROM dc_investigations")
    stats["total_dc"] = c.fetchone()["n"]

    c.execute("SELECT COUNT(*) as n FROM removal_requests")
    stats["total_removals"] = c.fetchone()["n"]

    # Case Pembersihan Data Stats
    c.execute("SELECT COUNT(*) as n FROM removal_cases")
    stats["total_removal_cases"] = c.fetchone()["n"]

    c.execute("SELECT COUNT(*) as n FROM removal_cases WHERE status = 'Berhasil Dihapus'")
    stats["completed_cases"] = c.fetchone()["n"]

    c.execute("SELECT COUNT(*) as n FROM removal_cases WHERE status IN ('Draft', 'Diajukan', 'Dalam Peninjauan')")
    stats["active_cases"] = c.fetchone()["n"]

    c.execute("SELECT COUNT(*) as n FROM police_reports")
    stats["total_reports"] = c.fetchone()["n"]

    c.execute("SELECT COUNT(*) as n FROM clients")
    stats["total_clients"] = c.fetchone()["n"]

    c.execute("SELECT AVG(risk_score) as avg FROM scan_history WHERE risk_score > 0")
    row = c.fetchone()
    stats["avg_risk_score"] = round(row["avg"] or 0)

    c.execute("SELECT COUNT(*) as n FROM scan_history WHERE risk_color = 'red'")
    stats["high_risk_count"] = c.fetchone()["n"]

    c.execute("SELECT COUNT(*) as n FROM dc_investigations WHERE is_spam = 1")
    stats["spam_dc_count"] = c.fetchone()["n"]

    # Scan terbaru
    c.execute("SELECT created_at, target_name, risk_score, risk_category FROM scan_history ORDER BY id DESC LIMIT 5")
    stats["recent_scans"] = [dict(r) for r in c.fetchall()]

    # Case Pembersihan Terbaru
    c.execute("SELECT id, case_code, created_at, client_name, target_url, status, progress_percent FROM removal_cases ORDER BY id DESC LIMIT 5")
    stats["recent_removal_cases"] = [dict(r) for r in c.fetchall()]

    # DC terbaru
    c.execute("SELECT created_at, dc_phone, operator, is_spam FROM dc_investigations ORDER BY id DESC LIMIT 5")
    stats["recent_dc"] = [dict(r) for r in c.fetchall()]

    conn.close()
    return stats


# ═══════════════════════════════════════════════════════════
# ADMIN USERS (AUTENTIKASI & MANAJEMEN ADMIN)
# ═══════════════════════════════════════════════════════════

def get_admin_user(username: str) -> Optional[dict]:
    """Ambil data admin berdasarkan username."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM admin_users WHERE username = ?", (username.strip(),))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None


def update_admin_login_time(user_id: int):
    """Update timestamp last_login admin."""
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = get_connection()
    conn.execute("UPDATE admin_users SET last_login = ? WHERE id = ?", (now_str, user_id))
    conn.commit()
    conn.close()


def update_admin_password(username: str, new_password_hash: str) -> bool:
    """Ubah password admin."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE admin_users SET password_hash = ? WHERE username = ?", (new_password_hash, username))
    conn.commit()
    affected = c.rowcount
    conn.close()
    return affected > 0


# ═══════════════════════════════════════════════════════════
# MANAJEMEN DATA KLIEN INTERNAL
# ═══════════════════════════════════════════════════════════

def create_client(
    full_name: str,
    nik: str = "",
    phone: str = "",
    email: str = "",
    address: str = "",
    emergency_contact: str = "",
    status: str = "Aktif",
    notes: str = "",
    created_by: str = "admin",
) -> tuple:
    """Buat data Klien internal baru."""
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_code = datetime.now().strftime("%Y%m%d")

    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT COUNT(*) as n FROM clients")
    seq = (c.fetchone()["n"] or 0) + 1
    client_code = f"CLI-{date_code}-{seq:03d}"

    c.execute("""
        INSERT INTO clients (
            client_code, created_at, updated_at, full_name, nik, phone, email,
            address, emergency_contact, status, notes, created_by
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        client_code, now_str, now_str, full_name, nik, phone, email,
        address, emergency_contact, status, notes, created_by
    ))
    client_id = c.lastrowid
    conn.commit()
    conn.close()
    return client_id, client_code


def get_clients(search_query: str = None, status_filter: str = None, limit: int = 200) -> list:
    """Ambil semua Klien beserta ringkasan jumlah kasus & diagnosa."""
    conn = get_connection()
    c = conn.cursor()

    query = "SELECT * FROM clients WHERE 1=1"
    params = []

    if status_filter and status_filter != "Semua Status":
        query += " AND status = ?"
        params.append(status_filter)

    if search_query and search_query.strip():
        sq = f"%{search_query.strip()}%"
        query += " AND (client_code LIKE ? OR full_name LIKE ? OR phone LIKE ? OR email LIKE ? OR nik LIKE ?)"
        params.extend([sq, sq, sq, sq, sq])

    query += " ORDER BY id DESC LIMIT ?"
    params.append(limit)

    c.execute(query, params)
    rows = [dict(r) for r in c.fetchall()]

    for r in rows:
        name_q = r.get("full_name", "")
        phone_q = r.get("phone", "")

        # Hitung Diagnosa
        c.execute("SELECT COUNT(*) as n FROM scan_history WHERE target_name LIKE ? OR (target_phone != '' AND target_phone LIKE ?)", (f"%{name_q}%", f"%{phone_q}%"))
        r["scan_count"] = c.fetchone()["n"]

        # Hitung Case Pembersihan
        c.execute("SELECT COUNT(*) as n FROM removal_cases WHERE client_name LIKE ?", (f"%{name_q}%",))
        r["removal_count"] = c.fetchone()["n"]

        # Hitung Laporan Polisi
        c.execute("SELECT COUNT(*) as n FROM police_reports WHERE reporter_name LIKE ?", (f"%{name_q}%",))
        r["report_count"] = c.fetchone()["n"]

    conn.close()
    return rows


def get_client_detail(client_id: int) -> dict:
    """Ambil detail Klien lengkap."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else {}


def update_client(
    client_id: int,
    full_name: str,
    nik: str,
    phone: str,
    email: str,
    address: str,
    emergency_contact: str,
    status: str,
    notes: str,
) -> bool:
    """Update data Klien."""
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        UPDATE clients
        SET full_name = ?, nik = ?, phone = ?, email = ?, address = ?,
            emergency_contact = ?, status = ?, notes = ?, updated_at = ?
        WHERE id = ?
    """, (full_name, nik, phone, email, address, emergency_contact, status, notes, now_str, client_id))
    conn.commit()
    affected = c.rowcount
    conn.close()
    return affected > 0


def delete_client(client_id: int):
    """Hapus data Klien."""
    conn = get_connection()
    conn.execute("DELETE FROM clients WHERE id = ?", (client_id,))
    conn.commit()
    conn.close()


def get_client_timeline_360(client_name: str, client_phone: str = "", client_email: str = "") -> list:
    """Ambil seluruh gabungan timeline 360° Diagnosa, Removal, & Laporan Polisi untuk Klien ini."""
    conn = get_connection()
    c = conn.cursor()
    timeline = []

    name_q = f"%{client_name.strip()}%"
    phone_q = f"%{client_phone.strip()}%" if client_phone.strip() else "____NONE____"

    # 1. Diagnosa Scans
    c.execute("""
        SELECT created_at, target_name, risk_score, risk_category, risk_color
        FROM scan_history
        WHERE target_name LIKE ? OR target_phone LIKE ?
        ORDER BY id DESC
    """, (name_q, phone_q))
    for r in c.fetchall():
        timeline.append({
            "date": r["created_at"],
            "type": "Diagnosa Scans",
            "icon": "🔍",
            "title": f"Diagnosa Jejak Digital (Score: {r['risk_score']}/100)",
            "badge": r["risk_category"],
            "color": r["risk_color"] or "#00D4FF",
            "desc": f"Target: {r['target_name']}"
        })

    # 2. Case Pembersihan Data
    c.execute("""
        SELECT created_at, case_code, target_url, status, progress_percent, removal_type
        FROM removal_cases
        WHERE client_name LIKE ? OR client_phone LIKE ?
        ORDER BY id DESC
    """, (name_q, phone_q))
    for r in c.fetchall():
        timeline.append({
            "date": r["created_at"],
            "type": "Removal Case",
            "icon": "📑",
            "title": f"Case Pembersihan {r['case_code']} ({r['status']})",
            "badge": f"{r['progress_percent']}% Progress",
            "color": "#00E676" if r['status'] == "Berhasil Dihapus" else "#FFD740",
            "desc": f"URL Target: {r['target_url']}"
        })

    # 3. Laporan Polisi PDF
    c.execute("""
        SELECT created_at, reporter_name, dc_phone, filename, status
        FROM police_reports
        WHERE reporter_name LIKE ? OR reporter_phone LIKE ?
        ORDER BY id DESC
    """, (name_q, phone_q))
    for r in c.fetchall():
        timeline.append({
            "date": r["created_at"],
            "type": "Laporan Polisi",
            "icon": "📄",
            "title": f"Laporan Pengaduan Siber ({r['filename']})",
            "badge": "Terbit",
            "color": "#7B61FF",
            "desc": f"Pelapor: {r['reporter_name']} | Target DC: {r['dc_phone']}"
        })

    conn.close()
    # Urutkan berdasarkan tanggal terbaru di atas
    timeline.sort(key=lambda x: x["date"], reverse=True)
    return timeline


# Inisialisasi otomatis saat modul diimport
init_database()
