"""
Menyalahati Cyber Intelligence - Removal & De-Indexing Generator Engine
Modul pembuatan berkas legal, draf permohonan take-down, dan panduan de-indexing Google / Media Sosial
khusus korban doxing & teror DC Pinjol.

Berdasarkan:
- UU ITE No. 19/2016 Pasal 26 (Right to be Forgotten / Hak Penghapusan Informasi)
- UU Perlindungan Data Pribadi (PDP) No. 27/2022 Pasal 43-44 (Hak Penghapusan Data)
- Google Outdated Content Policy & Legal Removal Framework
"""

import streamlit as st
from typing import Dict, List, Optional
from datetime import datetime


def generate_google_outdated_guide(target_url: str, word_term: str = "") -> Dict:
    """
    Panduan & data pengajuan untuk Google Outdated Content Removal Tool.
    Digunakan ketika komentar/postingan SUDAH dihapus di Instagram/web, tetapi MASIH terindeks di Google & AI Overview.
    """
    portal_url = "https://search.google.com/search-console/remove-outdated-content"
    
    steps = [
        "1. Buka portal **Google Outdated Content Removal Tool** di link yang disediakan.",
        "2. Klik **New Request (Permohonan Baru)**.",
        "3. Masukkan **URL Halaman** yang memuat komentar (misal link Instagram/web).",
        "4. Pilih opsi: **Content is no longer on page / Snippet & Cached Text out of date**.",
        "5. Masukkan kata kunci sensitif yang DULU ada tapi SEKARANG sudah dihapus (contoh: `" + (word_term or "BAYAR HUTANG") + "`).",
        "6. Kirim pengajuan. Google biasanya memproses & membersihkan AI Overview/Cache dalam **1 x 24 Jam**."
    ]
    
    return {
        "portal_url": portal_url,
        "target_url": target_url,
        "word_term": word_term,
        "steps": steps
    }


def generate_legal_removal_letter(
    full_name: str,
    nik: str,
    phone: str,
    email: str,
    target_url: str,
    doxing_evidence_desc: str,
    platform_name: str = "Google LLC / Admin Media Sosial",
) -> str:
    """
    Generate Draf Surat Resmi Permohonan Penghapusan Data Pribadi & Content Removal
    berdasarkan UU PDP No. 27/2022 & UU ITE No. 19/2016.
    """
    date_str = datetime.now().strftime("%d %B %Y")
    
    letter = f"""SURAT PERMOHONAN PENGHAPUSAN KONTEN DOXING & DE-INDEXING HAK PRIVASI
Nomor Ref: LEGAL-RMV/{datetime.now().strftime('%Y%m%d')}/{nik[-4:] if len(nik)>=4 else '0000'}

Kepada Yth.
Tim Pengelola / Moderasi Konten / Legal Compliance
{platform_name}

Dengan hormat,

Saya yang bertanda tangan di bawah ini:
- Nama Lengkap         : {full_name}
- NIK / Identitas Resmi: {nik or '[Lampirkan KTP]'}
- Nomor HP Kontak      : {phone}
- Alamat Email         : {email}

Dengan ini mengajukan PERMOHONAN PENGHAPUSAN KONTEN & DE-INDEXING ATAS PENCEMARAN NAMA BAIK DAN DOXING DATA PRIBADI yang dilakukan oleh pihak tidak bertanggung jawab (Debt Collector / Spammer Ilegal) pada tautan (URL) berikut:

🔗 URL Terpengaruh: {target_url}

DESKRIPSI PELANGGARAN & BUKTI DOXING:
--------------------------------------------------------------------------------
{doxing_evidence_desc or 'Ditemukan komentar/postingan spam berupa tuduhan utang, teror, dan penyebaran data pribadi yang mencemarkan nama baik serta memicu rangkuman palsu di mesin pencari.'}

DASAR HUKUM PENGHAPUSAN:
1. Undang-Undang Perlindungan Data Pribadi (UU PDP) No. 27 Tahun 2022 Pasal 43 & 44 mengenai Hak Subjek Data Pribadi untuk meminta penghapusan dan penghentian pemrosesan data yang tidak sah.
2. Undang-Undang ITE No. 19 Tahun 2016 Pasal 26 mengenai Hak Penghapusan Informasi Publik (Right to be Forgotten) atas informasi yang tidak benar atau merugikan.
3. Kebijakan Google Personal Data Removal & Defamation Policy mengenai penanganan materi doxing dan pencemaran nama baik.

Dampak dari tetap terindeksnya tautan ini adalah pencemaran nama baik fatal, gangguan psikologis, serta manipulasi informasi pada rangkuman AI Overview mesin pencari.

Oleh karena itu, saya memohon agar pihak {platform_name} dapat SEGERA:
1. Menghapus (Take-down) komentar/postingan teror tersebut dari platform.
2. Melakukan De-Indexing dan pembersihan Cache/AI Overview dari hasil pencarian publik.

Demikian permohonan ini saya sampaikan dengan sebenar-benarnya. Atas perhatian dan kerjasamanya saya ucapkan terima kasih.

Hormat Saya,


({full_name})
    """
    return letter.strip()


def generate_admin_dm_message(full_name: str, target_post_link: str, comment_text: str = "") -> str:
    """
    Template pesan singkat DM / WhatsApp ke Admin Medsos (misal Admin @infogarut).
    """
    msg = f"""Halo Mimin Admin {target_post_link[:30]}... 🙏

Saya {full_name}. Mohon bantuannya sangat mimin... Di postingan mimin yang link ini:
🔗 {target_post_link}

Ada komentar spam / teror pencemaran nama baik dari akun spammer/DC pinjol yang menyebut nama saya ({comment_text or 'pencemaran utang/teror'}). Komentar ini terbaca oleh Google AI Overview dan merugikan nama baik saya secara serius.

Mohon bantuan mimin untuk HAPUS / HIDE komentar spam tersebut di postingan mimin ya min. 

Terima kasih banyak atas pengertian dan bantuan mimin 🙏 god bless you min."""
    return msg.strip()


def check_url_indexing_status(url: str) -> Dict:
    """
    Lakukan pengecekan live HTTP & Google Indexing status untuk URL target.
    Return status HTTP, status keberadaan halaman, dan indikasi apakah masih terindeks di Google.
    """
    import requests

    if not url or not url.startswith(("http://", "https://")):
        return {
            "success": False,
            "status_code": 0,
            "is_live": False,
            "is_indexed": False,
            "message": "URL tidak valid (harus diawali http:// atau https://)",
            "badge_color": "gray"
        }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        resp = requests.get(url, headers=headers, timeout=8, allow_redirects=True)
        code = resp.status_code

        if code == 200:
            is_live = True
            msg = "🔴 Halaman Masih Tayang Publik (HTTP 200)"
            badge_color = "red"
        elif code in (404, 410):
            is_live = False
            msg = "🟢 Halaman SUDAH Terhapus di Web Sumber (HTTP " + str(code) + ") - Siap De-Index Google Outdated Tool!"
            badge_color = "green"
        elif code in (403, 401):
            is_live = True
            msg = f"🟡 Halaman Dilindungi / Butuh Login (HTTP {code})"
            badge_color = "orange"
        else:
            is_live = False
            msg = f"⚪ Status HTTP {code}"
            badge_color = "gray"

        return {
            "success": True,
            "status_code": code,
            "is_live": is_live,
            "is_indexed": is_live,  # default perkiraan
            "message": msg,
            "badge_color": badge_color
        }
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "status_code": 0,
            "is_live": False,
            "is_indexed": False,
            "message": "⏱️ Connection Timeout saat mengecek URL",
            "badge_color": "gray"
        }
    except Exception as e:
        return {
            "success": False,
            "status_code": 0,
            "is_live": False,
            "is_indexed": False,
            "message": f"⚠️ Gagal terhubung ke URL: {str(e)[:100]}",
            "badge_color": "gray"
        }

