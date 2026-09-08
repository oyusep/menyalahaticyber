"""
Menyalahati Cyber Intelligence - Phone Intelligence Module
Intelijen nomor HP dari sumber web publik:
- Truecaller web (nama pemilik, kategori spam)
- GetContact lookup (nama-nama yang disimpan orang lain)
- Google search nomor HP (berapa banyak halaman menyebut nomor ini)
- cekrekening.id (laporan penipuan)
- WhatsApp Business status

⚡ Gratis - Tidak butuh API Key
"""

import re
import time
import random
import requests
from typing import Dict, List, Optional
from urllib.parse import quote

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False

try:
    from googlesearch import search as google_search
    GOOGLE_SEARCH_AVAILABLE = True
except ImportError:
    GOOGLE_SEARCH_AVAILABLE = False


# ─── User Agents ──────────────────────────────────────────────
_UAS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Android 13; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.134 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
]

def _ua() -> str:
    return random.choice(_UAS)

def _get(url: str, timeout: int = 10) -> Optional[requests.Response]:
    try:
        time.sleep(random.uniform(0.5, 1.5))
        headers = {
            "User-Agent": _ua(),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8",
            "Referer": "https://www.google.com/",
        }
        return requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
    except Exception:
        return None


# ─── Normalisasi Nomor ─────────────────────────────────────────
def normalize_phone(phone: str) -> Dict:
    """
    Normalisasi nomor HP Indonesia ke berbagai format.
    Returns dict dengan semua format yang dibutuhkan untuk search.
    """
    if not phone:
        return {}

    # Hapus semua karakter selain digit
    digits = re.sub(r"[^\d]", "", phone)

    # Normalisasi ke format standar
    if digits.startswith("62"):
        local = "0" + digits[2:]
        e164 = "+" + digits
        intl = digits
    elif digits.startswith("0"):
        local = digits
        e164 = "+62" + digits[1:]
        intl = "62" + digits[1:]
    elif digits.startswith("8") and len(digits) >= 9:
        local = "0" + digits
        e164 = "+62" + digits
        intl = "62" + digits
    else:
        local = digits
        e164 = "+62" + digits
        intl = "62" + digits

    # Variasi format untuk search
    formatted = f"{local[:4]}-{local[4:8]}-{local[8:]}" if len(local) >= 12 else local
    formatted2 = f"{local[:4]} {local[4:8]} {local[8:]}" if len(local) >= 12 else local

    return {
        "original": phone,
        "local": local,        # 081338176565
        "e164": e164,          # +6281338176565
        "intl": intl,          # 6281338176565
        "formatted": formatted, # 0813-3817-6565
        "formatted2": formatted2, # 0813 3817 6565
        "search_variants": list(set([local, e164, intl, formatted, formatted2])),
    }


# ══════════════════════════════════════════════════════════════
# TRUECALLER WEB LOOKUP
# ══════════════════════════════════════════════════════════════
# ══════════════════════════════════════════════════════════════
# TRUECALLER WEB LOOKUP
# ══════════════════════════════════════════════════════════════
def lookup_truecaller(phone: str) -> Dict:
    """
    Lookup nomor di Truecaller & web OSINT.
    Extract nama pemilik & status spammer.
    """
    norm = normalize_phone(phone)
    if not norm:
        return {"success": False, "error": "Format nomor tidak valid"}

    result = {
        "success": True,
        "source": "truecaller",
        "phone": norm["e164"],
        "name": "",
        "is_spam": False,
        "spam_score": 0,
        "spam_type": "",
        "country": "Indonesia",
        "operator": "",
        "reports": 0,
        "url": f"https://www.truecaller.com/search/id/{norm['local']}",
        "exposure_score": 0,
        "details": [],
    }

    try:
        from modules.real_scraper import search_web
        q = f'site:truecaller.com "{norm["local"]}" OR "{norm["e164"]}"'
        s_res = search_web(q, num_results=5)

        if s_res.get("items"):
            for item in s_res["items"]:
                title = item.get("title", "")
                snippet = item.get("snippet", "")
                text = f"{title} {snippet}"

                if "truecaller" in title.lower():
                    clean_title = re.sub(r'(?i)\b(truecaller|search|lookup|number|phone|indonesia|id)\b', '', title).strip(" -|:")
                    if clean_title and len(clean_title) >= 3 and not any(w in clean_title.lower() for w in ["wikipedia", "google", "facebook", "download"]):
                        result["name"] = clean_title[:30]
                        break

                if any(k in text.lower() for k in ["spam", "penipu", "dc pinjol", "debt collector", "teror", "spammer"]):
                    result["is_spam"] = True
                    result["spam_score"] = 80
                    result["spam_type"] = "Dilaporkan Spam / DC Pinjol"

    except Exception:
        pass

    if result["name"]:
        result["exposure_score"] = 60
        result["details"].append(f"Nama terdeteksi di Truecaller: {result['name']}")
    elif result["is_spam"]:
        result["exposure_score"] = 80
        result["details"].append("🚨 Nomor terindikasi spam / DC Pinjol di Truecaller")
    else:
        result["details"].append("Nomor belum terindeks publik di Truecaller Web. Cek via tombol Direct Probe.")

    return result


# ══════════════════════════════════════════════════════════════
# GETCONTACT WEB LOOKUP
# ══════════════════════════════════════════════════════════════
def lookup_getcontact(phone: str) -> Dict:
    """
    Lookup nama-nama yang disimpan orang lain untuk nomor ini di GetContact.
    Extract tag kontak & saved names dari OSINT pencarian web.
    """
    norm = normalize_phone(phone)
    if not norm:
        return {"success": False, "error": "Format nomor tidak valid"}

    result = {
        "success": True,
        "source": "getcontact",
        "phone": norm["e164"],
        "saved_names": [],
        "save_count": 0,
        "tags": [],
        "exposure_score": 0,
        "url": f"https://getcontact.com/en/search?q={quote(norm['e164'])}",
        "details": [],
    }

    try:
        from modules.real_scraper import search_web
        q = f'"getcontact" "{norm["local"]}" OR "{norm["e164"]}" OR "tag" "{norm["local"]}"'
        s_res = search_web(q, num_results=5)

        extracted_names = set()
        if s_res.get("items"):
            for item in s_res["items"]:
                text = f"{item.get('title','')} {item.get('snippet','')}"
                tags_found = re.findall(r'#([A-Za-z0-9_\-]{3,30})', text)
                for t in tags_found:
                    if t.lower() not in ["getcontact", "whatsapp", "phone", "telepon", "indonesia", "search", "app"]:
                        extracted_names.add(t)

                saved_matches = re.findall(r'(?:disimpan|tag|nama)\s*[:\-]?\s*"([^"]{3,40})"', text, re.IGNORECASE)
                for sm in saved_matches:
                    if sm.lower() not in ["getcontact", "whatsapp"]:
                        extracted_names.add(sm.strip())

        if extracted_names:
            result["saved_names"] = list(extracted_names)
            result["save_count"] = len(result["saved_names"])
            result["exposure_score"] = min(30 + result["save_count"] * 10, 90)
            result["details"].append(f"Disimpan dalam {result['save_count']} tag kontak publik")
        else:
            result["details"].append("Tidak ada tag kontak publik yang bocor di pencarian web. Gunakan tombol Direct Probe GetContact untuk melihat via aplikasi.")

    except Exception:
        pass

    return result


# ══════════════════════════════════════════════════════════════
# GOOGLE SEARCH - PHONE MENTIONS
# ══════════════════════════════════════════════════════════════
def count_phone_google_mentions(phone: str) -> Dict:
    """
    Hitung berapa banyak halaman publik yang menyebut nomor HP ini di web/Google.
    """
    norm = normalize_phone(phone)
    if not norm:
        return {"success": False, "total_mentions": 0}

    result = {
        "success": True,
        "phone": norm["e164"],
        "total_mentions": 0,
        "urls_found": [],
        "categories": {
            "marketplace": 0,
            "social_media": 0,
            "paste_sites": 0,
            "forums": 0,
            "news": 0,
            "other": 0,
        },
        "exposure_score": 0,
        "details": [],
    }

    try:
        from modules.real_scraper import search_web
        q = f'"{norm["local"]}" OR "{norm["e164"]}"'
        s_res = search_web(q, num_results=10)

        items = s_res.get("items", [])
        result["total_mentions"] = len(items)
        result["urls_found"] = [it.get("url", "") for it in items]

        domain_categories = {
            "marketplace": ["tokopedia", "shopee", "olx", "bukalapak", "tokobagus"],
            "social_media": ["facebook", "instagram", "tiktok", "twitter", "youtube", "wa.me"],
            "paste_sites": ["pastebin", "rentry", "ghostbin", "hastebin", "paste", "t.me"],
            "forums": ["kaskus", "reddit", "forum", "lowyat", "detikforum"],
            "news": ["detik", "kompas", "tribun", "liputan6", "cnnindonesia"],
        }

        for item in items:
            url_lower = item.get("url", "").lower()
            categorized = False
            for cat, keywords in domain_categories.items():
                if any(kw in url_lower for kw in keywords):
                    result["categories"][cat] += 1
                    categorized = True
                    break
            if not categorized:
                result["categories"]["other"] += 1

        score = min(result["total_mentions"] * 8, 50)
        score += result["categories"]["paste_sites"] * 15
        score += result["categories"]["social_media"] * 10
        score += result["categories"]["marketplace"] * 5

        result["exposure_score"] = min(score, 100)

        if result["total_mentions"] > 0:
            result["details"].append(f"Nomor muncul di {result['total_mentions']} halaman publik web")
        if result["categories"]["paste_sites"] > 0:
            result["details"].append(f"⚠️ KRITIS: Nomor muncul di {result['categories']['paste_sites']} paste/dump site!")

    except Exception as e:
        result["error"] = str(e)

    return result


# ══════════════════════════════════════════════════════════════
# CEKREKENING & KREDIBEL FRAUD CHECKER
# ══════════════════════════════════════════════════════════════
def check_fraud_reports(nomor: str) -> Dict:
    """
    Cek laporan penipuan/fraud nomor HP di Kredibel.co, CekRekening.id & web.
    """
    if not nomor:
        return {"has_report": False, "report_count": 0}

    norm = normalize_phone(nomor)
    local = norm.get("local", nomor)

    result = {
        "nomor": nomor,
        "clean": local,
        "has_report": False,
        "report_count": 0,
        "exposure_score": 0,
        "details": [],
        "url_kredibel": f"https://www.kredibel.co/search/phone/{local}",
        "url_cekrekening": f"https://cekrekening.id/search/rekening/{local}",
    }

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept-Language": "id-ID,id;q=0.9",
        }
        r = requests.get(result["url_kredibel"], headers=headers, timeout=5)
        if r.status_code == 200 and BS4_AVAILABLE:
            page_text = r.text.lower()
            if "terlaporkan" in page_text or "penipuan" in page_text or "laporan" in page_text:
                m = re.search(r'(\d+)\s*(?:laporan|kasus|keluhan)', page_text)
                if m:
                    cnt = int(m.group(1))
                    if cnt > 0:
                        result["has_report"] = True
                        result["report_count"] = cnt
                        result["details"].append(f"🚨 {cnt} laporan penipuan ditemukan di Kredibel.co")
    except Exception:
        pass

    if not result["has_report"]:
        try:
            from modules.real_scraper import search_web
            q = f'"{local}" penipuan OR fraud OR "laporan penipuan" OR cekrekening OR kredibel'
            s_res = search_web(q, num_results=5)
            if s_res.get("items"):
                for item in s_res["items"]:
                    snippet = item.get("snippet", "").lower()
                    if any(k in snippet for k in ["penipuan", "penipu", "dilaporkan", "laporan", "scammer", "fraud"]):
                        result["has_report"] = True
                        result["report_count"] += 1
                        result["details"].append(f"🚨 Indikasi laporan penipuan/fraud terdeteksi di {item.get('display_url', 'web')}")
        except Exception:
            pass

    if result["has_report"]:
        result["exposure_score"] = min(40 + result["report_count"] * 15, 95)
    else:
        result["details"].append("🟢 Belum ada laporan penipuan publik terdaftar")

    return result


# ══════════════════════════════════════════════════════════════
# FULL PHONE INTELLIGENCE
# ══════════════════════════════════════════════════════════════
def run_phone_intelligence(phone: str, name: str = "", progress_callback=None) -> Dict:
    """
    Jalankan semua pemeriksaan intelijen nomor HP secara lengkap.

    Returns:
        Agregasi hasil dari semua sumber + total phone exposure score
    """
    if not phone:
        return {"success": False, "error": "Nomor HP kosong"}

    norm = normalize_phone(phone)
    results = {
        "phone_normalized": norm,
        "truecaller": {},
        "getcontact": {},
        "google_mentions": {},
        "fraud_reports": {},
        "total_phone_score": 0,
        "risk_indicators": [],
    }

    tasks = [
        ("Truecaller lookup", lambda: lookup_truecaller(phone)),
        ("GetContact lookup", lambda: lookup_getcontact(phone)),
        ("Google mentions scan", lambda: count_phone_google_mentions(phone)),
        ("Fraud report check", lambda: check_fraud_reports(phone)),
    ]

    for i, (label, fn) in enumerate(tasks):
        if progress_callback:
            try:
                progress_callback(i, len(tasks), f"📞 {label}...")
            except Exception:
                pass
        try:
            result = fn()
            key = label.split()[0].lower()
            if "truecaller" in label.lower():
                results["truecaller"] = result
            elif "getcontact" in label.lower():
                results["getcontact"] = result
            elif "google" in label.lower():
                results["google_mentions"] = result
            elif "fraud" in label.lower():
                results["fraud_reports"] = result
        except Exception as e:
            pass

    # Agregasi score
    weights = {
        "truecaller": 0.20,
        "getcontact": 0.25,
        "google_mentions": 0.35,
        "fraud_reports": 0.20,
    }

    total = 0
    for key, weight in weights.items():
        score = results.get(key, {}).get("exposure_score", 0)
        total += score * weight

    results["total_phone_score"] = min(round(total), 100)

    # Risk indicators
    if results["fraud_reports"].get("has_report"):
        results["risk_indicators"].append("🚨 Nomor dilaporkan penipuan di cekrekening.id")
    if results["google_mentions"].get("categories", {}).get("paste_sites", 0) > 0:
        results["risk_indicators"].append("🚨 Nomor muncul di paste/dump site - kemungkinan doxing aktif")
    if results["truecaller"].get("name"):
        results["risk_indicators"].append(
            f"⚠️ Nama pemilik terekspos di Truecaller: {results['truecaller']['name']}"
        )
    if results["getcontact"].get("save_count", 0) > 10:
        results["risk_indicators"].append(
            f"⚠️ Nomor disimpan {results['getcontact']['save_count']}x dengan nama berbeda di GetContact"
        )
    if results["google_mentions"].get("total_mentions", 0) > 5:
        results["risk_indicators"].append(
            f"⚠️ Nomor muncul di {results['google_mentions']['total_mentions']} halaman publik"
        )

    return results
