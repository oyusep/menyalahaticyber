"""
Menyalahati Cyber Intelligence - Risk Score Calculator v2
Menghitung Exposure Risk Score (0-100) dari 5 dimensi data nyata:

  DIMENSI 1 - Google Dork Score    (bobot 30%)
  DIMENSI 2 - Social Exposure Score (bobot 25%)
  DIMENSI 3 - Phone Intel Score     (bobot 20%)
  DIMENSI 4 - HIBP Breach Score     (bobot 15%)
  DIMENSI 5 - Doxing Active Score   (bobot 10%)

Formula:
  Final = D1×0.30 + D2×0.25 + D3×0.20 + D4×0.15 + D5×0.10
"""
from typing import List, Dict, Tuple


# ─── Bobot 5 Dimensi (total = 1.0) ──────────────────────────
WEIGHT_GOOGLE_DORK      = 0.30   # Dimensi 1
WEIGHT_SOCIAL_EXPOSURE  = 0.25   # Dimensi 2
WEIGHT_PHONE_INTEL      = 0.20   # Dimensi 3
WEIGHT_HIBP_BREACH      = 0.15   # Dimensi 4
WEIGHT_DOXING_ACTIVE    = 0.10   # Dimensi 5

# Risk per kategori dork
DORK_RISK_SCORES = {
    "critical": 20,
    "high": 12,
    "medium": 6,
    "low": 2,
}

# Risk per jenis data breach
BREACH_DATA_CLASS_SCORES = {
    "passwords": 15,
    "credit cards": 20,
    "bank account numbers": 20,
    "social security numbers": 20,
    "passport numbers": 18,
    "nik": 18,
    "phone numbers": 12,
    "physical addresses": 12,
    "dates of birth": 10,
    "email addresses": 5,
    "usernames": 4,
    "ip addresses": 6,
    "geographic locations": 8,
}

# Platform sosial media dan skor eksposur
SOCIAL_PLATFORM_SCORES = {
    "facebook.com": 8,
    "instagram.com": 7,
    "twitter.com": 6,
    "linkedin.com": 9,  # Lebih tinggi karena ada info profesional
    "tiktok.com": 5,
    "reddit.com": 4,
    "github.com": 3,
}


def calculate_dork_score(dork_results: List[Dict]) -> Tuple[float, List[str]]:
    """
    Hitung skor dari hasil Google Dorking.
    
    Returns:
        (raw_score, list_of_findings)
    """
    raw_score = 0
    findings = []

    for result in dork_results:
        found_count = result.get("found_count", 0)
        risk_level = result.get("risk", "medium")

        if found_count > 0:
            base_score = DORK_RISK_SCORES.get(risk_level, 6)
            # Tambah skor jika banyak temuan
            multiplier = min(found_count, 5) * 0.5 + 0.5
            score_contribution = base_score * multiplier
            raw_score += score_contribution
            findings.append(
                f"[{risk_level.upper()}] {result.get('label', '')}: "
                f"{found_count} temuan terindeks publik"
            )

    return min(raw_score, 100), findings


def calculate_breach_score(breaches: List[Dict]) -> Tuple[float, List[str]]:
    """
    Hitung skor dari data breach HIBP.
    
    Returns:
        (raw_score, list_of_findings)
    """
    raw_score = 0
    findings = []

    for breach in breaches:
        data_classes = [dc.lower() for dc in breach.get("data_classes", [])]
        breach_score = 0

        for dc in data_classes:
            for key, score in BREACH_DATA_CLASS_SCORES.items():
                if key in dc:
                    breach_score += score
                    break

        if breach_score == 0:
            breach_score = 5  # Minimal score per breach

        breach_score = min(breach_score, 25)  # Cap per breach
        raw_score += breach_score

        findings.append(
            f"Bocor di {breach.get('title', 'Layanan')}: "
            f"{', '.join(breach.get('data_classes', [])[:3])}"
        )

    return min(raw_score, 100), findings


def calculate_social_score(dork_results: List[Dict]) -> Tuple[float, List[str]]:
    """
    Hitung skor dari eksposur media sosial (dari hasil dork).
    
    Returns:
        (raw_score, list_of_findings)
    """
    raw_score = 0
    findings = []
    found_platforms = set()

    for result in dork_results:
        items = result.get("result", {}).get("items", [])
        for item in items:
            display_url = item.get("display_url", "").lower()
            url = item.get("url", "").lower()
            for platform, score in SOCIAL_PLATFORM_SCORES.items():
                if platform in display_url or platform in url:
                    if platform not in found_platforms:
                        found_platforms.add(platform)
                        raw_score += score
                        findings.append(f"Profil ditemukan di {platform}")

    return min(raw_score, 100), findings


def calculate_phone_score(phone_intel_data: Dict) -> Tuple[float, List[str]]:
    """
    Dimensi 3: Hitung skor dari hasil Phone Intelligence.
    Sumber: Truecaller, GetContact, Google mentions, cekrekening.id
    """
    if not phone_intel_data:
        return 0.0, []

    raw_score = 0
    findings = []

    # Truecaller
    truecaller = phone_intel_data.get("truecaller", {})
    tc_score = truecaller.get("exposure_score", 0)
    if tc_score > 0:
        raw_score += tc_score * 0.3
        if truecaller.get("name"):
            findings.append(f"Nama pemilik terekspos di Truecaller: {truecaller['name']}")
        if truecaller.get("spam_score", 0) > 0:
            findings.append("Nomor dilaporkan spam di Truecaller")

    # GetContact
    getcontact = phone_intel_data.get("getcontact", {})
    gc_score = getcontact.get("exposure_score", 0)
    if gc_score > 0:
        raw_score += gc_score * 0.25
        if getcontact.get("save_count", 0) > 0:
            findings.append(f"Disimpan {getcontact['save_count']}x dengan nama berbeda di GetContact")

    # Google mentions
    gm = phone_intel_data.get("google_mentions", {})
    gm_score = gm.get("exposure_score", 0)
    if gm_score > 0:
        raw_score += gm_score * 0.35
        mentions = gm.get("total_mentions", 0)
        if mentions > 0:
            findings.append(f"Nomor muncul di {mentions} halaman publik Google")
        paste = gm.get("categories", {}).get("paste_sites", 0)
        if paste > 0:
            findings.append(f"[CRITICAL] Nomor muncul di {paste} paste/dump site!")

    # Fraud reports
    fraud = phone_intel_data.get("fraud_reports", {})
    fr_score = fraud.get("exposure_score", 0)
    if fr_score > 0:
        raw_score += fr_score * 0.1
        if fraud.get("has_report"):
            findings.append(f"Nomor dilaporkan penipuan: {fraud.get('report_count', 1)} laporan")

    # Juga bisa dari direct phone score
    direct = phone_intel_data.get("total_phone_score", 0)
    if direct > 0 and raw_score == 0:
        raw_score = direct

    return min(raw_score, 100), findings


def calculate_doxing_active_score(dork_results: List[Dict], phone_intel: Dict = None) -> Tuple[float, List[str]]:
    """
    Dimensi 5: Deteksi apakah target sudah aktif di-doxing di Google & Medsos.
    Indikator: teror utang DC, komentar doxing medsos, paste sites, telegram, thread aktif.
    """
    raw_score = 0
    findings = []

    # Kata kunci indikator teror doxing & utang DC
    doxing_keywords = [
        "doxing", "doxed", "doxxed", "pastebin", "ghostbin", "rentry", "hastebin",
        "t.me", "telegram", "utang", "hutang", "pinjol", "bayar utang", "bayar utangku",
        "suruh", "ibunya", "tagihan", "sebar data", "debt collector", "dc pinjol",
        "penipu", "teror", "kondar", "kontak darurat"
    ]
    critical_categories = ["dump", "doxing", "family"]

    for result in dork_results:
        category = result.get("category", "").lower()
        label = result.get("label", "").lower()
        items = result.get("result", {}).get("items", [])
        found_count = result.get("found_count", 0)

        # Cek jika kategori atau label berkaitan dengan doxing / utang / keluarga
        if (category in critical_categories or "doxing" in label or "utang" in label) and found_count > 0:
            raw_score += 25 * min(found_count, 4)
            findings.append(
                f"[CRITICAL] Komentar/Thread Doxing DC terdeteksi: {result.get('label', '')} ({found_count} temuan terindeks)"
            )

        for item in items:
            url = item.get("url", "").lower()
            title = item.get("title", "").lower()
            snippet = item.get("snippet", "").lower()
            combined = f"{url} {title} {snippet}"

            if any(kw in combined for kw in ["utang", "hutang", "pinjol", "bayar utang", "suruh", "tagihan", "teror", "penipu", "kaburan"]):
                raw_score += 35
                findings.append(f"🚨 [KRITIS] Teror Utang DC terindeks di: {item.get('display_url', url[:50])}")

            elif any(kw in combined for kw in doxing_keywords):
                raw_score += 20
                findings.append(f"⚠️ Data Doxing/Mention ditemukan di: {item.get('display_url', url[:40])}")

    # Dari phone intel
    if phone_intel:
        paste_mentions = phone_intel.get("google_mentions", {}).get(
            "categories", {}
        ).get("paste_sites", 0)
        if paste_mentions > 0:
            raw_score += paste_mentions * 25
            findings.append(f"[CRITICAL] Nomor HP muncul di {paste_mentions} paste site")

    return min(raw_score, 100), findings


def calculate_exposure_risk(
    dork_results: List[Dict] = None,
    breaches: List[Dict] = None,
    social_data: Dict = None,
    phone_intel: Dict = None,
) -> Dict:
    """
    Hitung total Exposure Risk Score dari 5 dimensi.

    Args:
        dork_results: Hasil dari real_scraper.run_real_dork_scan() atau google_dorking
        breaches: Hasil dari breach_audit.check_email_breaches()
        social_data: Hasil dari social_scanner.scan_all_social_platforms()
        phone_intel: Hasil dari phone_intel.run_phone_intelligence()

    Returns:
        dict berisi score, kategori, findings, rekomendasi, dan breakdown 5 dimensi
    """
    dork_results = dork_results or []
    breaches = breaches or []

    # Dimensi 1 - Google Dork
    dork_raw, dork_findings = calculate_dork_score(dork_results)

    # Dimensi 2 - Social Exposure
    if social_data and isinstance(social_data, dict):
        # Dari social_scanner - gunakan aggregate score
        social_raw = social_data.get("total_social_score", 0)
        social_findings_raw = []
        for platform, pdata in social_data.get("platforms", {}).items():
            for detail in pdata.get("exposure_details", []) or pdata.get("details", []):
                social_findings_raw.append(f"[{platform.upper()}] {detail}")
        social_findings = social_findings_raw or []
    else:
        # Fallback ke metode lama dari dork results
        social_raw, social_findings = calculate_social_score(dork_results)

    # Dimensi 3 - Phone Intelligence
    if phone_intel:
        phone_raw, phone_findings = calculate_phone_score(phone_intel)
    else:
        phone_raw, phone_findings = 0.0, []

    # Dimensi 4 - HIBP Breach
    breach_raw, breach_findings = calculate_breach_score(breaches)

    # Dimensi 5 - Doxing Active
    doxing_raw, doxing_findings = calculate_doxing_active_score(dork_results, phone_intel)

    # Formula tertimbang 5 dimensi
    weighted_score = (
        dork_raw   * WEIGHT_GOOGLE_DORK
        + social_raw  * WEIGHT_SOCIAL_EXPOSURE
        + phone_raw   * WEIGHT_PHONE_INTEL
        + breach_raw  * WEIGHT_HIBP_BREACH
        + doxing_raw  * WEIGHT_DOXING_ACTIVE
    )

    final_score = min(round(weighted_score), 100)

    # Kategorisasi
    if final_score <= 30:
        category = "RENDAH"
        color = "green"
        emoji = "🟢"
        summary = "Jejak digital Anda relatif aman. Tetap waspada dan lakukan pemantauan rutin."
    elif final_score <= 60:
        category = "SEDANG"
        color = "orange"
        emoji = "🟡"
        summary = "Beberapa data Anda terekspos. Segera lakukan mitigasi pada temuan berisiko."
    else:
        category = "KRITIS"
        color = "red"
        emoji = "🔴"
        summary = "Data Anda SANGAT RENTAN dan banyak terekspos. Tindakan segera diperlukan!"

    # Rekomendasi mitigasi
    recommendations = generate_recommendations(final_score, dork_findings, breach_findings, phone_intel)

    all_findings = dork_findings + social_findings + phone_findings + breach_findings + doxing_findings

    return {
        "final_score": final_score,
        "category": category,
        "color": color,
        "emoji": emoji,
        "summary": summary,
        # ── Breakdown 5 Dimensi ──
        "dork_score": round(dork_raw),
        "social_score": round(social_raw),
        "phone_score": round(phone_raw),
        "breach_score": round(breach_raw),
        "doxing_active_score": round(doxing_raw),
        # ── Findings per Dimensi ──
        "all_findings": all_findings,
        "dork_findings": dork_findings,
        "social_findings": social_findings,
        "phone_findings": phone_findings,
        "breach_findings": breach_findings,
        "doxing_findings": doxing_findings,
        "recommendations": recommendations,
        # ── Meta ──
        "has_real_data": bool(social_data or phone_intel),
        "data_sources_used": [
            "Google Dorking" if dork_results else None,
            "Social Media Scan" if social_data else None,
            "Phone Intelligence" if phone_intel else None,
            "HIBP Breach Check" if breaches else None,
        ],
    }


def generate_recommendations(score: int, dork_findings: List, breach_findings: List, phone_intel: Dict = None) -> List[Dict]:
    """Generate daftar rekomendasi berdasarkan hasil scan 5 dimensi."""
    recs = []

    # Rekomendasi universal
    recs.append({
        "priority": "tinggi",
        "icon": "🔐",
        "title": "Aktifkan Autentikasi Dua Faktor (2FA)",
        "detail": "Aktifkan 2FA di semua akun penting: email, perbankan, medsos. Gunakan aplikasi authenticator (Google Authenticator / Authy).",
    })

    if breach_findings:
        recs.append({
            "priority": "kritis",
            "icon": "🚨",
            "title": "Ganti Password SEGERA",
            "detail": "Email/akun Anda ditemukan dalam database kebocoran. Ganti password semua layanan yang menggunakan email tersebut SEKARANG. Gunakan password manager.",
        })

    if dork_findings:
        recs.append({
            "priority": "kritis",
            "icon": "🤖",
            "title": "Ajukan De-Indexing & Clean-up AI Overview Google",
            "detail": "Komentar teror DC di Instagram/medsos telah dibaca oleh Google AI Overview. Segera ajukan Take-down Form di Google Search Console ('Remove Outdated Content') dan minta pemegang akun Instagram tempat komentar terposting (misal @infogarut) untuk menghapus/hides komentar spam DC tersebut.",
        })
        recs.append({
            "priority": "tinggi",
            "icon": "🗑️",
            "title": "Ajukan Penghapusan Data Pribadi ke Google",
            "detail": "Gunakan Google Results About You (myactivity.google.com/page-removal) untuk meminta penghapusan hasil pencarian yang memuat nama & kata pencemaran nama baik.",
        })
        recs.append({
            "priority": "tinggi",
            "icon": "🔒",
            "title": "Kunci Privasi Akun & Hapus Tag Medsos",
            "detail": "Set semua akun medsos ke private. Batasi siapa yang dapat memberikan komentar dan mention (@) pada akun media sosial Anda.",
        })

    recs.append({
        "priority": "sedang",
        "icon": "📱",
        "title": "Waspadai Social Engineering",
        "detail": "Jangan bagikan OTP, PIN, atau data pribadi via telepon/chat kepada siapapun, termasuk yang mengaku dari pinjol.",
    })

    recs.append({
        "priority": "sedang",
        "icon": "📋",
        "title": "Audit Aplikasi yang Diinstal",
        "detail": "Hapus aplikasi pinjol ilegal yang mungkin masih memiliki izin akses kontak, kamera, dan penyimpanan di HP Anda.",
    })

    if score >= 60:
        recs.append({
            "priority": "kritis",
            "icon": "🏛️",
            "title": "Laporkan ke OJK & Bareskrim",
            "detail": "Hubungi OJK di 157 atau www.ojk.go.id. Laporkan pinjol ilegal ke Satgas PASTI OJK dan Bareskrim Polri di 0800-1000-00.",
        })

    recs.append({
        "priority": "sedang",
        "icon": "📧",
        "title": "Gunakan Email Alias",
        "detail": "Buat email terpisah untuk pendaftaran layanan online. Pertimbangkan menggunakan layanan email alias (SimpleLogin / AnonAddy).",
    })

    return recs
