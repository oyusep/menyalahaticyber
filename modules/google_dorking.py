"""
OSINT Cyber Guardian - Google Dorking Engine
Menggunakan Google Custom Search JSON API untuk mendeteksi data terindeks publik
"""
import requests
import time
from typing import List, Dict, Optional


# Mapping platform ke domain dan ikon
PLATFORM_META = {
    "instagram": {
        "domain": "instagram.com",
        "label": "Instagram",
        "icon": "📸",
        "url_pattern": "https://instagram.com/{username}",
        "risk": "medium",
    },
    "tiktok": {
        "domain": "tiktok.com",
        "label": "TikTok",
        "icon": "🎵",
        "url_pattern": "https://tiktok.com/@{username}",
        "risk": "medium",
    },
    "facebook": {
        "domain": "facebook.com",
        "label": "Facebook",
        "icon": "👤",
        "url_pattern": "https://facebook.com/{username}",
        "risk": "high",  # FB lebih banyak info pribadi
    },
    "twitter": {
        "domain": "twitter.com OR site:x.com",
        "label": "Twitter / X",
        "icon": "🐦",
        "url_pattern": "https://x.com/{username}",
        "risk": "medium",
    },
    "linkedin": {
        "domain": "linkedin.com",
        "label": "LinkedIn",
        "icon": "💼",
        "url_pattern": "https://linkedin.com/in/{username}",
        "risk": "high",  # Berisi info profesional/kantor
    },
    "youtube": {
        "domain": "youtube.com",
        "label": "YouTube",
        "icon": "▶️",
        "url_pattern": "https://youtube.com/@{username}",
        "risk": "low",
    },
    "reddit": {
        "domain": "reddit.com",
        "label": "Reddit",
        "icon": "🟠",
        "url_pattern": "https://reddit.com/u/{username}",
        "risk": "medium",
    },
    "github": {
        "domain": "github.com",
        "label": "GitHub",
        "icon": "🐙",
        "url_pattern": "https://github.com/{username}",
        "risk": "low",
    },
}


def build_dork_queries(
    full_name: str = "",
    phone: str = "",
    email: str = "",
    spouse_family_name: str = "",
    additional_keywords: str = "",
    # Per-platform social media usernames
    username_instagram: str = "",
    username_tiktok: str = "",
    username_facebook: str = "",
    username_twitter: str = "",
    username_linkedin: str = "",
    username_youtube: str = "",
    username_reddit: str = "",
    username_github: str = "",
) -> List[Dict[str, str]]:
    """
    Bangun daftar kueri Google Dork berdasarkan input data target.
    Social media dipisah per platform untuk dork yang lebih presisi.
    Termasuk pencarian kerabat/keluarga & kata kunci tambahan.
    """
    queries = []

    # ── Kueri berbasis Nama ───────────────────────────────
    if full_name:
        name_q = f'"{full_name}"'
        queries += [
            {
                "label": "Informasi Umum Nama",
                "query": name_q,
                "risk": "medium",
                "description": "Mencari semua referensi nama di internet",
            },
            {
                "label": "Dokumen Publik (PDF/DOC)",
                "query": f"{name_q} (filetype:pdf OR filetype:doc OR filetype:docx OR filetype:xlsx)",
                "risk": "high",
                "description": "Dokumen seperti ijazah, SK, kontrak yang mungkin bocor",
            },
            {
                "label": "Data KTP / NIK / Ijazah",
                "query": f'{name_q} (KTP OR NIK OR "nomor identitas" OR ijazah OR SKCK)',
                "risk": "critical",
                "description": "Dokumen identitas yang mungkin terindeks publik",
            },
            {
                "label": "Informasi Alamat Tempat Tinggal",
                "query": f'{name_q} (alamat OR "RT" OR "RW" OR kelurahan OR kecamatan OR domisili)',
                "risk": "critical",
                "description": "Data lokasi tempat tinggal",
            },
            {
                "label": "Data Pekerjaan / Kantor",
                "query": f'{name_q} (kantor OR perusahaan OR jabatan OR "tempat kerja" OR divisi)',
                "risk": "high",
                "description": "Informasi pekerjaan yang mungkin terekspos",
            },
            {
                "label": "Thread Doxing DC & Utang",
                "query": f'{name_q} (utang OR hutang OR "bayar utang" OR pinjol OR tagihan OR "debt collector" OR penipu OR doxing)',
                "risk": "critical",
                "description": "Deteksi postingan tagihan utang, pinjol, atau teror DC",
            },
            {
                "label": "Komentar Doxing di Medsos",
                "query": f'{name_q} (site:instagram.com OR site:facebook.com OR site:tiktok.com) (utang OR hutang OR pinjol OR bayar)',
                "risk": "critical",
                "description": "Deteksi komentar teror DC di akun Instagram/Facebook/TikTok",
            },
        ]

    # Kueri Kerabat / Pasangan / Keluarga (Fitur Utama Deteksi Doxing DC)
    if spouse_family_name.strip():
        fam_name = spouse_family_name.strip()
        fam_q = f'"{fam_name}"'
        if full_name:
            queries.append({
                "label": "Keluarga/Pasangan + Nama Target",
                "query": f'{name_q} {fam_q}',
                "risk": "critical",
                "description": f"Kombinasi nama target dan kerabat ({fam_name}) di internet",
            })
            queries.append({
                "label": "Doxing Pasangan / Kerabat",
                "query": f'{fam_q} ("{full_name}" OR doxing OR pinjol OR "suami" OR "istri")',
                "risk": "critical",
                "description": f"Jejak doxing atau asosiasi keluarga {fam_name}",
            })

    # Kueri Kata Kunci Spesifik (Tempat Kerja / Kampus)
    if additional_keywords.strip():
        kw = additional_keywords.strip()
        kw_q = f'"{kw}"' if " " in kw else kw
        if full_name:
            queries.append({
                "label": "Kata Kunci Tambahan + Nama",
                "query": f'{name_q} {kw_q}',
                "risk": "high",
                "description": f"Target dikaitkan dengan {kw}",
            })

    # ── Kueri berbasis Nomor HP ───────────────────────────
    if phone:
        queries.append({
            "label": "Kebocoran Nomor HP",
            "query": f'"{phone}"',
            "risk": "critical",
            "description": "Nomor HP yang terindeks di internet",
        })
        if full_name:
            queries.append({
                "label": "Nama + Nomor HP (Kombinasi)",
                "query": f'"{full_name}" "{phone}"',
                "risk": "critical",
                "description": "Kombinasi nama dan nomor yang muncul bersamaan di internet",
            })

    # ── Kueri berbasis Email ──────────────────────────────
    if email:
        queries.append({
            "label": "Kebocoran Alamat Email",
            "query": f'"{email}"',
            "risk": "high",
            "description": "Alamat email yang terindeks publik atau muncul di forum/database",
        })

    # ── Kueri per Platform Media Sosial ──────────────────
    social_inputs = [
        ("instagram", username_instagram),
        ("tiktok", username_tiktok),
        ("facebook", username_facebook),
        ("twitter", username_twitter),
        ("linkedin", username_linkedin),
        ("youtube", username_youtube),
        ("reddit", username_reddit),
        ("github", username_github),
    ]

    for platform_key, uname in social_inputs:
        if not uname.strip():
            continue
        uname = uname.strip().lstrip("@")  # Hapus @ jika ada
        meta = PLATFORM_META.get(platform_key, {})
        domain = meta.get("domain", f"{platform_key}.com")
        label_icon = meta.get("icon", "🔗")
        label_name = meta.get("label", platform_key.title())
        risk = meta.get("risk", "medium")

        # Kueri 1: site: operator - sangat presisi
        queries.append({
            "label": f"{label_icon} Profil {label_name}",
            "query": f'"{uname}" site:{domain.split(" OR")[0]}',
            "risk": risk,
            "description": f"Mencari profil @{uname} langsung di {label_name}",
            "platform": platform_key,
            "direct_url": meta.get("url_pattern", "").format(username=uname),
        })

        # Kueri 2: username + nama (jika ada nama)
        if full_name and platform_key in ("facebook", "linkedin", "instagram"):
            queries.append({
                "label": f"{label_icon} Nama + Username {label_name}",
                "query": f'"{full_name}" "{uname}" site:{domain.split(" OR")[0]}',
                "risk": risk,
                "description": f"Kombinasi nama asli dan username @{uname} di {label_name}",
                "platform": platform_key,
                "direct_url": "",
            })

    return queries


def search_google(query: str, api_key: str, cx: str, num_results: int = 5) -> Dict:
    """
    Jalankan satu kueri ke Google Custom Search JSON API.
    
    Returns:
        dict berisi 'items' (list hasil) atau 'error' (pesan error)
    """
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": cx,
        "q": query,
        "num": min(num_results, 10),
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            items = data.get("items", [])
            return {
                "success": True,
                "items": [
                    {
                        "title": item.get("title", ""),
                        "url": item.get("link", ""),
                        "snippet": item.get("snippet", ""),
                        "display_url": item.get("displayLink", ""),
                    }
                    for item in items
                ],
                "total_results": data.get("searchInformation", {}).get("totalResults", "0"),
            }
        elif response.status_code == 429:
            return {"success": False, "error": "Kuota API Google habis. Coba lagi besok.", "items": []}
        elif response.status_code == 403:
            return {"success": False, "error": "Google API 403: Pastikan 'Custom Search API' sudah di-ENABLE pada proyek Google Cloud Console Anda.", "items": []}
        else:
            return {"success": False, "error": f"Error HTTP {response.status_code}: {response.text[:200]}", "items": []}
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Koneksi timeout. Periksa koneksi internet.", "items": []}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Tidak dapat terhubung ke Google API.", "items": []}
    except Exception as e:
        return {"success": False, "error": f"Error tidak terduga: {str(e)}", "items": []}


def run_full_dork_scan(
    full_name: str = "",
    phone: str = "",
    email: str = "",
    spouse_family_name: str = "",
    additional_keywords: str = "",
    # Per-platform social media
    username_instagram: str = "",
    username_tiktok: str = "",
    username_facebook: str = "",
    username_twitter: str = "",
    username_linkedin: str = "",
    username_youtube: str = "",
    username_reddit: str = "",
    username_github: str = "",
    api_key: str = "",
    cx: str = "",
    delay: float = 0.5,
) -> List[Dict]:
    """
    Jalankan semua kueri dork dan kumpulkan hasilnya.
    """
    queries = build_dork_queries(
        full_name=full_name,
        phone=phone,
        email=email,
        spouse_family_name=spouse_family_name,
        additional_keywords=additional_keywords,
        username_instagram=username_instagram,
        username_tiktok=username_tiktok,
        username_facebook=username_facebook,
        username_twitter=username_twitter,
        username_linkedin=username_linkedin,
        username_youtube=username_youtube,
        username_reddit=username_reddit,
        username_github=username_github,
    )
    results = []

    for q in queries:
        if api_key and cx:
            result = search_google(q["query"], api_key, cx)
            time.sleep(delay)  # Hindari rate limiting
        else:
            # Mode demo tanpa API
            result = {
                "success": False,
                "error": "API Key belum dikonfigurasi",
                "items": [],
                "demo_mode": True,
            }

        results.append({
            "label": q["label"],
            "query": q["query"],
            "risk": q["risk"],
            "description": q["description"],
            "platform": q.get("platform", ""),
            "direct_url": q.get("direct_url", ""),
            "result": result,
            "found_count": len(result.get("items", [])),
        })

    return results


def get_mock_results(full_name: str) -> List[Dict]:
    """Data demo/mock untuk tampilan tanpa API."""
    return [
        {
            "label": "Informasi Umum",
            "query": f'"{full_name}"',
            "risk": "medium",
            "description": "Demo: Mencari semua referensi nama di internet",
            "result": {
                "success": True,
                "items": [
                    {
                        "title": f"{full_name} - LinkedIn Profile",
                        "url": "https://www.linkedin.com/in/contoh",
                        "snippet": f"Profil LinkedIn {full_name}, bekerja di PT Contoh...",
                        "display_url": "linkedin.com",
                    }
                ],
            },
            "found_count": 1,
        },
        {
            "label": "Dokumen Publik (PDF/DOC)",
            "query": f'"{full_name}" filetype:pdf',
            "risk": "high",
            "description": "Demo: Dokumen PDF yang mungkin bocor",
            "result": {"success": True, "items": []},
            "found_count": 0,
        },
        {
            "label": "Data KTP / NIK",
            "query": f'"{full_name}" KTP OR NIK',
            "risk": "critical",
            "description": "Demo: Data identitas publik",
            "result": {"success": True, "items": []},
            "found_count": 0,
        },
    ]
