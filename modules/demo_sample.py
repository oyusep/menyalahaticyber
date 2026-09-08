"""
Menyalahati Cyber Intelligence - Demo Sample Data
Data simulasi/contoh untuk demonstrasi tampilan diagnosa.
⚠️ DATA INI ADALAH SAMPEL DEMONSTRASI - BUKAN HASIL SCAN NYATA
"""
from typing import Dict, List


SAMPLE_TARGET = {
    "name": "Ika Lidya Sari Kismindar Ningrum",
    "phone": "+62 813-3817-6565",
    "email": "ikalidya.sari@gmail.com",
    "instagram": "ika.lidyasari",
    "facebook": "ika.lidyasari.kismindar",
    "tiktok": "ikalidya_official",
    "twitter": "",
    "linkedin": "",
}


def get_sample_dork_results() -> List[Dict]:
    """
    Simulasi hasil Google Dorking untuk target demo.
    Risk Score Critical >82% - banyak eksposur di sosmed & google.
    """
    name = SAMPLE_TARGET["name"]
    phone = SAMPLE_TARGET["phone"]

    return [
        # ── Nama (Informasi Umum) ─────────────────────────────
        {
            "label": "Informasi Umum",
            "query": f'"{name}"',
            "risk": "medium",
            "description": "Semua referensi nama di internet",
            "platform": "",
            "direct_url": "",
            "found_count": 7,
            "result": {
                "success": True,
                "items": [
                    {
                        "title": f"{name} | Facebook",
                        "url": "https://www.facebook.com/ika.lidyasari.kismindar",
                        "snippet": f"{name} ada di Facebook. Bergabunglah dengan Facebook untuk terhubung dengan {name} dan orang-orang lain yang mungkin kamu kenal...",
                        "display_url": "facebook.com",
                    },
                    {
                        "title": f"@ika.lidyasari · Instagram photos and videos",
                        "url": "https://www.instagram.com/ika.lidyasari/",
                        "snippet": f"3,847 Followers, 521 Following, 278 Posts - {name} (@ika.lidyasari) on Instagram. Surabaya 🌹 | Ibu Rumah Tangga...",
                        "display_url": "instagram.com",
                    },
                    {
                        "title": f"{name} - Profil & Informasi Kontak",
                        "url": "https://truecaller.com/search/id/0813-3817-6565",
                        "snippet": f"Nomor +62 813-3817-6565 terdaftar atas nama {name}. Lokasi: Surabaya, Jawa Timur. Operator: Telkomsel...",
                        "display_url": "truecaller.com",
                    },
                    {
                        "title": f"Ika Lidya Sari Kismindar Ningrum - TikTok",
                        "url": "https://www.tiktok.com/@ikalidya_official",
                        "snippet": f"ikalidya_official TikTok | {name}. 12.4K likes. Surabaya. Ibu 2 anak.",
                        "display_url": "tiktok.com",
                    },
                    {
                        "title": "Data Kependudukan - Surabaya",
                        "url": "https://data.surabaya.go.id/penduduk/detail",
                        "snippet": f"Nama: {name} | TTL: Surabaya, 14 Maret 1988 | Alamat: Jl. Ketintang Baru No. 47 RT.003/RW.002 Kel. Ketintang, Kec. Gayungan, Surabaya Selatan...",
                        "display_url": "data.surabaya.go.id",
                    },
                    {
                        "title": f"{name} | Tokopedia Seller",
                        "url": "https://www.tokopedia.com/ika-lidya-shop",
                        "snippet": f"Toko online {name}. Surabaya. Rating 4.8. 231 Produk. Bergabung sejak 2019...",
                        "display_url": "tokopedia.com",
                    },
                    {
                        "title": f"Testimoni & Review - {name}",
                        "url": "https://kaskus.co.id/thread/testimoni/ika-lidya",
                        "snippet": f"Kumpulan informasi tentang {name} dari berbagai pengguna Kaskus. Nomor WA: 0813-3817-6565...",
                        "display_url": "kaskus.co.id",
                    },
                ],
            },
        },
        # ── Dokumen Publik PDF/DOC ────────────────────────────
        {
            "label": "Dokumen Publik (PDF/DOC)",
            "query": f'"{name}" filetype:pdf OR filetype:doc',
            "risk": "high",
            "description": "Dokumen publik yang mungkin mengandung data pribadi",
            "platform": "",
            "direct_url": "",
            "found_count": 3,
            "result": {
                "success": True,
                "items": [
                    {
                        "title": f"Daftar Peserta BPJS Ketenagakerjaan 2022 - {name}",
                        "url": "https://drive.google.com/file/d/1xKm8TsampleBPJS/view",
                        "snippet": f"...Nama: {name} | NIK: 3578××××××××0003 | No. BPJS: 10012345678 | Perusahaan: CV Mitra Usaha Bersama...",
                        "display_url": "drive.google.com",
                    },
                    {
                        "title": f"Laporan Keuangan Koperasi RW 002 - Ketintang 2023",
                        "url": "https://docs.google.com/spreadsheets/d/kop-rw002-ketintang",
                        "snippet": f"...No. 14 | Ika Lidya Sari | +6281338176565 | Saldo: Rp 3.250.000 | Cicilan...",
                        "display_url": "docs.google.com",
                    },
                    {
                        "title": f"Sertifikat Pelatihan UMKM Surabaya - {name}",
                        "url": "https://disnakersurabaya.go.id/sertifikat/2022/pdf",
                        "snippet": f"Diberikan kepada: {name} | TTL: Surabaya, 14-03-1988 | Pelatihan: Digital Marketing UMKM | Tanggal: 22 Juli 2022...",
                        "display_url": "disnakersurabaya.go.id",
                    },
                ],
            },
        },
        # ── Data KTP / NIK / Identitas ─────────────────────────
        {
            "label": "Data KTP / NIK / Ijazah",
            "query": f'"{name}" KTP OR NIK OR "nomor identitas"',
            "risk": "critical",
            "description": "Dokumen identitas yang terindeks publik",
            "platform": "",
            "direct_url": "",
            "found_count": 4,
            "result": {
                "success": True,
                "items": [
                    {
                        "title": f"NIK Bocor - {name} | Pastebin",
                        "url": "https://pastebin.com/sample_ika_nik",
                        "snippet": f"DATA DUMP: {name} | NIK: 3578××××××××0003 | TTL: Surabaya 14/03/1988 | Ibu Kandung: Sri Wahyuni | Alamat: Jl. Ketintang Baru 47...",
                        "display_url": "pastebin.com",
                    },
                    {
                        "title": f"Foto KTP {name} - Grup Facebook Verifikasi Pinjol",
                        "url": "https://facebook.com/groups/pinjol.verifikasi/posts/sample123",
                        "snippet": f"KTP atas nama {name}, NIK: 3578××. Foto selfie dengan KTP terindeks di grup publik Facebook...",
                        "display_url": "facebook.com",
                    },
                    {
                        "title": f"Data KTP {name} - Doksing Telegram",
                        "url": "https://t.me/s/doxing_id_sample",
                        "snippet": f"[DOXED] {name} | +62813-3817-6565 | KTP Surabaya | Foto KTP + Selfie tersedia...",
                        "display_url": "t.me",
                    },
                    {
                        "title": f"Ijazah SMA {name} - Google Drive Shared",
                        "url": "https://drive.google.com/file/d/sampleijazah/view",
                        "snippet": f"Ijazah atas nama {name} | SMAN 5 Surabaya | Tahun Lulus 2006 | Nomor Ijazah: 06-DP-××-×...",
                        "display_url": "drive.google.com",
                    },
                ],
            },
        },
        # ── Alamat / Domisili ──────────────────────────────────
        {
            "label": "Informasi Alamat Tempat Tinggal",
            "query": f'"{name}" alamat OR "RT" OR "RW" OR kelurahan',
            "risk": "critical",
            "description": "Data lokasi tempat tinggal yang terekspos",
            "platform": "",
            "direct_url": "",
            "found_count": 5,
            "result": {
                "success": True,
                "items": [
                    {
                        "title": f"Direktori Warga - Ketintang Surabaya",
                        "url": "https://ketintang.surabaya.go.id/warga",
                        "snippet": f"{name} | Jl. Ketintang Baru No. 47 RT.003/RW.002 | Kel. Ketintang, Kec. Gayungan | Surabaya 60231",
                        "display_url": "ketintang.surabaya.go.id",
                    },
                    {
                        "title": f"Daftar Penerima BLT 2021 - Kelurahan Ketintang",
                        "url": "https://data.surabaya.go.id/blt-2021/ketintang",
                        "snippet": f"No.87 | {name} | HP: 081338176565 | RT003/RW002 | Layak Menerima BLT...",
                        "display_url": "data.surabaya.go.id",
                    },
                    {
                        "title": f"Foto Rumah {name} - Instagram",
                        "url": "https://www.instagram.com/p/sample_home_post/",
                        "snippet": f"Check-in dari Jl. Ketintang Baru 47, Surabaya. Tagged: {name}. Rumah baru kami ✨ #Surabaya #Ketintang",
                        "display_url": "instagram.com",
                    },
                    {
                        "title": f"Maps - Lokasi Usaha {name} | Google Maps",
                        "url": "https://maps.google.com/place/ika-lidya-shop",
                        "snippet": f"Ika Lidya Shop | Jl. Ketintang Baru No. 47, Surabaya | Pemilik: {name} | Tel: 0813-3817-6565",
                        "display_url": "maps.google.com",
                    },
                    {
                        "title": f"Grup WA - Tetangga RT 003 Ketintang (Bocor)",
                        "url": "https://chat.whatsapp.com/sample_leaked_group",
                        "snippet": f"Link grup WA RT.003 bocor ke publik. Anggota termasuk {name} (0813-3817-6565)...",
                        "display_url": "chat.whatsapp.com",
                    },
                ],
            },
        },
        # ── Instagram ─────────────────────────────────────────
        {
            "label": "📸 Instagram",
            "query": 'site:instagram.com "ika.lidyasari"',
            "risk": "medium",
            "description": "Profil dan aktivitas di Instagram",
            "platform": "instagram",
            "direct_url": "https://instagram.com/ika.lidyasari",
            "found_count": 8,
            "result": {
                "success": True,
                "items": [
                    {
                        "title": "@ika.lidyasari - Instagram",
                        "url": "https://www.instagram.com/ika.lidyasari/",
                        "snippet": "3,847 Followers. Profil publik. Foto wajah, alamat rumah, kegiatan sehari-hari, foto anak.",
                        "display_url": "instagram.com",
                    },
                    {
                        "title": "Ika Lidya Sari tagged photos",
                        "url": "https://www.instagram.com/explore/tags/ikalidya/",
                        "snippet": f"Tag #ikalidya #ikalidyasari: 127 posts. Foto ID Card, Foto KTP, selfie, lokasi check-in Surabaya.",
                        "display_url": "instagram.com",
                    },
                    {
                        "title": f"Story Highlight - {name}",
                        "url": "https://www.instagram.com/ika.lidyasari/highlights/",
                        "snippet": "Highlight story berisi foto keluarga, nomor rekening BCA, info belanja online, nomor HP.",
                        "display_url": "instagram.com",
                    },
                ],
            },
        },
        # ── Facebook ──────────────────────────────────────────
        {
            "label": "👤 Facebook",
            "query": 'site:facebook.com "Ika Lidya Sari Kismindar"',
            "risk": "high",
            "description": "Profil dan postingan publik di Facebook",
            "platform": "facebook",
            "direct_url": "https://facebook.com/ika.lidyasari.kismindar",
            "found_count": 11,
            "result": {
                "success": True,
                "items": [
                    {
                        "title": f"{name} | Facebook",
                        "url": "https://www.facebook.com/ika.lidyasari.kismindar",
                        "snippet": f"Profil publik. Surabaya, Jawa Timur. Bekerja di: CV Mitra Usaha. Sekolah: SMAN 5 Surabaya. Foto KTP dibagikan di postingan publik.",
                        "display_url": "facebook.com",
                    },
                    {
                        "title": f"{name} - Marketplace Facebook",
                        "url": "https://www.facebook.com/marketplace/profile/ika.lidyasari/",
                        "snippet": f"Penjual aktif. Lokasi: Surabaya Selatan. Kontak: 0813-3817-6565. Rating: 4.7/5.",
                        "display_url": "facebook.com",
                    },
                    {
                        "title": "Ika Lidya Sari - Grup Arisan Online",
                        "url": "https://www.facebook.com/groups/arisan.online.id/",
                        "snippet": f"Postingan dari {name}: Nomor rekening BCA 123-456-789 a.n. Ika Lidya Sari. WA: 0813-3817-6565.",
                        "display_url": "facebook.com",
                    },
                    {
                        "title": f"Doxing Thread - {name} di Facebook",
                        "url": "https://www.facebook.com/groups/doxid2024/posts/dox_ika_sample",
                        "snippet": f"⚠️ DATA DISEBARKAN: {name} | +62813-3817-6565 | KTP: foto tersedia | Alamat: Jl. Ketintang Baru 47 Surabaya...",
                        "display_url": "facebook.com",
                    },
                ],
            },
        },
        # ── Nomor HP ──────────────────────────────────────────
        {
            "label": "Nomor HP Terekspos",
            "query": f'"081338176565" OR "+6281338176565" OR "0813-3817-6565"',
            "risk": "high",
            "description": "Nomor HP yang terindeks di berbagai platform",
            "platform": "",
            "direct_url": "",
            "found_count": 6,
            "result": {
                "success": True,
                "items": [
                    {
                        "title": "Truecaller - +62 813-3817-6565",
                        "url": "https://truecaller.com/search/id/0813-3817-6565",
                        "snippet": f"Nama: {name} | Surabaya, JT | Operator: Telkomsel | Kategori: Pribadi | Terlapor: 0",
                        "display_url": "truecaller.com",
                    },
                    {
                        "title": "GetContact - 0813-3817-6565",
                        "url": "https://getcontact.com/id/62/0813-3817-6565",
                        "snippet": f"Nama disimpan pengguna lain: 'Ika Lidya Pinjol', 'Bu Ika Ketintang', 'Ika Arisan RT3'. Kontak tersimpan 47x.",
                        "display_url": "getcontact.com",
                    },
                    {
                        "title": f"WA Business - {name} Ika Lidya Shop",
                        "url": "https://wa.me/6281338176565",
                        "snippet": f"WhatsApp Business terdaftar: Ika Lidya Shop | Surabaya | Dibagikan di 23 forum publik.",
                        "display_url": "wa.me",
                    },
                    {
                        "title": f"Laporan Penipuan - 0813-3817-6565",
                        "url": "https://cekrekening.id/laporan/0813-3817-6565",
                        "snippet": f"Nomor ini pernah dilaporkan: 2 laporan penipuan arisan. Data pemilik: {name}.",
                        "display_url": "cekrekening.id",
                    },
                ],
            },
        },
        # ── Data Keuangan / Rekening ──────────────────────────
        {
            "label": "Data Rekening / Keuangan",
            "query": f'"{name}" rekening OR "no rek" OR BCA OR BRI OR Mandiri',
            "risk": "critical",
            "description": "Informasi rekening dan keuangan yang terekspos",
            "platform": "",
            "direct_url": "",
            "found_count": 4,
            "result": {
                "success": True,
                "items": [
                    {
                        "title": f"Nomor Rekening {name} - Facebook Marketplace",
                        "url": "https://facebook.com/marketplace/post/sample-ika",
                        "snippet": f"Transfer ke: BCA 3891-234-567 a.n. IKA LIDYA SARI. Hub: {phone}",
                        "display_url": "facebook.com",
                    },
                    {
                        "title": f"Grup Arisan Online - Data Anggota Bocor",
                        "url": "https://docs.google.com/spreadsheets/d/arisan-ketintang-rw02",
                        "snippet": f"Nama: {name} | Rekening BCA: 389-123-4567 | WA: 0813-3817-6565 | Cicilan: Rp 500.000/bulan",
                        "display_url": "docs.google.com",
                    },
                ],
            },
        },
    ]


def get_sample_breach_data() -> Dict:
    """Simulasi data breach HIBP untuk target demo."""
    return {
        "success": True,
        "demo_mode": True,
        "total_breaches": 5,
        "message": "⚠️ SAMPLE DATA - Simulasi kebocoran data untuk demonstrasi",
        "breaches": [
            {
                "name": "Tokopedia",
                "title": "Tokopedia",
                "domain": "tokopedia.com",
                "breach_date": "2020-05-02",
                "pwn_count": 91000000,
                "data_classes": ["Email addresses", "Passwords", "Phone numbers", "Physical addresses", "Dates of birth"],
                "description": "Tokopedia breach 2020: 91 juta data pengguna bocor termasuk email, password hash, nomor HP, dan alamat.",
                "is_sensitive": False,
                "is_verified": True,
            },
            {
                "name": "IndiHome",
                "title": "IndiHome / Telkom Indonesia",
                "domain": "indihome.co.id",
                "breach_date": "2023-08-18",
                "pwn_count": 24000000,
                "data_classes": ["Email addresses", "Physical addresses", "Phone numbers", "Geographic locations", "Usernames"],
                "description": "Data 24 juta pelanggan IndiHome bocor di forum hacker termasuk alamat lengkap dan nomor HP.",
                "is_sensitive": True,
                "is_verified": True,
            },
            {
                "name": "LinkedIn",
                "title": "LinkedIn",
                "domain": "linkedin.com",
                "breach_date": "2021-04-08",
                "pwn_count": 700000000,
                "data_classes": ["Email addresses", "Geographic locations", "Phone numbers", "Usernames"],
                "description": "Data scraping LinkedIn 2021: 700 juta profil termasuk nomor HP dan email.",
                "is_sensitive": False,
                "is_verified": True,
            },
            {
                "name": "BRI Life",
                "title": "BRI Life Asuransi",
                "domain": "brilife.co.id",
                "breach_date": "2021-07-16",
                "pwn_count": 2100000,
                "data_classes": ["Passwords", "Email addresses", "Physical addresses", "Dates of birth", "Bank account numbers"],
                "description": "Kebocoran data nasabah BRI Life: nama, NIK, nomor rekening, foto KTP bocor dijual di darkweb.",
                "is_sensitive": True,
                "is_verified": True,
            },
            {
                "name": "BPJS Kesehatan",
                "title": "BPJS Kesehatan",
                "domain": "bpjs-kesehatan.go.id",
                "breach_date": "2021-05-22",
                "pwn_count": 279000000,
                "data_classes": ["Email addresses", "Dates of birth", "Phone numbers", "Physical addresses", "Passwords"],
                "description": "279 juta data peserta BPJS bocor di RaidForum termasuk NIK, nama, alamat, dan nomor HP.",
                "is_sensitive": True,
                "is_verified": True,
            },
        ],
    }


def get_sample_risk_data() -> Dict:
    """
    Risk score simulasi: KRITIS - 87/100
    Mencerminkan eksposur masif di Google, Instagram, Facebook,
    kebocoran data breach ganda, dan doxing aktif.
    """
    return {
        "final_score": 87,
        "category": "KRITIS",
        "color": "red",
        "emoji": "🔴",
        "summary": (
            "Data pribadi target SANGAT RENTAN dan tersebar luas di internet. "
            "Ditemukan doxing aktif di Facebook dan Telegram, foto KTP bocor ke publik, "
            "alamat tempat tinggal terindeks, nomor rekening tersebar, serta 5 kebocoran data breach. "
            "Tindakan perlindungan SEGERA diperlukan!"
        ),
        "dork_score": 91,
        "breach_score": 78,
        "social_score": 85,
        "dork_findings": [
            "[CRITICAL] Data KTP / NIK / Ijazah: 4 temuan foto KTP & NIK terindeks publik",
            "[CRITICAL] Informasi Alamat Tempat Tinggal: 5 temuan alamat lengkap tersebar",
            "[CRITICAL] Data Rekening / Keuangan: Nomor rekening BCA bocor di 2 platform",
            "[HIGH] Dokumen Publik (PDF/DOC): 3 dokumen BPJS & ijazah terindeks Google",
            "[HIGH] 👤 Facebook: 11 temuan termasuk thread doxing aktif",
            "[HIGH] Nomor HP Terekspos: Nomor +62813-3817-6565 terindeks di 6 platform",
            "[MEDIUM] Informasi Umum: 7 referensi nama di internet",
            "[MEDIUM] 📸 Instagram: 8 temuan profil publik & foto pribadi",
        ],
        "breach_findings": [
            "Bocor di Tokopedia (2020): Email, Password, Phone numbers, Physical addresses, Dates of birth",
            "Bocor di IndiHome/Telkom (2023): Email, Alamat Lengkap, Phone numbers - DATA SENSITIF",
            "Bocor di LinkedIn (2021): Email, Phone numbers, Usernames",
            "Bocor di BRI Life (2021): Password, Rekening Bank, NIK, Alamat - DATA SANGAT SENSITIF",
            "Bocor di BPJS Kesehatan (2021): Email, NIK, Alamat, Phone - DATA SENSITIF",
        ],
        "social_findings": [
            "Profil ditemukan di instagram.com - Akun PUBLIK, 3.847 followers",
            "Profil ditemukan di facebook.com - Thread doxing aktif ditemukan",
            "Profil ditemukan di tiktok.com - Konten lokasi & keseharian",
            "Profil ditemukan di tokopedia.com - Data penjual terekspos",
        ],
        "all_findings": [
            "[CRITICAL] Data KTP / NIK / Ijazah: 4 temuan foto KTP & NIK terindeks publik",
            "[CRITICAL] Informasi Alamat Tempat Tinggal: 5 temuan alamat lengkap tersebar",
            "[CRITICAL] Data Rekening / Keuangan: Nomor rekening BCA bocor di 2 platform",
            "[HIGH] Dokumen Publik (PDF/DOC): 3 dokumen BPJS & ijazah terindeks Google",
            "[HIGH] 👤 Facebook: 11 temuan termasuk thread doxing aktif",
            "[HIGH] Nomor HP Terekspos: Nomor +62813-3817-6565 terindeks di 6 platform",
            "[MEDIUM] Informasi Umum: 7 referensi nama di internet",
            "[MEDIUM] 📸 Instagram: 8 temuan profil publik & foto pribadi",
            "Bocor di Tokopedia (2020): Email, Password, Phone numbers, Physical addresses, Dates of birth",
            "Bocor di IndiHome/Telkom (2023): Email, Alamat Lengkap, Phone numbers - DATA SENSITIF",
            "Bocor di LinkedIn (2021): Email, Phone numbers, Usernames",
            "Bocor di BRI Life (2021): Password, Rekening Bank, NIK, Alamat - DATA SANGAT SENSITIF",
            "Bocor di BPJS Kesehatan (2021): Email, NIK, Alamat, Phone - DATA SENSITIF",
            "Profil ditemukan di instagram.com - Akun PUBLIK, 3.847 followers",
            "Profil ditemukan di facebook.com - Thread doxing aktif ditemukan",
            "Profil ditemukan di tiktok.com - Konten lokasi & keseharian",
        ],
        "recommendations": [
            {
                "priority": "kritis",
                "icon": "🚨",
                "title": "Laporkan Doxing Aktif ke Platform & Polisi SEGERA",
                "detail": (
                    "Thread doxing ditemukan aktif di Facebook & Telegram. "
                    "Laporkan konten via fitur 'Report' di platform. "
                    "Buat laporan ke Bareskrim Polri (patrolisiber.id) dan BSSN (bssn.go.id). "
                    "Sertakan screenshot sebagai bukti digital. Ini tindak pidana UU ITE Pasal 27."
                ),
            },
            {
                "priority": "kritis",
                "icon": "🪪",
                "title": "Ajukan Takedown Foto KTP ke Google & Platform",
                "detail": (
                    "Foto KTP & NIK terindeks publik adalah pelanggaran UU PDP No.27/2022. "
                    "Ajukan penghapusan via Google Results About You (myactivity.google.com/remove-info). "
                    "Hubungi admin Pastebin, Telegram, dan Facebook untuk DCMA/Privacy takedown."
                ),
            },
            {
                "priority": "kritis",
                "icon": "🏦",
                "title": "Blokir & Ganti Nomor Rekening BCA",
                "detail": (
                    "Nomor rekening BCA 3891-234-567 telah tersebar di beberapa platform publik. "
                    "Hubungi Halo BCA di 1500888 untuk blokir dan pengajuan nomor rekening baru. "
                    "Pantau mutasi rekening secara berkala."
                ),
            },
            {
                "priority": "kritis",
                "icon": "🔐",
                "title": "Ganti Password & Aktifkan 2FA di Semua Akun",
                "detail": (
                    "5 data breach ditemukan. Password kemungkinan besar sudah bocor. "
                    "Ganti semua password sekarang, gunakan password unik per layanan. "
                    "Aktifkan 2FA menggunakan Google Authenticator atau Authy."
                ),
            },
            {
                "priority": "tinggi",
                "icon": "📵",
                "title": "Ganti Nomor HP atau Sembunyikan dari Publik",
                "detail": (
                    "Nomor +62 813-3817-6565 terindeks di Truecaller, GetContact, WA Business, dan forum publik. "
                    "Pertimbangkan ganti nomor atau gunakan nomor berbeda untuk kontak publik. "
                    "Hapus nomor dari profil sosmed publik."
                ),
            },
            {
                "priority": "tinggi",
                "icon": "🔒",
                "title": "Privatkan Semua Akun Media Sosial",
                "detail": (
                    "Instagram (@ika.lidyasari) masih akun publik dengan 3.847 followers. "
                    "Set ke Private segera. Hapus postingan yang mengandung alamat, nomor rekening, "
                    "atau foto dokumen dari Instagram, Facebook, dan TikTok."
                ),
            },
            {
                "priority": "tinggi",
                "icon": "🏛️",
                "title": "Laporkan ke OJK & Satgas PASTI",
                "detail": (
                    "Hubungi OJK di 157 atau Satgas PASTI di 0811-5050-100 (WhatsApp). "
                    "Buat laporan online di www.ojk.go.id jika terkait pinjol ilegal. "
                    "Simpan semua bukti doxing (screenshot dengan timestamp) sebelum melaporkan."
                ),
            },
            {
                "priority": "sedang",
                "icon": "🗑️",
                "title": "Audit & Hapus Dokumen dari Google Drive Publik",
                "detail": (
                    "Dokumen BPJS dan sertifikat ditemukan di Google Drive yang bisa diakses publik. "
                    "Masuk ke drive.google.com dan ubah izin berbagi menjadi 'Hanya Saya' atau "
                    "hapus file yang mengandung data pribadi sensitif."
                ),
            },
        ],
    }
