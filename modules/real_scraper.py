"""
Menyalahati Cyber Intelligence - Real Scraper Engine v2
Pencarian data nyata menggunakan DuckDuckGo HTML scraping.

WHY DuckDuckGo?
- Google mengembalikan halaman JavaScript-only (tidak bisa di-scrape langsung)
- DuckDuckGo HTML endpoint (html.duckduckgo.com) mengembalikan HTML statis
- Tidak butuh JS, tidak butuh API Key, GRATIS
- Hasil akurat (DuckDuckGo mengindeks konten Google juga)

Fallback: Bing search jika DDG tidak tersedia

⚡ Mode: FREE - Tidak butuh API Key apapun
⚠️  Rate limit: Beri delay antar query untuk hindari block
"""

import re
import time
import random
import hashlib
import requests
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from urllib.parse import unquote, quote_plus
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False

try:
    from fake_useragent import UserAgent
    _ua = UserAgent()
    def get_ua():
        try:
            return _ua.chrome
        except Exception:
            return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    UA_AVAILABLE = True
except ImportError:
    def get_ua():
        agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        ]
        return random.choice(agents)
    UA_AVAILABLE = False

# googlesearch-python tetap diimpor sebagai alternatif terakhir
try:
    from googlesearch import search as _gsearch
    GOOGLE_LIB_AVAILABLE = True
except ImportError:
    GOOGLE_LIB_AVAILABLE = False


# ─── Simple In-Memory Cache ───────────────────────────────────
_cache: Dict[str, Dict] = {}
CACHE_TTL_MINUTES = 60

def _cache_get(key: str) -> Optional[Dict]:
    if key in _cache:
        entry = _cache[key]
        if datetime.now() < entry["expires"]:
            return entry["data"]
        else:
            del _cache[key]
    return None

def _cache_set(key: str, data, ttl_minutes: int = CACHE_TTL_MINUTES):
    _cache[key] = {
        "data": data,
        "expires": datetime.now() + timedelta(minutes=ttl_minutes),
    }

def _make_cache_key(*args) -> str:
    return hashlib.md5("|".join(str(a) for a in args).encode()).hexdigest()


# ─── HTTP Helper ──────────────────────────────────────────────
def _get_headers(referer: str = "https://www.google.com") -> dict:
    return {
        "User-Agent": get_ua(),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": referer,
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
    }

def _safe_get(url: str, timeout: int = 10, referer: str = "https://www.google.com") -> Optional[requests.Response]:
    """HTTP GET dengan error handling dan retry."""
    try:
        resp = requests.get(
            url,
            headers=_get_headers(referer),
            timeout=timeout,
            allow_redirects=True,
        )
        return resp
    except requests.exceptions.SSLError:
        try:
            resp = requests.get(url, headers=_get_headers(), timeout=timeout, verify=False)
            return resp
        except Exception:
            return None
    except Exception:
        return None


def build_real_dork_queries(
    full_name: str = "",
    phone: str = "",
    email: str = "",
    spouse_family_name: str = "",
    additional_keywords: str = "",
) -> List[Dict]:
    """
    Bangun daftar kueri Google Dork untuk scraping nyata.
    Termasuk deteksi doxing hubungan keluarga/kerabat & kata kunci pekerjaan/kampus.
    """
    queries = []
    name_q = f'"{full_name}"' if full_name else ""

    if full_name:
        queries += [
            # Informasi umum
            {"label": "Informasi Umum Nama", "query": name_q,
             "risk": "medium", "category": "general",
             "description": "Semua referensi nama di internet"},

            # Dokumen bocor
            {"label": "Dokumen Publik (PDF/DOC)",
             "query": f"{name_q} (filetype:pdf OR filetype:doc OR filetype:docx OR filetype:xlsx)",
             "risk": "high", "category": "documents",
             "description": "Dokumen yang mungkin mengandung data pribadi"},

            # KTP & NIK
            {"label": "Data KTP / NIK / Identitas",
             "query": f'{name_q} (KTP OR NIK OR "nomor identitas" OR ijazah OR SKCK OR passport)',
             "risk": "critical", "category": "identity",
             "description": "Dokumen identitas terindeks publik"},

            # Alamat
            {"label": "Alamat Tempat Tinggal",
             "query": f'{name_q} (alamat OR "RT" OR "RW" OR kelurahan OR kecamatan OR domisili OR "kode pos")',
             "risk": "critical", "category": "address",
             "description": "Lokasi tempat tinggal tersebar di internet"},

            # Data keuangan
            {"label": "Data Rekening / Keuangan",
             "query": f'{name_q} (rekening OR "no rek" OR BCA OR BRI OR Mandiri OR BNI OR DANA OR OVO OR "nomor rekening")',
             "risk": "critical", "category": "financial",
             "description": "Informasi keuangan terekspos"},

            # Media sosial
            {"label": "Profil Facebook",
             "query": f'{name_q} site:facebook.com',
             "risk": "high", "category": "social",
             "description": "Profil dan aktivitas di Facebook"},

            {"label": "Profil Instagram",
             "query": f'{name_q} site:instagram.com',
             "risk": "medium", "category": "social",
             "description": "Profil dan foto di Instagram"},

            # Paste & dump sites
            {"label": "Data Dump / Paste Sites",
             "query": f'{name_q} (site:pastebin.com OR site:rentry.co OR site:ghostbin.com OR site:hastebin.com)',
             "risk": "critical", "category": "dump",
             "description": "Data tersebar di situs paste/dump"},

            # Doxing aktif & Tagihan Utang DC Pinjol
            {"label": "Thread Doxing DC & Utang",
             "query": f'{name_q} (utang OR hutang OR "bayar utang" OR pinjol OR tagihan OR "debt collector" OR penipu OR doxing OR doxed)',
             "risk": "critical", "category": "doxing",
             "description": "Deteksi postingan tagihan utang, pinjol, atau teror DC"},

            {"label": "Komentar Doxing di Medsos",
             "query": f'{name_q} (site:instagram.com OR site:facebook.com OR site:tiktok.com) (utang OR hutang OR pinjol OR bayar)',
             "risk": "critical", "category": "doxing",
             "description": "Deteksi komentar teror DC di akun Instagram/Facebook/TikTok"},
        ]

    # Kueri Kerabat / Pasangan / Keluarga (Fitur Utama Deteksi Doxing DC)
    if spouse_family_name.strip():
        fam_raw = spouse_family_name.strip()
        fam_list = [f.strip() for f in fam_raw.split(",") if f.strip()]
        for fam_item in fam_list:
            fam_q = f'"{fam_item}"'
            if full_name:
                queries.append({
                    "label": f"Doxing Kerabat & Utang ({fam_item})",
                    "query": f'{fam_q} (utang OR hutang OR pinjol OR "bayar utang" OR tagihan OR doxing)',
                    "risk": "critical", "category": "family",
                    "description": f"Jejak teror DC atau tagihan utang pada kerabat {fam_item}",
                })
                queries.append({
                    "label": f"Kerabat ({fam_item}) + Target ({full_name})",
                    "query": f'{name_q} {fam_q}',
                    "risk": "critical", "category": "family",
                    "description": f"Kombinasi nama target dan kerabat ({fam_item}) di internet",
                })
            else:
                queries.append({
                    "label": f"Data Kerabat ({fam_item})",
                    "query": fam_q,
                    "risk": "high", "category": "family",
                    "description": f"Pencarian publik nama kerabat {fam_item}",
                })

    # Kueri Kata Kunci Spesifik (Tempat Kerja / Kampus)
    if additional_keywords.strip():
        kw_raw = additional_keywords.strip()
        kw_list = [k.strip() for k in kw_raw.split(",") if k.strip()]
        if kw_list:
            if len(kw_list) == 1:
                kw_q = f'"{kw_list[0]}"' if " " in kw_list[0] else kw_list[0]
            else:
                formatted_kw = " OR ".join([f'"{k}"' if " " in k else k for k in kw_list])
                kw_q = f'({formatted_kw})'
            if full_name:
                queries.append({
                    "label": "Kata Kunci Tambahan + Nama",
                    "query": f'{name_q} {kw_q}',
                    "risk": "high", "category": "keywords",
                    "description": f"Target dikaitkan dengan: {kw_raw}",
                })

    if phone:
        # Normalisasi nomor HP
        ph_clean = phone.replace(" ", "").replace("-", "").replace("+62", "0").replace("62", "0", 1)
        ph_variants = [ph_clean, ph_clean.replace("0", "+62", 1), f"0{ph_clean.lstrip('0')}"]
        ph_query = "(" + " OR ".join([f'"{p}"' for p in set(ph_variants) if p]) + ")"

        queries += [
            {"label": "Nomor HP di Internet",
             "query": ph_query,
             "risk": "high", "category": "phone",
             "description": "Nomor HP terindeks di halaman publik"},

            {"label": "HP di Paste/Dump/Telegram",
             "query": f'{ph_query} (site:pastebin.com OR site:rentry.co OR site:t.me)',
             "risk": "critical", "category": "dump",
             "description": "Nomor HP tersebar di paste/dump/Telegram"},
        ]

        if full_name:
            queries.append({
                "label": "Kombinasi Nama + HP",
                "query": f'{name_q} {ph_query}',
                "risk": "critical", "category": "combined",
                "description": "Nama dan nomor HP muncul bersama - indikasi kuat doxing",
            })

    if email:
        queries += [
            {"label": "Email Terekspos",
             "query": f'"{email}" -site:haveibeenpwned.com',
             "risk": "high", "category": "email",
             "description": "Email terindeks di halaman publik"},

            {"label": "Email di Paste/Dump",
             "query": f'"{email}" site:pastebin.com OR site:rentry.co',
             "risk": "critical", "category": "dump",
             "description": "Email muncul di data dump publik"},
        ]

    return queries


# ─── DuckDuckGo Scraper (Primary Engine) ─────────────────────
def search_duckduckgo(
    query: str,
    num_results: int = 8,
    delay_range: tuple = (0.2, 0.5),
) -> Dict:
    """
    Scrape hasil pencarian dari DuckDuckGo HTML endpoint.
    Menggunakan verify=False untuk mencegah SSLError Hostname Mismatch di Windows.
    """
    if not BS4_AVAILABLE:
        return {
            "success": False,
            "error": "beautifulsoup4 tidak terinstall.",
            "items": [], "engine": "duckduckgo",
        }

    cache_key = _make_cache_key("ddg", query, num_results)
    cached = _cache_get(cache_key)
    if cached:
        return {**cached, "from_cache": True}

    ddg_url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
    headers = {
        "User-Agent": get_ua(),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://duckduckgo.com/",
    }

    try:
        resp = requests.get(ddg_url, headers=headers, timeout=4, verify=False, allow_redirects=True)

        if resp.status_code != 200:
            return {
                "success": False,
                "error": f"DuckDuckGo HTTP {resp.status_code}",
                "items": [], "engine": "duckduckgo",
            }

        soup = BeautifulSoup(resp.text, "lxml")
        items = []

        result_links = soup.find_all("a", class_="result__a", limit=num_results * 2)

        for link in result_links:
            raw_href = link.get("href", "")
            if "uddg=" in raw_href:
                url = unquote(raw_href.split("uddg=")[1].split("&")[0])
            elif raw_href.startswith("http"):
                url = raw_href
            else:
                continue

            if "duckduckgo.com" in url:
                continue

            title = link.get_text(strip=True)[:200] or f"Hasil dari {url}"
            snippet = ""
            parent = link.find_parent("div", class_="result__body") or link.find_parent("div")
            if parent:
                snippet_el = parent.find("a", class_="result__snippet")
                if not snippet_el:
                    texts = [t.strip() for t in parent.strings if t.strip() and t.strip() != title]
                    snippet = " ".join(texts[:3])[:300]
                else:
                    snippet = snippet_el.get_text(strip=True)[:300]

            try:
                from urllib.parse import urlparse
                display_url = urlparse(url).netloc.replace("www.", "")
            except Exception:
                display_url = url[:50]

            if url and title:
                items.append({
                    "title": title,
                    "url": url,
                    "snippet": snippet,
                    "display_url": display_url,
                })

        result = {
            "success": True,
            "items": items[:num_results],
            "total": len(items[:num_results]),
            "engine": "duckduckgo",
            "from_cache": False,
        }

        if items:
            _cache_set(cache_key, result)
        return result

    except Exception as e:
        return {"success": False, "error": f"DDG: {str(e)}", "items": [], "engine": "duckduckgo"}


# ─── Bing Fallback Scraper ────────────────────────────────────
def search_bing(
    query: str,
    num_results: int = 8,
    delay_range: tuple = (0.2, 0.5),
) -> Dict:
    """
    Fallback ke Bing jika DuckDuckGo tidak responsif.
    """
    if not BS4_AVAILABLE:
        return {"success": False, "error": "beautifulsoup4 tidak tersedia", "items": [], "engine": "bing"}

    cache_key = _make_cache_key("bing", query, num_results)
    cached = _cache_get(cache_key)
    if cached:
        return {**cached, "from_cache": True}

    bing_url = f"https://www.bing.com/search?q={quote_plus(query)}&count={num_results*2}&mkt=id-ID&cc=id&setlang=id"
    headers = {
        "User-Agent": get_ua(),
        "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }

    try:
        resp = requests.get(bing_url, headers=headers, timeout=4, verify=False)
        if resp.status_code != 200:
            return {"success": False, "error": f"Bing HTTP {resp.status_code}", "items": [], "engine": "bing"}

        soup = BeautifulSoup(resp.text, "lxml")
        items = []

        for li in soup.find_all("li", class_="b_algo"):
            h2 = li.find("h2")
            a = h2.find("a", href=True) if h2 else None
            if not (h2 and a):
                continue
            url = a.get("href", "")
            if not url.startswith("http"):
                continue
            title = h2.get_text(strip=True)[:200]
            snippet_el = li.find("p")
            snippet = snippet_el.get_text(strip=True)[:300] if snippet_el else ""
            try:
                from urllib.parse import urlparse
                display_url = urlparse(url).netloc.replace("www.", "")
            except Exception:
                display_url = url[:50]

            items.append({"title": title, "url": url, "snippet": snippet, "display_url": display_url})

        result = {"success": True, "items": items, "total": len(items), "engine": "bing", "from_cache": False}
        if items:
            _cache_set(cache_key, result)
        return result

    except Exception as e:
        return {"success": False, "error": f"Error Bing: {str(e)}", "items": [], "engine": "bing"}


# ─── Intel Tag Extractor ──────────────────────────────────────
def extract_intel_tags(title: str, snippet: str, url: str) -> List[str]:
    combined = f"{title} {snippet} {url}".lower()
    tags = []

    if re.search(r'\b\d{16}\b', combined) or any(k in combined for k in ["nik ", "ktp ", "paspor", "ijazah", "skck"]):
        tags.append("🆔 Indikasi Identity / NIK")

    if re.search(r'\b(08\d{8,11}|\+62\d{8,11}|628\d{8,11})\b', combined) or "wa.me/" in combined or "nomor hp" in combined:
        tags.append("📱 Telepon / WhatsApp")

    if re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', combined) or "email" in combined:
        tags.append("📧 Email Address")

    if any(k in combined for k in ["rekening", "bank bca", "bank mandiri", "bank bni", "bank bri", "transfer ke", "virtual account"]):
        tags.append("💳 Rekening Bank")

    if any(k in combined for k in ["jl.", "jalan ", "kelurahan", "kecamatan", "kabupaten", "rt 0", "rw 0", "perumahan", "domisili"]):
        tags.append("📍 Alamat / Domisili")

    if any(k in combined for k in ["utang", "hutang", "pinjol", "bayar utang", "tagihan", "penipu", "collector", "dc pinjol", "doxed", "doxing"]):
        tags.append("🚨 Indikasi Doxing DC / Tagihan Utang")

    if any(k in combined for k in ["pastebin", "rentry", "ghostbin", "justpaste", "leaked", "leak"]):
        tags.append("☠️ Paste / Dump Site")

    if any(domain in combined for domain in ["instagram.com", "facebook.com", "tiktok.com", "twitter.com", "x.com", "linkedin.com"]):
        tags.append("🌐 Profil Social Media")

    if any(ext in combined for ext in [".pdf", ".doc", ".docx", ".xlsx", "filetype:pdf"]):
        tags.append("📄 Dokumen Terindeks")

    return tags if tags else ["🔍 Halaman Web Umum"]


# ─── Yahoo Fallback Scraper ───────────────────────────────────
def search_yahoo(
    query: str,
    num_results: int = 8,
    delay_range: tuple = (0.2, 0.5),
) -> Dict:
    """
    Fallback ketiga ke Yahoo Search.
    """
    if not BS4_AVAILABLE:
        return {"success": False, "error": "beautifulsoup4 tidak tersedia", "items": [], "engine": "yahoo"}

    cache_key = _make_cache_key("yahoo", query, num_results)
    cached = _cache_get(cache_key)
    if cached:
        return {**cached, "from_cache": True}

    yahoo_url = f"https://search.yahoo.com/search?p={quote_plus(query)}&vc=id"
    headers = {
        "User-Agent": get_ua(),
        "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }

    try:
        resp = requests.get(yahoo_url, headers=headers, timeout=4, verify=False)
        if resp.status_code != 200:
            return {"success": False, "error": f"Yahoo HTTP {resp.status_code}", "items": [], "engine": "yahoo"}

        soup = BeautifulSoup(resp.text, "lxml")
        items = []

        for div in soup.find_all("div", class_="dd algo"):
            h3 = div.find("h3")
            a = h3.find("a", href=True) if h3 else None
            if not (h3 and a):
                continue
            url = a.get("href", "")
            if "RU=" in url:
                try:
                    url = unquote(url.split("RU=")[1].split("/RK=")[0])
                except Exception:
                    pass
            if not url.startswith("http"):
                continue

            title = h3.get_text(strip=True)[:200]
            comp = div.find("div", class_="compText") or div.find("p")
            snippet = comp.get_text(strip=True)[:300] if comp else ""

            try:
                from urllib.parse import urlparse
                display_url = urlparse(url).netloc.replace("www.", "")
            except Exception:
                display_url = url[:50]

            tags = extract_intel_tags(title, snippet, url)
            items.append({
                "title": title,
                "url": url,
                "snippet": snippet,
                "display_url": display_url,
                "intel_tags": tags,
            })

        result = {"success": True, "items": items, "total": len(items), "engine": "yahoo", "from_cache": False}
        if items:
            _cache_set(cache_key, result)
        return result

    except Exception as e:
        return {"success": False, "error": f"Error Yahoo: {str(e)}", "items": [], "engine": "yahoo"}


# ─── Relevance Filter Engine ───────────────────────────────────
def is_item_relevant(query: str, item: Dict) -> bool:
    """
    Filter ketat & akurat untuk membuang hasil pencarian tidak relevan (spam, bahasa asing, quotes acak, atau hasil fallback engine).
    """
    title = item.get("title", "")
    snippet = item.get("snippet", "")
    url = item.get("url", "").lower()
    combined = f"{title} {snippet} {url}".lower()

    # 1. Filter Karakter Bahasa Asing (Arab, Cyrillic, Mandarin)
    if re.search(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\u4E00-\u9FFF]', combined):
        return False

    # 2. Filter Judul Fallback / Engine Internal Garbage
    garbage_keywords = [
        "binghomepagequiz", "microsoft rewards", "bing homepage quiz",
        "top 25 quotes", "quote of the day", "a-z quotes",
        "privacy policy", "terms of service", "cookie policy"
    ]
    if any(g in title.lower() for g in garbage_keywords):
        return False

    # 3. Filter site: domain constraint
    site_matches = re.findall(r'site:(\S+)', query.lower())
    if site_matches:
        allowed_domains = [sm.split('/')[0].strip() for sm in site_matches]
        domain_matched = any(dom in url for dom in allowed_domains)
        if not domain_matched:
            return False

    # 4. Filter Target Nama (Jika query mengandung nama dalam tanda petik, e.g. "Kirana Vinzi Apsari")
    name_quotes = re.findall(r'"([A-Za-z\s]{3,40})"', query)
    name_tokens = []
    ignored_phrases = ["nomor identitas", "bayar utang", "debt collector", "laporan penipuan", "kode pos"]
    for nq in name_quotes:
        if nq.lower() not in ignored_phrases:
            # Ambil setidaknya 1 kata kunci nama yang signifikan (>=3 huruf)
            tokens = [t.lower() for t in nq.split() if len(t) >= 3 and t.lower() not in ["utang", "hutang", "pinjol", "doxing", "suami", "istri"]]
            if tokens:
                name_tokens.append(tokens)

    if name_tokens:
        # Paling sedikit 1 grup nama (misal nama target ATAU nama kerabat) harus cocok
        any_name_group_matched = False
        for grp in name_tokens:
            if any(t in combined for t in grp):
                any_name_group_matched = True
                break
        if not any_name_group_matched:
            return False

    # 5. Filter Target Nomor HP
    phone_digits = re.findall(r'\b\d{8,13}\b', query)
    if phone_digits:
        target_ph = phone_digits[0]
        local_target = "0" + target_ph.lstrip("0") if target_ph.startswith("8") else target_ph
        intl_target = "62" + local_target[1:] if local_target.startswith("0") else local_target
        clean_text = combined.replace(" ", "").replace("-", "").replace("+62", "0")

        ph_match = (
            local_target in clean_text or
            intl_target in clean_text or
            local_target[1:] in clean_text or
            any(sub in clean_text for sub in [local_target[:6], local_target[-6:]])
        )
        if not ph_match:
            return False

    return True


# ─── Unified Search (DDG → Bing → Yahoo) ────────────────────
def search_web(
    query: str,
    num_results: int = 8,
    delay_range: tuple = (0.2, 0.5),
) -> Dict:
    """
    Engine pencarian utama multi-source - coba DDG, fallback ke Bing & Yahoo.
    Hasil difilter secara sangat ketat agar 100% relevan dan bebas garbage/spam/SSL error.
    """
    def process_items(raw_items):
        clean_items = []
        for item in raw_items:
            if is_item_relevant(query, item):
                if "intel_tags" not in item:
                    item["intel_tags"] = extract_intel_tags(item.get("title", ""), item.get("snippet", ""), item.get("url", ""))
                clean_items.append(item)
        return clean_items

    # Primary: DuckDuckGo
    res_ddg = search_duckduckgo(query, num_results, delay_range)
    if res_ddg.get("success") and res_ddg.get("items"):
        clean = process_items(res_ddg["items"])
        if clean:
            return {**res_ddg, "items": clean[:num_results], "total": len(clean[:num_results])}

    # Fallback 1: Bing
    res_bing = search_bing(query, num_results, delay_range)
    if res_bing.get("success") and res_bing.get("items"):
        clean = process_items(res_bing["items"])
        if clean:
            return {**res_bing, "items": clean[:num_results], "total": len(clean[:num_results])}

    # Fallback 2: Yahoo
    yahoo_result = search_yahoo(query, num_results, delay_range)
    if yahoo_result.get("success") and yahoo_result.get("items"):
        clean = process_items(yahoo_result["items"])
        if clean:
            return {**yahoo_result, "items": clean[:num_results], "total": len(clean[:num_results])}

    return {"success": True, "items": [], "total": 0, "engine": "multi"}


# ─── Alias untuk kompatibilitas ──────────────────────────────
def scrape_google_results(query: str, num_results: int = 8, delay_range: tuple = (1.5, 3.0)) -> Dict:
    """Alias - sekarang menggunakan DDG bukan Google scraping."""
    return search_web(query, num_results, delay_range)


def enrich_url_with_metadata(url: str) -> Dict:
    """
    Ambil metadata (title, description, OG tags) dari sebuah URL.
    Digunakan untuk memperkaya hasil scraping dengan snippet nyata.
    """
    cache_key = _make_cache_key("meta", url)
    cached = _cache_get(cache_key)
    if cached:
        return cached

    resp = _safe_get(url, timeout=8)
    if not resp or resp.status_code != 200:
        return {"title": "", "description": "", "og_image": ""}

    if not BS4_AVAILABLE:
        return {"title": url, "description": "", "og_image": ""}

    try:
        soup = BeautifulSoup(resp.text[:50000], "lxml" if BS4_AVAILABLE else "html.parser")
        title = ""
        desc = ""
        og_image = ""

        if soup.title:
            title = soup.title.get_text(strip=True)[:200]

        og_title = soup.find("meta", property="og:title")
        if og_title:
            title = og_title.get("content", title)[:200]

        og_desc = soup.find("meta", property="og:description")
        if og_desc:
            desc = og_desc.get("content", "")[:300]
        else:
            meta_desc = soup.find("meta", attrs={"name": "description"})
            if meta_desc:
                desc = meta_desc.get("content", "")[:300]

        og_img = soup.find("meta", property="og:image")
        if og_img:
            og_image = og_img.get("content", "")

        result = {"title": title, "description": desc, "og_image": og_image}
        _cache_set(cache_key, result, ttl_minutes=120)
        return result

    except Exception:
        return {"title": "", "description": "", "og_image": ""}


# ─── Main Scan Function ───────────────────────────────────────
def run_real_dork_scan(
    full_name: str = "",
    phone: str = "",
    email: str = "",
    spouse_family_name: str = "",
    additional_keywords: str = "",
    max_queries: int = 12,
    num_results_per_query: int = 5,
    progress_callback=None,
) -> List[Dict]:
    """
    Jalankan full scan dork nyata (tanpa API berbayar).
    """
    if not BS4_AVAILABLE:
        return [{
            "label": "Error",
            "query": "",
            "risk": "low",
            "category": "error",
            "description": "Library beautifulsoup4 belum terinstall",
            "found_count": 0,
            "result": {
                "success": False,
                "error": "Jalankan: pip install beautifulsoup4 lxml",
                "items": [],
            },
        }]

    queries = build_real_dork_queries(
        full_name=full_name,
        phone=phone,
        email=email,
        spouse_family_name=spouse_family_name,
        additional_keywords=additional_keywords,
    )
    # Batasi jumlah query
    queries = queries[:max_queries]

    results = []
    total = len(queries)

    for i, q in enumerate(queries):
        if progress_callback:
            try:
                progress_callback(i, total, q["label"])
            except Exception:
                pass

        # Jalankan scraping
        search_result = scrape_google_results(
            q["query"],
            num_results=num_results_per_query,
            delay_range=(1.2, 2.5),
        )

        # Enrich top result dengan metadata
        items = search_result.get("items", [])
        if items and not search_result.get("from_cache"):
            top_url = items[0]["url"]
            # Hanya enrich untuk hasil yang menarik (paste, facebook, dll)
            should_enrich = any(
                domain in top_url
                for domain in ["pastebin", "facebook", "instagram", "kaskus", "tokopedia"]
            )
            if should_enrich:
                meta = enrich_url_with_metadata(top_url)
                if meta["title"]:
                    items[0]["title"] = meta["title"]
                if meta["description"]:
                    items[0]["snippet"] = meta["description"]

        results.append({
            "label": q["label"],
            "query": q["query"],
            "risk": q["risk"],
            "category": q["category"],
            "description": q["description"],
            "platform": q.get("platform", ""),
            "direct_url": q.get("direct_url", ""),
            "found_count": len(items),
            "result": search_result,
        })

    return results


# ─── Paste/Dump Checker ───────────────────────────────────────
def check_pastebin_for_data(query: str) -> Dict:
    """
    Cek apakah data target muncul di Pastebin secara spesifik.
    Menggunakan Google untuk search ke dalam Pastebin.
    """
    paste_query = f'{query} site:pastebin.com'
    return scrape_google_results(paste_query, num_results=5, delay_range=(1, 2))


def check_telegram_exposure(name: str, phone: str = "") -> Dict:
    """
    Cek apakah data target tersebar di Telegram public channels.
    Menggunakan Google untuk search t.me
    """
    if phone:
        query = f'site:t.me "{name}" OR "{phone}"'
    else:
        query = f'site:t.me "{name}"'
    return scrape_google_results(query, num_results=5, delay_range=(1, 2))


def check_dark_web_mentions(name: str, phone: str = "") -> Dict:
    """
    Cek referensi di forum-forum terbuka yang sering dipakai untuk doxing.
    (Bukan dark web sebenarnya - forum publik yang diketahui)
    """
    if phone:
        query = f'"{name}" "{phone}" site:kaskus.co.id OR site:lowyat.net OR site:reddit.com'
    else:
        query = f'"{name}" doxed OR doxing OR "info lengkap" OR "data pribadi"'
    return scrape_google_results(query, num_results=5, delay_range=(1, 2))


# ─── Status Check ─────────────────────────────────────────────
def get_engine_status() -> Dict:
    """Cek status ketersediaan semua komponen scraper."""
    return {
        "duckduckgo": BS4_AVAILABLE,
        "beautifulsoup4": BS4_AVAILABLE,
        "fake_useragent": UA_AVAILABLE,
        "cache_entries": len(_cache),
        "ready": BS4_AVAILABLE,
    }
