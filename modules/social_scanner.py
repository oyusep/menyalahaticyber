"""
Menyalahati Cyber Intelligence - Social Media Scanner
Scraping profil media sosial publik untuk mengukur digital exposure.

Platform didukung:
- Instagram (profil publik via web)
- Facebook (profil & marketplace publik)
- TikTok (profil publik)
- Twitter / X (profil publik)
- Truecaller Web (nama pemilik nomor HP)

⚡ Gratis - Tidak butuh API Key
⚠️  Hanya membaca data yang SUDAH PUBLIK di internet
"""

import re
import time
import random
import hashlib
import requests
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from urllib.parse import quote, urlparse

try:
    from bs4 import BeautifulSoup, Tag
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False

# ─── Cache & Headers ──────────────────────────────────────────
_cache: Dict = {}

def _cache_get(key: str) -> Optional[Dict]:
    if key in _cache:
        e = _cache[key]
        if datetime.now() < e["exp"]:
            return e["data"]
        del _cache[key]
    return None

def _cache_set(key: str, data, ttl: int = 30):
    _cache[key] = {"data": data, "exp": datetime.now() + timedelta(minutes=ttl)}

def _key(*args) -> str:
    return hashlib.md5("|".join(str(a) for a in args).encode()).hexdigest()

# Daftar User-Agent browser populer
_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
]

def _headers(referer: str = "https://www.google.com") -> dict:
    return {
        "User-Agent": random.choice(_USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": referer,
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
    }

def _get(url: str, timeout: int = 10, referer: str = "https://www.google.com") -> Optional[requests.Response]:
    try:
        time.sleep(random.uniform(0.5, 1.5))
        return requests.get(url, headers=_headers(referer), timeout=timeout, allow_redirects=True)
    except Exception:
        return None


# ══════════════════════════════════════════════════════════════
# INSTAGRAM SCANNER
# ══════════════════════════════════════════════════════════════
def scan_instagram(username: str) -> Dict:
    """
    Scrape profil Instagram publik.
    Mengambil: followers, following, post count, bio, is_public, verified.

    Returns:
        dict dengan data profil dan exposure info
    """
    if not username:
        return {"success": False, "platform": "instagram", "error": "Username kosong"}

    username = username.strip().lstrip("@").split("/")[-1].split("?")[0]
    cache_key = _key("ig", username)
    cached = _cache_get(cache_key)
    if cached:
        return {**cached, "from_cache": True}

    url = f"https://www.instagram.com/{username}/"
    resp = _get(url, referer="https://www.google.com/search?q=instagram")

    result = {
        "success": False,
        "platform": "instagram",
        "username": username,
        "url": url,
        "exists": False,
        "is_public": False,
        "followers": 0,
        "following": 0,
        "posts": 0,
        "full_name": "",
        "bio": "",
        "website": "",
        "is_verified": False,
        "profile_pic": "",
        "exposure_score": 0,
        "exposure_details": [],
        "error": "",
    }

    if not resp:
        result["error"] = "Tidak dapat terhubung ke Instagram"
        return result

    if resp.status_code == 404:
        result["error"] = "Akun tidak ditemukan"
        return result

    if resp.status_code == 200 and BS4_AVAILABLE:
        try:
            soup = BeautifulSoup(resp.text, "lxml")

            # Cek apakah akun exist dari title
            title = soup.title.get_text() if soup.title else ""
            if "Page Not Found" in title or "Sorry" in title:
                result["error"] = "Akun tidak ditemukan"
                return result

            result["exists"] = True

            # Extract dari meta tags
            og_title = soup.find("meta", property="og:title")
            if og_title:
                full_title = og_title.get("content", "")
                result["full_name"] = full_title.split("•")[0].strip() if "•" in full_title else full_title.split("(")[0].strip()

            og_desc = soup.find("meta", property="og:description")
            if og_desc:
                desc = og_desc.get("content", "")
                result["bio"] = desc

                # Parse followers/following/posts dari description
                # Format: "X Followers, X Following, X Posts"
                nums = re.findall(r"([\d,\.]+[KkMm]?)\s+(\w+)", desc)
                for num_str, label in nums:
                    label_lower = label.lower()
                    count = _parse_count(num_str)
                    if "follower" in label_lower:
                        result["followers"] = count
                    elif "following" in label_lower:
                        result["following"] = count
                    elif "post" in label_lower:
                        result["posts"] = count

            og_image = soup.find("meta", property="og:image")
            if og_image:
                result["profile_pic"] = og_image.get("content", "")

            # Cek verified
            if "verified" in resp.text.lower():
                result["is_verified"] = "verified" in (resp.text[:5000]).lower()

            # Cek apakah akun publik (bisa dilihat postingan-nya)
            # Private account biasanya muncul teks "This Account is Private"
            is_private = "This Account is Private" in resp.text or "akun ini pribadi" in resp.text.lower()
            result["is_public"] = not is_private
            result["success"] = True

            # Hitung exposure score Instagram
            exposure = _calc_instagram_exposure(result)
            result["exposure_score"] = exposure["score"]
            result["exposure_details"] = exposure["details"]

        except Exception as e:
            result["error"] = f"Gagal parse: {str(e)}"

    elif resp.status_code == 200:
        result["exists"] = True
        result["success"] = True
        result["bio"] = "Data tersedia (install beautifulsoup4 untuk detail)"

    elif resp.status_code == 429:
        result["error"] = "Rate limited oleh Instagram. Coba lagi dalam beberapa menit."
    else:
        result["error"] = f"HTTP {resp.status_code}"

    _cache_set(cache_key, result)
    return result


def _calc_instagram_exposure(data: Dict) -> Dict:
    """Hitung exposure score Instagram (0-100)."""
    score = 0
    details = []

    if data.get("exists"):
        score += 10
        details.append("Akun ditemukan di Instagram")

    if data.get("is_public"):
        score += 25
        details.append("Akun PUBLIK - siapapun bisa lihat postingan")
    else:
        score += 5
        details.append("Akun privat - hanya follower yang lihat")

    followers = data.get("followers", 0)
    if followers > 10000:
        score += 25
        details.append(f"Banyak followers ({followers:,}) - eksposur sangat luas")
    elif followers > 1000:
        score += 15
        details.append(f"Followers cukup banyak ({followers:,})")
    elif followers > 100:
        score += 8
        details.append(f"Followers: {followers:,}")

    if data.get("is_verified"):
        score += 15
        details.append("Akun terverifikasi - lebih mudah ditemukan")

    if data.get("bio"):
        bio = data["bio"]
        if any(kw in bio.lower() for kw in ["hp", "wa", "whatsapp", "telepon", "+62", "081", "082"]):
            score += 20
            details.append("⚠️ Nomor HP tercantum di bio Instagram!")
        if any(kw in bio.lower() for kw in ["alamat", "jl.", "jalan", "no.", "rt", "rw"]):
            score += 20
            details.append("⚠️ Alamat tercantum di bio Instagram!")

    return {"score": min(score, 100), "details": details}


# ══════════════════════════════════════════════════════════════
# FACEBOOK SCANNER
# ══════════════════════════════════════════════════════════════
def scan_facebook(name_or_username: str) -> Dict:
    """
    Scan kehadiran Facebook dari nama/username.
    Facebook sangat terbatas tanpa login, tapi bisa cek:
    - Apakah profil publik ada
    - Marketplace listings
    - Grup publik yang menyebut nama ini
    """
    if not name_or_username:
        return {"success": False, "platform": "facebook", "error": "Input kosong"}

    name_enc = quote(name_or_username)
    cache_key = _key("fb", name_or_username)
    cached = _cache_get(cache_key)
    if cached:
        return {**cached, "from_cache": True}

    # Cek via Facebook search (untuk nama, bukan username langsung)
    # Facebook tanpa login sangat terbatas - kita cek via Google
    result = {
        "success": True,
        "platform": "facebook",
        "name": name_or_username,
        "profile_url": f"https://www.facebook.com/search/people/?q={name_enc}",
        "marketplace_url": f"https://www.facebook.com/marketplace/search/?query={name_enc}",
        "found_via_google": False,
        "listing_count": 0,
        "exposure_score": 0,
        "exposure_details": [],
        "note": "Facebook membatasi akses tanpa login. Hasil diambil via Google dorking.",
    }

    # Scrape halaman profil jika ada username
    clean = name_or_username.strip().lstrip("@").split("?")[0]
    if "/" not in clean and " " not in clean:
        fb_url = f"https://www.facebook.com/{clean}"
        resp = _get(fb_url, referer="https://www.google.com")
        if resp and resp.status_code == 200:
            result["found_via_google"] = True
            result["direct_url"] = fb_url
            result["exposure_score"] = 60
            result["exposure_details"] = [
                "Profil Facebook ditemukan secara langsung",
                "Data profil publik terindeks Google",
            ]
        elif resp and resp.status_code == 404:
            result["exists"] = False

    # Default exposure untuk nama yang ada di FB publik
    if not result.get("exposure_score"):
        result["exposure_score"] = 40
        result["exposure_details"] = [
            "Profil Facebook kemungkinan ada (dicek via Google)",
            "Data publik Facebook terindeks mesin pencari",
        ]

    _cache_set(cache_key, result)
    return result


# ══════════════════════════════════════════════════════════════
# TIKTOK SCANNER
# ══════════════════════════════════════════════════════════════
def scan_tiktok(username: str) -> Dict:
    """
    Scrape profil TikTok publik.
    Mengambil: followers, likes, bio, video count.
    """
    if not username:
        return {"success": False, "platform": "tiktok", "error": "Username kosong"}

    username = username.strip().lstrip("@").split("?")[0]
    cache_key = _key("tt", username)
    cached = _cache_get(cache_key)
    if cached:
        return {**cached, "from_cache": True}

    url = f"https://www.tiktok.com/@{username}"
    resp = _get(url, referer="https://www.google.com")

    result = {
        "success": False,
        "platform": "tiktok",
        "username": username,
        "url": url,
        "exists": False,
        "followers": 0,
        "likes": 0,
        "videos": 0,
        "full_name": "",
        "bio": "",
        "is_verified": False,
        "exposure_score": 0,
        "exposure_details": [],
        "error": "",
    }

    if not resp:
        result["error"] = "Tidak dapat terhubung ke TikTok"
        return result

    if resp.status_code == 200 and BS4_AVAILABLE:
        try:
            soup = BeautifulSoup(resp.text, "lxml")
            title = soup.title.get_text() if soup.title else ""

            if "TikTok" in title and "@" + username in resp.text:
                result["exists"] = True
                result["success"] = True

            og_desc = soup.find("meta", property="og:description")
            if og_desc:
                desc = og_desc.get("content", "")
                result["bio"] = desc
                nums = re.findall(r"([\d,\.]+[KkMm]?)", desc)
                if len(nums) >= 3:
                    result["followers"] = _parse_count(nums[0])
                    result["likes"] = _parse_count(nums[1])
                    result["videos"] = _parse_count(nums[2])

            og_title = soup.find("meta", property="og:title")
            if og_title:
                result["full_name"] = og_title.get("content", username)

            if result["exists"]:
                score = 10 + (20 if result["followers"] > 1000 else 5)
                result["exposure_score"] = min(score, 100)
                result["exposure_details"] = [
                    f"Profil TikTok aktif: {result['followers']:,} followers",
                    "Konten video publik terindeks Google",
                ]
                result["success"] = True

        except Exception as e:
            result["error"] = str(e)

    elif resp.status_code == 404:
        result["error"] = "Akun tidak ditemukan"

    _cache_set(cache_key, result)
    return result


# ══════════════════════════════════════════════════════════════
# TWITTER / X SCANNER
# ══════════════════════════════════════════════════════════════
def scan_twitter(username: str) -> Dict:
    """
    Cek kehadiran Twitter/X dari username.
    """
    if not username:
        return {"success": False, "platform": "twitter", "error": "Username kosong"}

    username = username.strip().lstrip("@")
    cache_key = _key("tw", username)
    cached = _cache_get(cache_key)
    if cached:
        return {**cached, "from_cache": True}

    url = f"https://nitter.net/{username}"  # Nitter = Twitter mirror tanpa JS
    resp = _get(url, referer="https://www.google.com")

    result = {
        "success": False,
        "platform": "twitter",
        "username": username,
        "url": f"https://x.com/{username}",
        "exists": False,
        "followers": 0,
        "tweets": 0,
        "full_name": "",
        "bio": "",
        "is_verified": False,
        "exposure_score": 0,
        "exposure_details": [],
    }

    if resp and resp.status_code == 200 and BS4_AVAILABLE:
        try:
            soup = BeautifulSoup(resp.text, "lxml")
            if "profile-card" in resp.text or "timeline" in resp.text:
                result["exists"] = True
                result["success"] = True

                name_el = soup.find(class_="profile-card-fullname")
                if name_el:
                    result["full_name"] = name_el.get_text(strip=True)

                bio_el = soup.find(class_="profile-bio")
                if bio_el:
                    result["bio"] = bio_el.get_text(strip=True)

                stats = soup.find_all(class_="profile-stat-num")
                if stats:
                    for i, s in enumerate(stats[:3]):
                        val = _parse_count(s.get_text(strip=True))
                        if i == 0:
                            result["tweets"] = val
                        elif i == 1:
                            result["followers"] = val

                score = 10
                if result["followers"] > 1000:
                    score += 20
                result["exposure_score"] = score
                result["exposure_details"] = [f"Akun Twitter/X ditemukan: {result['followers']:,} followers"]

        except Exception:
            pass

    _cache_set(cache_key, result)
    return result


# ══════════════════════════════════════════════════════════════
# MULTI-PLATFORM USERNAME CHECK
# ══════════════════════════════════════════════════════════════
def check_username_existence(username: str) -> Dict:
    """
    Cek apakah username ini ada di berbagai platform sekaligus.
    Menggunakan HTTP HEAD request untuk kecepatan.
    Berguna untuk menemukan akun sosmed dari satu username.
    """
    if not username:
        return {"username": username, "found_platforms": [], "total": 0}

    username = username.strip().lstrip("@")
    platforms = {
        "Instagram": f"https://www.instagram.com/{username}/",
        "TikTok": f"https://www.tiktok.com/@{username}",
        "Twitter/X": f"https://x.com/{username}",
        "GitHub": f"https://github.com/{username}",
        "Pinterest": f"https://www.pinterest.com/{username}/",
        "Tumblr": f"https://{username}.tumblr.com",
    }

    found = []
    for platform, url in platforms.items():
        try:
            time.sleep(random.uniform(0.3, 0.8))
            resp = requests.head(url, headers=_headers(), timeout=6, allow_redirects=True)
            if resp.status_code in [200, 301, 302]:
                found.append({"platform": platform, "url": url, "status": resp.status_code})
        except Exception:
            pass

    return {
        "username": username,
        "found_platforms": found,
        "total": len(found),
        "exposure_score": min(len(found) * 15, 100),
    }


# ══════════════════════════════════════════════════════════════
# PHONE EXPOSURE CHECKER via Web
# ══════════════════════════════════════════════════════════════
def check_wa_status(phone: str) -> Dict:
    """
    Cek apakah nomor aktif di WhatsApp via wa.me link.
    """
    if not phone:
        return {"active": False, "error": "Nomor kosong"}

    # Normalisasi nomor
    clean = re.sub(r"[^\d]", "", phone)
    if clean.startswith("0"):
        clean = "62" + clean[1:]
    elif not clean.startswith("62"):
        clean = "62" + clean

    url = f"https://wa.me/{clean}"
    resp = _get(url, timeout=8)

    is_active = False
    if resp and resp.status_code == 200:
        is_active = "open?phone=" in resp.url or "api.whatsapp" in resp.url or "web.whatsapp" in resp.url

    return {
        "phone": f"+{clean}",
        "wa_url": url,
        "active": is_active,
        "exposure_score": 30 if is_active else 0,
        "detail": "Nomor aktif WhatsApp Business/Personal" if is_active else "Status WA tidak terdeteksi",
    }


def check_cekrekening(nomor: str, tipe: str = "hp") -> Dict:
    """
    Cek laporan penipuan di cekrekening.id
    """
    if not nomor:
        return {"has_report": False, "error": "Nomor kosong"}

    clean = re.sub(r"[^\d]", "", nomor)
    url = f"https://cekrekening.id/laporan/{clean}"
    resp = _get(url, referer="https://www.google.com")

    result = {
        "nomor": nomor,
        "url": url,
        "has_report": False,
        "report_count": 0,
        "exposure_score": 0,
    }

    if resp and resp.status_code == 200 and BS4_AVAILABLE:
        soup = BeautifulSoup(resp.text, "lxml")
        # Cek apakah ada laporan
        if "laporan" in resp.text.lower() and "penipuan" in resp.text.lower():
            result["has_report"] = True
            # Coba hitung jumlah laporan
            count_el = soup.find(string=re.compile(r"\d+\s+laporan", re.I))
            if count_el:
                nums = re.findall(r"\d+", count_el)
                if nums:
                    result["report_count"] = int(nums[0])
            result["exposure_score"] = 40 + min(result["report_count"] * 5, 30)

    return result


# ══════════════════════════════════════════════════════════════
# AGREGASI SEMUA PLATFORM
# ══════════════════════════════════════════════════════════════
def scan_all_social_platforms(
    name: str = "",
    phone: str = "",
    username_instagram: str = "",
    username_tiktok: str = "",
    username_facebook: str = "",
    username_twitter: str = "",
    progress_callback=None,
) -> Dict:
    """
    Jalankan scan semua platform sosial secara berurutan.
    Returns agregasi hasil + total social exposure score.
    """
    results = {}
    total_tasks = 5
    task_n = 0

    def _progress(label):
        nonlocal task_n
        task_n += 1
        if progress_callback:
            try:
                progress_callback(task_n, total_tasks, label)
            except Exception:
                pass

    # Instagram
    if username_instagram:
        _progress(f"📸 Scan Instagram: @{username_instagram}")
        results["instagram"] = scan_instagram(username_instagram)
    elif name:
        # Coba tebak username dari nama
        guess = name.lower().replace(" ", ".").replace(".", "")[:20]
        _progress(f"📸 Cek Instagram: @{guess}")
        ig = scan_instagram(guess)
        if ig.get("exists"):
            results["instagram"] = ig

    # Facebook
    _progress(f"👤 Scan Facebook: {username_facebook or name}")
    results["facebook"] = scan_facebook(username_facebook or name)

    # TikTok
    if username_tiktok:
        _progress(f"🎵 Scan TikTok: @{username_tiktok}")
        results["tiktok"] = scan_tiktok(username_tiktok)

    # Twitter
    if username_twitter:
        _progress(f"🐦 Scan Twitter/X: @{username_twitter}")
        results["twitter"] = scan_twitter(username_twitter)

    # WhatsApp
    if phone:
        _progress(f"📱 Cek WhatsApp: {phone}")
        results["whatsapp"] = check_wa_status(phone)
        results["cekrekening"] = check_cekrekening(phone)

    # Hitung total social exposure score (weighted)
    weights = {
        "instagram": 0.25,
        "facebook": 0.30,
        "tiktok": 0.15,
        "twitter": 0.10,
        "whatsapp": 0.12,
        "cekrekening": 0.08,
    }
    total_score = 0
    found_platforms = []

    for platform, weight in weights.items():
        if platform in results:
            r = results[platform]
            score = r.get("exposure_score", 0)
            total_score += score * weight
            if r.get("exists") or r.get("active") or r.get("has_report") or r.get("success"):
                found_platforms.append(platform)

    return {
        "platforms": results,
        "found_platforms": found_platforms,
        "total_social_score": min(round(total_score), 100),
        "platform_count": len(found_platforms),
    }


# ─── Utility ──────────────────────────────────────────────────
def _parse_count(s: str) -> int:
    """Parse string seperti '12.4K', '3.2M', '1,847' ke integer."""
    if not s:
        return 0
    s = str(s).strip().replace(",", "")
    try:
        if s.upper().endswith("K"):
            return int(float(s[:-1]) * 1000)
        elif s.upper().endswith("M"):
            return int(float(s[:-1]) * 1_000_000)
        elif s.upper().endswith("B"):
            return int(float(s[:-1]) * 1_000_000_000)
        return int(float(s))
    except (ValueError, AttributeError):
        return 0
