"""
Menyalahati Cyber Intelligence - AI Doxing & Debt Exposure Analyzer
Analisis AI kecerdasan buatan untuk mengidentifikasi keterkaitan nama/identitas
dengan tagihan utang, teror DC pinjol, dan komentar doxing di Google & Medsos.
"""

import re
from typing import Dict, List
from urllib.parse import quote_plus

def analyze_doxing_reputation(
    full_name: str = "",
    phone: str = "",
    spouse_family_name: str = "",
    additional_keywords: str = "",
    dork_results: List[Dict] = None
) -> Dict:
    """
    Analisis cerdas kecerdasan buatan (AI Cyber Intelligence):
    Evaluasi keterkaitan kata kunci target dengan reputasi utang/pinjol/doxing.
    """
    full_name = full_name.strip()
    phone = phone.strip()
    spouse_name = spouse_family_name.strip()
    keywords = additional_keywords.strip()

    analysis = {
        "target_name": full_name,
        "phone": phone,
        "family_target": spouse_name,
        "has_debt_association": False,
        "doxing_risk_level": "🟢 AMAN",
        "risk_color": "#00E676",
        "ai_summary": "",
        "detected_threats": [],
        "google_live_queries": [],
        "deindexing_steps": []
    }

    # Bangun Kueri Google Langsung (1-Click Google Live Action Links)
    queries = []
    if full_name:
        q_text1 = f'"{full_name}" (hutang OR utang OR pinjol)'
        queries.append({
            "label": f'🔍 Google: "{full_name} hutang"',
            "url": f'https://www.google.com/search?q={quote_plus(q_text1)}'
        })
        q_text2 = f'"{full_name}" (site:instagram.com OR site:facebook.com) (utang OR pinjol)'
        queries.append({
            "label": f'🔍 Google Medsos: "{full_name} instagram/facebook"',
            "url": f'https://www.google.com/search?q={quote_plus(q_text2)}'
        })

    # Tangani multiple kerabat yang dipisah koma (e.g., "Khairul Razi, Kirana Vinzi Apsari Khairana, Vinzi Athahira")
    if spouse_name:
        family_list = [f.strip() for f in spouse_name.split(",") if f.strip()]
        for fam in family_list[:3]:  # Maksimal 3 tombol kerabat teratas agar UI rapi
            q_fam = f'"{fam}" (utang OR hutang OR pinjol OR doxing)'
            queries.append({
                "label": f'🔍 Google Kerabat: "{fam} utang"',
                "url": f'https://www.google.com/search?q={quote_plus(q_fam)}'
            })

    if phone:
        clean_ph = re.sub(r'[^\d]', '', phone)
        # Kueri bersih nomor HP tanpa kata kunci pembatas agar semua jejak HP ditemukan
        q_text4 = f'"{clean_ph}" OR "62{clean_ph.lstrip("0")}"'
        queries.append({
            "label": f'🔍 Google HP (Semua): "{phone}"',
            "url": f'https://www.google.com/search?q={quote_plus(q_text4)}'
        })
        # Kueri khusus doxing/pinjol dengan pengelompokan tanda kurung yang benar
        q_text5 = f'("{clean_ph}" OR "62{clean_ph.lstrip("0")}") (doxing OR pinjol OR utang OR penipu)'
        queries.append({
            "label": f'🔍 Google HP (Doxing/Pinjol): "{phone}"',
            "url": f'https://www.google.com/search?q={quote_plus(q_text5)}'
        })

    analysis["google_live_queries"] = queries

    # Cek Indikasi Risiko Doxing & Keuangan
    debt_terms = ["utang", "hutang", "pinjol", "bayar utang", "debt collector", "dc pinjol", "teror", "penipu", "sebar data", "tagihan"]
    detected_threats = []

    # Periksa dari Dork Results jika ada
    dork_count = 0
    if dork_results:
        for res in dork_results:
            items = res.get("result", {}).get("items", [])
            for it in items:
                combined = f"{it.get('title','')} {it.get('snippet','')}".lower()
                if any(dt in combined for dt in debt_terms):
                    detected_threats.append(f"Terdeteksi kata kunci utang/pinjol pada hasil: {it.get('title')}")
                    dork_count += 1

    # Evaluasi berdasarkan input & findings
    input_combined = f"{full_name} {spouse_name} {keywords}".lower()
    has_debt_kw = any(dt in input_combined for dt in debt_terms) or dork_count > 0

    if has_debt_kw:
        analysis["has_debt_association"] = True
        analysis["doxing_risk_level"] = "🔴 KRITIS - Teridentifikasi Doxing Utang/Pinjol"
        analysis["risk_color"] = "#FF5252"
        analysis["ai_summary"] = (
            f"🤖 **Analisis AI Cyber Intelligence:** Nama target **'{full_name}'** "
            f"{f'dan kerabat ({spouse_name}) ' if spouse_name else ''}memiliki indikasi tinggi keterkaitan dengan "
            f"kata kunci utang/pinjol/doxing. Komentar teror DC atau postingan tagihan rentan terindeks di Google AI Overview & Komentar Medsos (Instagram/FB)."
        )
    elif spouse_name or keywords:
        analysis["doxing_risk_level"] = "🟡 WASPADA - Data Identitas Terekspos"
        analysis["risk_color"] = "#FFD740"
        analysis["ai_summary"] = (
            f"🤖 **Analisis AI Cyber Intelligence:** Nama target **'{full_name}'** terdeteksi bersama data kerabat "
            f"({spouse_name}). Informasi ini dapat dimanfaatkan oleh DC pinjol untuk melakukan profiling doxing sosial."
        )
    else:
        analysis["ai_summary"] = (
            f"🤖 **Analisis AI Cyber Intelligence:** Nama target **'{full_name}'** saat ini belum menunjukkan indikasi "
            f"doxing utang pinjol aktif di indeks publik. Gunakan tombol kueri Google di bawah untuk verifikasi langsung."
        )

    # Langkah Pengajuan De-Indexing Google
    analysis["deindexing_steps"] = [
        "1. Gunakan Google Outdated Content Removal Tool (https://search.google.com/search-console/remove-outdated-content) jika postingan/komentar di Instagram telah dihapus tapi masih muncul di Google.",
        "2. Ajukan Legal Removal UU PDP No. 27/2022 & UU ITE ke Google Help Center untuk penghapusan data pribadi (KTP/NIK/HP/Foto Doxing).",
        "3. Lakukan DM Admin & Laporkan Komentar Doxing ke Instagram/Facebook help center dengan template surat dari Tab Asisten Removal."
    ]

    return analysis
