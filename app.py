"""
╔══════════════════════════════════════════════════════════╗
║       Menyalahati Cyber Intelligence                     ║
║       OSINT & DC Profiler - Anti Doxing System           ║
║       Versi 2.0 | Python + Streamlit                     ║
║       Untuk Korban Pinjaman Online Ilegal Indonesia      ║
╚══════════════════════════════════════════════════════════╝
"""

import streamlit as st
from datetime import datetime

# ─── Page Config (HARUS PERTAMA) ─────────────────────────
st.set_page_config(
    page_title="Menyalahati Cyber Intelligence - OSINT & Anti Doxing",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://www.ojk.go.id",
        "Report a bug": None,
        "About": "Menyalahati Cyber Intelligence v2.0 - Alat bantu korban pinjol ilegal",
    },
)

# ─── Import Modules ───────────────────────────────────────
from modules import settings as cfg
from modules import google_dorking as gdork
from modules import breach_audit as hibp
from modules import phone_profiler as phonep
from modules import risk_scorer as scorer
from modules import report_generator as rgen
from modules import ui_components as ui
from modules import demo_sample as demo
# ── Real Data Engine ───────────────────────────────
from modules import real_scraper as rsc
from modules import social_scanner as soc
from modules import phone_intel as pintel
from modules import removal_generator as rmv
from modules import ai_analyzer as ai_engine
# ── Database ────────────────────────────────────────
from modules import database as db


# ─── Inisialisasi Session State ───────────────────────────
def init_session_state():
    defaults = {
        "google_api_key": "",
        "google_cx": "",
        "hibp_api_key": "",
        "serp_api_key": "",
        "scan_results": None,
        "breach_results": None,
        "risk_data": None,
        "phone_profile": None,
        "last_scan_input": {},
        "scan_running": False,
        # ── Real Data Engine ──
        "social_data": None,
        "phone_intel_data": None,
        "scan_mode": "real",  # 'real' atau 'api'
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val
    cfg.load_keys_from_env()


# ─── SIDEBAR ────────────────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="padding: 16px 10px 12px; border-bottom: 1px solid #334155; margin-bottom: 16px;">
            <div style="display:flex; align-items:center; gap:10px; margin-bottom:8px;">
                <div style="
                    width:36px; height:36px;
                    background: #2563EB;
                    border-radius: 8px;
                    display:flex; align-items:center; justify-content:center;
                    font-size:1.1rem;
                    color: white;
                    flex-shrink:0;
                ">🔍</div>
                <div>
                    <div style="font-size:0.92rem; font-weight:800; color:#F8FAFC; line-height:1.2;">Menyalahati</div>
                    <div style="font-size:0.78rem; font-weight:600; color:#60A5FA;">Cyber Intelligence</div>
                </div>
            </div>
            <div style="font-size:0.68rem; color:#94A3B8; font-weight:500; text-transform:uppercase; letter-spacing:0.5px;">OSINT & Anti Doxing System</div>
        </div>
        """, unsafe_allow_html=True)

        # DB Stats di sidebar
        try:
            stats = db.get_dashboard_stats()
            st.markdown(f"""
            <div style="padding: 0 2px; margin-bottom: 12px;">
                <div style="font-size:0.68rem; color:#94A3B8; font-weight:600; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:8px;">Ringkasan Database</div>
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:6px;">
                    <div style="background:#1E293B; border:1px solid #334155; border-radius:6px; padding:8px; text-align:center;">
                        <div style="font-size:1.1rem; font-weight:800; color:#60A5FA;">{stats.get('total_scans', 0)}</div>
                        <div style="font-size:0.65rem; color:#94A3B8;">Diagnosa</div>
                    </div>
                    <div style="background:#1E293B; border:1px solid #334155; border-radius:6px; padding:8px; text-align:center;">
                        <div style="font-size:1.1rem; font-weight:800; color:#A78BFA;">{stats.get('total_dc', 0)}</div>
                        <div style="font-size:0.65rem; color:#94A3B8;">Investigasi DC</div>
                    </div>
                    <div style="background:#1E293B; border:1px solid #334155; border-radius:6px; padding:8px; text-align:center;">
                        <div style="font-size:1.1rem; font-weight:800; color:#F87171;">{stats.get('high_risk_count', 0)}</div>
                        <div style="font-size:0.65rem; color:#94A3B8;">Risiko Tinggi</div>
                    </div>
                    <div style="background:#1E293B; border:1px solid #334155; border-radius:6px; padding:8px; text-align:center;">
                        <div style="font-size:1.1rem; font-weight:800; color:#34D399;">{stats.get('total_reports', 0)}</div>
                        <div style="font-size:0.65rem; color:#94A3B8;">Laporan PDF</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        except Exception:
            pass

        # Admin Bertugas Section
        import modules.auth as auth
        curr_user = auth.get_current_user()
        if curr_user:
            st.markdown('<div style="font-size:0.68rem; color:#94A3B8; font-weight:600; text-transform:uppercase; letter-spacing:0.5px; padding:0 2px; margin-bottom:6px;">ADMIN BERTUGAS</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div style="background:#1E293B; border:1px solid #334155; border-radius:8px; padding:10px 12px; margin-bottom:10px;">
                <div style="font-weight:700; color:#F8FAFC; font-size:0.85rem;">👤 {curr_user.get('full_name')}</div>
                <div style="font-size:0.73rem; color:#94A3B8;">Role: <b style="color:#34D399;">{curr_user.get('role','operator').upper()}</b> | @{curr_user.get('username')}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🚪 Logout / Keluar", key="btn_logout_sb", use_container_width=True):
                auth.logout_user()

        st.markdown('<div style="border-top:1px solid #334155; margin:12px 0;"></div>', unsafe_allow_html=True)

        api_status = cfg.get_api_status()
        st.markdown('<div style="font-size:0.68rem; color:#94A3B8; font-weight:600; text-transform:uppercase; letter-spacing:0.5px; padding:0 2px; margin-bottom:8px;">STATUS KONFIGURASI API</div>', unsafe_allow_html=True)
        for name, is_active in api_status.items():
            dot = '<span style="display:inline-block;width:7px;height:7px;background:#34D399;border-radius:50%;margin-right:6px;"></span>' if is_active else '<span style="display:inline-block;width:7px;height:7px;background:#F87171;border-radius:50%;margin-right:6px;"></span>'
            label_color = "#34D399" if is_active else "#F87171"
            status_txt = "Aktif" if is_active else "Belum dikonfigurasi"
            st.markdown(f'<div style="font-size:0.78rem; color:{label_color}; padding:3px 2px; display:flex; align-items:center;">{dot}{name}: {status_txt}</div>', unsafe_allow_html=True)

        st.markdown('<div style="border-top:1px solid #334155; margin:12px 0;"></div>', unsafe_allow_html=True)

        st.markdown('<div style="font-size:0.68rem; color:#94A3B8; font-weight:600; text-transform:uppercase; letter-spacing:0.5px; padding:0 2px; margin-bottom:8px;">PANDUAN ALUR PROSES</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="font-size:0.78rem; color:#CBD5E1; padding:0 2px; line-height:1.7;">
            1. Daftarkan Klien di <b style="color:#60A5FA;">Data Klien</b><br>
            2. Jalankan scan di <b style="color:#60A5FA;">Diagnosa Jejak Digital</b><br>
            3. Buat Case & hapus di <b style="color:#60A5FA;">Asisten Removal</b><br>
            4. Buat Laporan di <b style="color:#60A5FA;">Investigasi DC</b>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div style="border-top:1px solid #334155; margin:16px 0 8px;"></div>', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:0.7rem; color:#64748B; text-align:center;">🕐 {datetime.now().strftime("%d/%m/%Y %H:%M")} WIB<br>v2.1 | Menyalahati Cyber Intelligence</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# TAB 1 - DASHBOARD
# ══════════════════════════════════════════════════════════
def render_tab_dashboard():
    ui.render_emergency_banner()
    ui.cyber_divider()

    # ── Dashboard stats dari DB ────────────────────────────
    try:
        stats = db.get_dashboard_stats()
    except Exception:
        stats = {}

    st.markdown("### 📊 Dashboard Ringkasan")

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        api_count = sum(1 for v in cfg.get_api_status().values() if v)
        st.metric("⚙️ API Aktif", f"{api_count}/3")
    with col2:
        st.metric("🔍 Total Diagnosa", stats.get('total_scans', 0))
    with col3:
        st.metric("📡 Investigasi DC", stats.get('total_dc', 0))
    with col4:
        avg = stats.get('avg_risk_score', 0)
        st.metric("🎯 Avg Risk Score", f"{avg}/100" if avg else "-")
    with col5:
        st.metric("📄 Laporan PDF", stats.get('total_reports', 0))

    ui.cyber_divider()

    # Recent Activity
    recent_scans = stats.get("recent_scans", [])
    recent_dc = stats.get("recent_dc", [])
    recent_cases = stats.get("recent_removal_cases", [])

    if recent_scans or recent_dc or recent_cases:
        col_ra, col_rb, col_rc = st.columns(3)
        with col_ra:
            st.markdown("#### 🕒 Diagnosa Terbaru")
            if recent_scans:
                for s in recent_scans:
                    score = s.get('risk_score', 0)
                    color = '#FF5252' if score >= 70 else ('#FFD740' if score >= 40 else '#00E676')
                    st.markdown(f"""
                    <div style="background:#070C1A; border:1px solid #0F1E3A; border-radius:8px; padding:10px 14px; margin:4px 0; display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <div style="color:#C0D8F0; font-weight:600; font-size:0.88rem;">{s.get('target_name','-')}</div>
                            <div style="color:#2A4060; font-size:0.72rem;">{s.get('created_at','')}</div>
                        </div>
                        <div style="font-size:0.88rem; font-weight:700; color:{color};">{score}/100</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.caption("Belum ada data")

        with col_rb:
            st.markdown("#### 🕒 Investigasi DC Terbaru")
            if recent_dc:
                for d in recent_dc:
                    spam = bool(d.get('is_spam', 0))
                    color = '#FF5252' if spam else '#00E676'
                    label = '🚨 SPAM' if spam else '✓ Normal'
                    st.markdown(f"""
                    <div style="background:#070C1A; border:1px solid #0F1E3A; border-radius:8px; padding:10px 14px; margin:4px 0; display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <div style="color:#C0D8F0; font-weight:600; font-size:0.88rem; font-family:'JetBrains Mono',monospace;">{d.get('dc_phone','-')}</div>
                            <div style="color:#2A4060; font-size:0.72rem;">{d.get('operator','-')} | {d.get('created_at','')}</div>
                        </div>
                        <div style="font-size:0.78rem; font-weight:700; color:{color};">{label}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.caption("Belum ada data")

        with col_rc:
            st.markdown("#### 🕒 Case Pembersihan Terbaru")
            if recent_cases:
                for rc in recent_cases:
                    c_status = rc.get('status', 'Draft')
                    c_code = rc.get('case_code', 'RMV-000')
                    color = '#00E676' if c_status == 'Berhasil Dihapus' else ('#FFD740' if c_status == 'Diajukan' else '#00D4FF')
                    st.markdown(f"""
                    <div style="background:#070C1A; border:1px solid #0F1E3A; border-radius:8px; padding:10px 14px; margin:4px 0; display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <div style="color:#00D4FF; font-weight:700; font-size:0.82rem; font-family:'JetBrains Mono',monospace;">{c_code}</div>
                            <div style="color:#C0D8F0; font-size:0.78rem;">{rc.get('client_name','-')}</div>
                        </div>
                        <div style="font-size:0.75rem; font-weight:700; color:{color};">{c_status} ({rc.get('progress_percent',0)}%)</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.caption("Belum ada case pembersihan")

    ui.cyber_divider()

    # Info cards
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#0A1428,#0F1629);
                    border:1px solid #1E2D50; border-top:3px solid #00D4FF;
                    border-radius:12px; padding:20px; height:180px;">
            <div style="font-size:1.5rem; margin-bottom:10px;">🔍</div>
            <div style="font-weight:700; color:#E0E6F0; margin-bottom:8px;">Diagnosa Jejak Digital</div>
            <div style="font-size:0.82rem; color:#6E7E9A; line-height:1.5;">
                Scan data Anda yang mungkin terindeks publik lewat Google Dorking otomatis,
                dan cek kebocoran email di database HIBP.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col_b:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#0A1428,#0F1629);
                    border:1px solid #1E2D50; border-top:3px solid #FFD740;
                    border-radius:12px; padding:20px; height:180px;">
            <div style="font-size:1.5rem; margin-bottom:10px;">📡</div>
            <div style="font-weight:700; color:#E0E6F0; margin-bottom:8px;">Investigasi Nomor DC</div>
            <div style="font-size:0.82rem; color:#6E7E9A; line-height:1.5;">
                Profil nomor HP pelaku: identifikasi operator telco, wilayah registrasi,
                dan tipe jaringan untuk keperluan penyidikan.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col_c:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#0A1428,#0F1629);
                    border:1px solid #1E2D50; border-top:3px solid #00E676;
                    border-radius:12px; padding:20px; height:180px;">
            <div style="font-size:1.5rem; margin-bottom:10px;">📄</div>
            <div style="font-weight:700; color:#E0E6F0; margin-bottom:8px;">Generator Laporan PDF</div>
            <div style="font-size:0.82rem; color:#6E7E9A; line-height:1.5;">
                Auto-generate laporan pengaduan siber resmi format PDF
                lengkap dengan profil nomor pelaku dan tabel CDR/BTS.
            </div>
        </div>
        """, unsafe_allow_html=True)

    ui.cyber_divider()

    # Pinjol ilegal info
    st.markdown("### ⚖️ Kenali Pinjol Ilegal")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **🚫 Ciri-ciri Pinjol ILEGAL:**
        - Tidak terdaftar/berizin OJK
        - Bunga & denda tidak transparan / sangat tinggi
        - Akses ke seluruh data kontak HP
        - Teror, ancaman, dan intimidasi ke keluarga/kontak
        - Proses cepat tanpa verifikasi ketat
        - Tidak ada kantor fisik yang jelas

        **📱 Cara Cek Legalitas Pinjol:**
        Kunjungi [ojk.go.id/id/kanal/iknb/financial-technology](https://ojk.go.id)
        atau hubungi OJK di **157**.
        """)
    with col2:
        st.markdown("""
        **✅ Pasal Hukum yang Melindungi Anda:**
        - **UU ITE Pasal 29** - Ancaman via elektronik = PIDANA
        - **UU PDP (No.27/2022)** - Data kontak diambil tanpa izin = PELANGGARAN
        - **POJK No.77/2016** - Pinjol wajib berizin OJK
        - **KUHP Pasal 368** - Pemerasan = PIDANA

        **🆘 Kontak Bantuan:**
        - OJK: **157** (Bebas pulsa, 24 jam)
        - Satgas PASTI: **0811-5050-100** (WhatsApp)
        - Bareskrim Polri: [patrolisiber.id](https://patrolisiber.id)
        - LBH Jakarta: 021-3145-518
        """)


# ══════════════════════════════════════════════════════════
# TAB KLIEN - MANAJEMEN DATA KLIEN INTERNAL
# ══════════════════════════════════════════════════════════
def render_tab_clients():
    st.markdown("### 👥 Manajemen Data Klien (Internal Tracking)")
    st.caption("Kelola profil Klien internal, catat identitas resmi, dan pantau seluruh timeline aktivitas Diagnosa, Pembersihan, dan Laporan Polisi.")

    ui.cyber_divider()

    # Cek & tampilkan notifikasi flash tersimpan
    if "client_created_success" in st.session_state:
        flash_msg = st.session_state.pop("client_created_success")
        st.success(flash_msg)
        st.toast("💾 Data Klien Tersimpan!", icon="👤")

    try:
        stats = db.get_dashboard_stats()
    except Exception:
        stats = {}

    ctab1, ctab2, ctab3 = st.tabs([
        f"📊 Daftar Klien ({stats.get('total_clients', 0)})",
        "➕ Registrasi Klien Baru",
        "🔍 Timeline Activity 360° per Klien",
    ])

    with ctab1:
        # Subtab Daftar Klien
        f_col1, f_col2 = st.columns([2, 3])
        with f_col1:
            status_filter = st.selectbox(
                "Filter Status Klien",
                ["Semua Status", "Aktif", "Dalam Pendampingan", "Selesai"],
                key="cli_filter_status"
            )
        with f_col2:
            search_query = st.text_input(
                "🔎 Cari Nama Klien / NIK / Phone / Email",
                placeholder="Ketik nama atau NIK Klien...",
                key="cli_search_query"
            )

        try:
            clients = db.get_clients(search_query=search_query, status_filter=status_filter)
        except Exception as e:
            clients = []
            st.error(f"Gagal memuat data klien: {e}")

        if not clients:
            st.markdown("""
            <div style="text-align:center; padding:50px 20px; background:#070C1A; border:1px solid #0F1E3A; border-radius:12px; margin-top:16px;">
                <div style="font-size:3rem; margin-bottom:12px;">👥</div>
                <div style="font-size:1rem; font-weight:700; color:#A0B8D0;">Belum Ada Data Klien Terdaftar</div>
                <div style="font-size:0.83rem; color:#5A7090; margin-top:6px;">
                    Tambahkan Klien baru melalui tab <b>'➕ Registrasi Klien Baru'</b>.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"##### 📋 Daftar Klien Internal ({len(clients)} data)")
            for cli in clients:
                c_id = cli["id"]
                c_code = cli.get("client_code", f"CLI-{c_id:03d}")
                c_name = cli.get("full_name", "")
                c_phone = cli.get("phone", "-")
                c_email = cli.get("email", "-")
                c_nik = cli.get("nik", "-")
                c_status = cli.get("status", "Aktif")
                c_scans = cli.get("scan_count", 0)
                c_removals = cli.get("removal_count", 0)
                c_reports = cli.get("report_count", 0)

                status_col = "#00E676" if c_status == "Selesai" else ("#FFD740" if c_status == "Dalam Pendampingan" else "#00D4FF")

                st.markdown(f"""
                <div style="background:#070C1A; border:1px solid #0F1E3A; border-left:4px solid {status_col}; border-radius:10px; padding:14px; margin:10px 0;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                        <div>
                            <span style="font-family:'JetBrains Mono',monospace; font-weight:700; color:#00D4FF; font-size:0.92rem;">{c_code}</span>
                            <span style="color:#E2E8F0; font-weight:700; font-size:0.95rem; margin-left:10px;">👤 {c_name}</span>
                            <span style="color:#5A7090; font-size:0.75rem; margin-left:10px;">NIK: {c_nik}</span>
                        </div>
                        <div>
                            <span style="background:{status_col}20; border:1px solid {status_col}; color:{status_col}; font-weight:700; padding:3px 10px; border-radius:12px; font-size:0.75rem;">
                                {c_status.upper()}
                            </span>
                        </div>
                    </div>
                    <div style="font-size:0.8rem; color:#A0B8D0; margin-bottom:6px;">
                        📱 HP: <b>{c_phone}</b> | ✉️ Email: <b>{c_email}</b>
                    </div>
                    <div style="font-size:0.75rem; color:#6A80A0; display:flex; gap:16px;">
                        <span>🔍 Scans: <b style="color:#00D4FF;">{c_scans}</b></span>
                        <span>📑 Removal Cases: <b style="color:#FFD740;">{c_removals}</b></span>
                        <span>📄 Laporan PDF: <b style="color:#7B61FF;">{c_reports}</b></span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                with st.expander(f"⚙️ Edit Data & Catatan Kasus ({c_code} - {c_name})"):
                    with st.form(f"form_edit_client_{c_id}"):
                        ce_name = st.text_input("Nama Lengkap Klien", value=c_name)
                        ce_col1, ce_col2 = st.columns(2)
                        with ce_col1:
                            ce_nik = st.text_input("NIK / KTP", value=cli.get("nik",""))
                            ce_phone = st.text_input("Nomor HP", value=cli.get("phone",""))
                        with ce_col2:
                            ce_email = st.text_input("Email", value=cli.get("email",""))
                            ce_status = st.selectbox("Status Pendampingan", ["Aktif", "Dalam Pendampingan", "Selesai"], index=["Aktif", "Dalam Pendampingan", "Selesai"].index(c_status) if c_status in ["Aktif", "Dalam Pendampingan", "Selesai"] else 0)

                        ce_address = st.text_area("Alamat Domisili", value=cli.get("address",""), height=60)
                        ce_contact = st.text_input("Kontak Darurat / Kerabat", value=cli.get("emergency_contact",""))
                        ce_notes = st.text_area("Catatan Kasus / Kronologi", value=cli.get("notes",""), height=70)

                        btn_update_cli = st.form_submit_button("💾 Update Data Klien", type="primary", use_container_width=True)
                        if btn_update_cli:
                            db.update_client(
                                client_id=c_id,
                                full_name=ce_name.strip(),
                                nik=ce_nik.strip(),
                                phone=ce_phone.strip(),
                                email=ce_email.strip(),
                                address=ce_address.strip(),
                                emergency_contact=ce_contact.strip(),
                                status=ce_status,
                                notes=ce_notes.strip()
                            )
                            msg = f"✅ Data Klien **{c_code}** ({ce_name}) berhasil diperbarui!"
                            st.session_state["client_created_success"] = msg
                            st.toast("💾 Data Klien Diperbarui!", icon="✅")
                            st.rerun()

                    if st.button("🗑️ Hapus Klien Ini", key=f"btn_del_cli_{c_id}", use_container_width=True):
                        db.delete_client(c_id)
                        msg = f"🗑️ Klien **{c_code}** berhasil dihapus."
                        st.session_state["client_created_success"] = msg
                        st.toast("🗑️ Klien Dihapus", icon="🗑️")
                        st.rerun()

    with ctab2:
        # Subtab Registrasi Klien Baru
        st.markdown("#### ➕ Registrasi Klien Internal Baru")
        st.caption("Daftarkan Klien baru untuk kemudahan tracking diagnosa, pembersihan index, dan laporan kepolisian.")

        with st.form("form_create_client"):
            cr_name = st.text_input("👤 Nama Lengkap Klien *", placeholder="Contoh: Yusep Maulana")
            cr_col1, cr_col2 = st.columns(2)
            with cr_col1:
                cr_nik = st.text_input("🆔 NIK / Nomor KTP", placeholder="16 digit NIK")
                cr_phone = st.text_input("📱 Nomor HP Klien", placeholder="081234567890")
            with cr_col2:
                cr_email = st.text_input("✉️ Alamat Email", placeholder="email@gmail.com")
                cr_status = st.selectbox("Status Pendampingan", ["Aktif", "Dalam Pendampingan", "Selesai"])

            cr_address = st.text_area("🏠 Alamat Domisili Klien", placeholder="Jl. Contoh No. 12, Kota...", height=65)
            cr_contact = st.text_input("👥 Nama & Kontak Kerabat / Pasangan", placeholder="Contoh: Istri - 081999888777")
            cr_notes = st.text_area("📋 Catatan Kasus / Kronologi Awal", placeholder="Ringkasan kasus teror DC / doxing yang dialami...", height=75)

            btn_save_client = st.form_submit_button("🚀 Simpan Data Klien Baru", type="primary", use_container_width=True)

            if btn_save_client:
                if not cr_name.strip():
                    st.error("❌ Nama Lengkap Klien wajib diisi!")
                else:
                    import modules.auth as auth
                    curr_user = auth.get_current_user() or {}
                    c_id, c_code = db.create_client(
                        full_name=cr_name.strip(),
                        nik=cr_nik.strip(),
                        phone=cr_phone.strip(),
                        email=cr_email.strip(),
                        address=cr_address.strip(),
                        emergency_contact=cr_contact.strip(),
                        status=cr_status,
                        notes=cr_notes.strip(),
                        created_by=curr_user.get("username", "admin")
                    )
                    msg = f"🎉 **BERHASIL DISIMPAN!** Klien **{c_code}** ({cr_name.strip()}) telah terdaftar di database."
                    st.session_state["client_created_success"] = msg
                    st.toast(f"💾 Klien {c_code} Terdaftar!", icon="👤")
                    st.rerun()

    with ctab3:
        # Subtab Timeline Activity 360°
        st.markdown("#### 🔍 Timeline Activity & Monitoring 360° per Klien")
        st.caption("Pilih Klien untuk melihat seluruh gabungan riwayat Diagnosa, Removal Case, dan Laporan Polisi.")

        all_cli = db.get_clients(limit=300)
        if not all_cli:
            st.info("Belum ada data Klien di database. Registrasikan Klien terlebih dahulu.")
        else:
            cli_options = [f"{c.get('client_code')} - {c.get('full_name')} ({c.get('phone','-')})" for c in all_cli]
            sel_cli_idx = st.selectbox("Pilih Klien Target", range(len(cli_options)), format_func=lambda x: cli_options[x], key="tl_cli_sel")
            selected_cli = all_cli[sel_cli_idx]

            # Banner Detail Klien
            st.markdown(f"""
            <div style="background:#080F1F; border:1px solid #1E2D50; border-radius:12px; padding:16px; margin:14px 0;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div style="font-size:1.1rem; font-weight:800; color:#00D4FF;">👤 {selected_cli.get('full_name')}</div>
                    <div style="font-family:'JetBrains Mono',monospace; color:#A0B8D0; font-size:0.88rem;">{selected_cli.get('client_code')}</div>
                </div>
                <div style="font-size:0.83rem; color:#A0B8D0; margin-top:8px;">
                    🆔 NIK: <b>{selected_cli.get('nik') or '-'}</b> | 📱 HP: <b>{selected_cli.get('phone') or '-'}</b> | ✉️ Email: <b>{selected_cli.get('email') or '-'}</b>
                </div>
                <div style="font-size:0.8rem; color:#64748B; margin-top:4px;">
                    🏠 Alamat: {selected_cli.get('address') or '-'} | 👥 Kerabat: {selected_cli.get('emergency_contact') or '-'}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Fetch Timeline
            timeline = db.get_client_timeline_360(
                client_name=selected_cli.get("full_name",""),
                client_phone=selected_cli.get("phone",""),
                client_email=selected_cli.get("email","")
            )

            if not timeline:
                st.info("Belum ada aktivitas (Diagnosa / Removal / Laporan) yang tercatat untuk Klien ini.")
            else:
                st.markdown(f"##### 📜 Timeline Activity 360° ({len(timeline)} Rekam Aktivitas)")
                for item in timeline:
                    st.markdown(f"""
                    <div style="background:#050914; border-left:4px solid {item['color']}; border-radius:8px; padding:12px 14px; margin:8px 0;">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <div style="font-weight:700; color:#E2E8F0; font-size:0.88rem;">
                                {item['icon']} {item['title']}
                            </div>
                            <div style="font-size:0.75rem; color:#64748B;">
                                ⏱️ {item['date']}
                            </div>
                        </div>
                        <div style="font-size:0.8rem; color:#A0B8D0; margin-top:4px;">
                            {item['desc']}
                        </div>
                        <div style="margin-top:6px;">
                            <span style="background:{item['color']}20; border:1px solid {item['color']}; color:{item['color']}; font-size:0.7rem; font-weight:700; padding:2px 8px; border-radius:10px;">
                                {item['badge']}
                            </span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# TAB 2 - DIAGNOSA KLIEN
# ══════════════════════════════════════════════════════════
def render_tab_diagnosa():
    st.markdown("### 🔍 Diagnosa Mandiri Jejak Digital")
    st.caption(
        "Masukkan data Anda untuk mendeteksi informasi pribadi yang mungkin terekspos di internet "
        "dan memeriksa kebocoran data akun Anda."
    )

    ui.cyber_divider()

    # ── Form Input ─────────────────────────────────────────
    with st.form("form_diagnosa", clear_on_submit=False):
        st.markdown("#### 📋 Data untuk Diagnosa")
        col1, col2 = st.columns(2)
        with col1:
            full_name = st.text_input(
                "👤 Nama Lengkap *",
                placeholder="Contoh: Budi Santoso",
                help="Nama yang ingin diperiksa jejak digitalnya",
            )
            phone = st.text_input(
                "📱 Nomor HP",
                placeholder="Contoh: 081234567890",
                help="Nomor HP yang ingin dicek apakah terindeks publik",
            )
        with col2:
            email = st.text_input(
                "📧 Alamat Email",
                placeholder="Contoh: budi@gmail.com",
                help="Email untuk dicek kebocoran data di HIBP",
            )

        # ── Data Hubungan / Anggota Keluarga (Penting untuk deteksi doxing DC) ──
        st.markdown("##### 👥 Informasi Keluarga / Kerabat (Penting untuk Deteksi Doxing DC Pinjol)")
        col_fam1, col_fam2 = st.columns(2)
        with col_fam1:
            spouse_family_name = st.text_input(
                "👩‍👩‍👦 Nama Istri / Suami / Pasangan / Orang Tua",
                placeholder="Contoh: Budi Santoso / Ahmad Fauzi",
                help="Nama kerabat yang sering dicari DC Pinjol untuk teror/doxing",
            )
        with col_fam2:
            additional_keywords = st.text_input(
                "🔑 Kata Kunci Tambahan / Tempat Kerja / Kampus",
                placeholder="Contoh: Universitas Indonesia, PT Maju Jaya",
                help="Kata kunci spesifik yang berpotensi muncul bersama nama Anda",
            )

        # ── Media Sosial (Per Platform) ──────────────────────
        st.markdown("##### 📱 Username Media Sosial (Opsional - isi yang relevan saja)")
        st.caption("Diisi untuk dork yang lebih presisi per platform. Tanpa '@'. Boleh tidak semua diisi.")

        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            username_instagram = st.text_input(
                "📸 Instagram",
                placeholder="Contoh: budi.santoso",
                help="Username Instagram tanpa @",
            )
            username_tiktok = st.text_input(
                "🎵 TikTok",
                placeholder="Contoh: budi_official",
                help="Username TikTok tanpa @",
            )
        with col_s2:
            username_facebook = st.text_input(
                "👤 Facebook",
                placeholder="Contoh: budi.santoso.123 atau link profil",
                help="Username/ID Facebook atau bagian terakhir dari URL profil",
            )
            username_twitter = st.text_input(
                "🐦 Twitter / X",
                placeholder="Contoh: budi_santoso",
                help="Username Twitter/X tanpa @",
            )
        with col_s3:
            username_linkedin = st.text_input(
                "💼 LinkedIn",
                placeholder="Contoh: budi-santoso-xyz",
                help="Username LinkedIn (bagian di linkedin.com/in/...)",
            )
            username_youtube = st.text_input(
                "▶️ YouTube",
                placeholder="Contoh: BudiChannel",
                help="Username YouTube tanpa @",
            )

        col_a, col_b = st.columns([3, 1])
        with col_b:
            submit_scan = st.form_submit_button(
                "🚀 Mulai Scan",
                use_container_width=True,
                type="primary",
            )

    # ── Proses Scan ────────────────────────────────────────
    if submit_scan:
        if not full_name.strip():
            st.error("❌ Nama Lengkap wajib diisi untuk memulai diagnosa.")
            return

        import time

        # ── Cek status Real Scraper Engine ─────────────────
        engine_status = rsc.get_engine_status()

        with st.spinner("🔄 Menginisialisasi mesin scan..."):
            progress = st.progress(0, text="🚀 Mempersiapkan Real Data Engine...")
            time.sleep(0.3)

        # ═══════════════════════════════════════════════════
        # TAHAP 1 - GOOGLE DORKING REAL
        # ═══════════════════════════════════════════════════
        progress.progress(5, text="🔍 Tahap 1/5 - Google Dorking Real (tanpa API)...")

        api_key = cfg.get_api_key("google_api_key")
        cx = cfg.get_api_key("google_cx")

        google_api_failed = False  # Flag jika Google API gagal

        if api_key and cx:
            # Mode API - coba Google Custom Search API dulu
            progress.progress(10, text="🔍 Mencoba Google Custom Search API...")
            dork_results = gdork.run_full_dork_scan(
                full_name=full_name, phone=phone, email=email,
                spouse_family_name=spouse_family_name,
                additional_keywords=additional_keywords,
                username_instagram=username_instagram,
                username_tiktok=username_tiktok,
                username_facebook=username_facebook,
                username_twitter=username_twitter,
                username_linkedin=username_linkedin,
                username_youtube=username_youtube,
                api_key=api_key, cx=cx,
            )

            # Cek apakah semua hasil gagal (403 / error)
            all_failed = all(
                not r.get("result", {}).get("success", True) and (
                    "403" in str(r.get("result", {}).get("error", "")) or
                    "429" in str(r.get("result", {}).get("error", "")) or
                    "quota" in str(r.get("result", {}).get("error", "")).lower() or
                    "enable" in str(r.get("result", {}).get("error", "")).lower()
                )
                for r in (dork_results or [{}])
            ) if dork_results else True

            if all_failed and engine_status.get("ready"):
                # Auto-fallback ke Real Scraper
                google_api_failed = True
                st.warning(
                    "⚠️ Google Custom Search API belum aktif atau kuota habis. "
                    "**Auto-fallback ke Real Scraper (DuckDuckGo + Bing)** - scan tetap berjalan!"
                )
                progress.progress(10, text="🔄 Fallback ke Real Scraper (DuckDuckGo + Bing + Yahoo)...")
                dork_results = rsc.run_real_dork_scan(
                    full_name=full_name,
                    phone=phone,
                    email=email,
                    spouse_family_name=spouse_family_name,
                    additional_keywords=additional_keywords,
                    max_queries=15,
                    num_results_per_query=5,
                )

        elif engine_status.get("ready"):
            # Mode Real Scraper - gratis (tanpa API key)
            progress.progress(10, text="🔍 Scraping Multi-Engine (DuckDuckGo + Bing + Yahoo)...")
            dork_results = rsc.run_real_dork_scan(
                full_name=full_name,
                phone=phone,
                email=email,
                spouse_family_name=spouse_family_name,
                additional_keywords=additional_keywords,
                max_queries=15,
                num_results_per_query=5,
            )
        else:
            # Fallback mode demo jika library belum terinstall
            progress.progress(10, text="⚠️ Mode terbatas - googlesearch-python belum terinstall")
            dork_results = gdork.get_mock_results(full_name)

        progress.progress(30, text="✅ Google Dorking selesai!")

        # ═══════════════════════════════════════════════════
        # TAHAP 2 - SOCIAL MEDIA SCANNER
        # ═══════════════════════════════════════════════════
        progress.progress(32, text="📱 Tahap 2/5 - Scanning Social Media Publik...")
        try:
            social_data = soc.scan_all_social_platforms(
                name=full_name,
                phone=phone,
                username_instagram=username_instagram,
                username_tiktok=username_tiktok,
                username_facebook=username_facebook or full_name,
                username_twitter=username_twitter,
            )
        except Exception as e:
            social_data = {"platforms": {}, "total_social_score": 0, "found_platforms": []}

        progress.progress(55, text="✅ Social Media scan selesai!")

        # ═══════════════════════════════════════════════════
        # TAHAP 3 - PHONE INTELLIGENCE
        # ═══════════════════════════════════════════════════
        phone_intel_data = None
        if phone.strip():
            progress.progress(57, text="📞 Tahap 3/5 - Phone Intelligence (Truecaller, GetContact)...")
            try:
                phone_intel_data = pintel.run_phone_intelligence(phone=phone, name=full_name)
            except Exception as e:
                phone_intel_data = None
            progress.progress(72, text="✅ Phone Intelligence selesai!")
        else:
            progress.progress(72, text="⏭️ Tahap 3/5 - Phone Intel dilewati (nomor tidak diisi)")

        # ═══════════════════════════════════════════════════
        # TAHAP 4 - BREACH AUDIT (HIBP)
        # ═══════════════════════════════════════════════════
        progress.progress(74, text="🔐 Tahap 4/5 - Memeriksa kebocoran data (HIBP)...")
        hibp_key = cfg.get_api_key("hibp_api_key")
        if email and hibp_key:
            breach_data = hibp.check_email_breaches(email, hibp_key)
            breaches = breach_data.get("breaches", [])
        elif email and not hibp_key:
            breach_data = hibp.get_mock_breaches(email)
            breaches = breach_data.get("breaches", [])
        else:
            breach_data = {"breaches": [], "message": "Email tidak diinput"}
            breaches = []
        progress.progress(88, text="✅ Breach audit selesai!")

        # ═══════════════════════════════════════════════════
        # TAHAP 5 - RISK SCORING 5 DIMENSI
        # ═══════════════════════════════════════════════════
        progress.progress(90, text="📊 Tahap 5/5 - Menghitung Risk Score 5 Dimensi...")
        risk_data = scorer.calculate_exposure_risk(
            dork_results=dork_results,
            breaches=breaches,
            social_data=social_data,
            phone_intel=phone_intel_data,
        )

        progress.progress(100, text="✅ Scan lengkap selesai!")
        time.sleep(0.5)
        progress.empty()

        # ── Simpan ke session state ─────────────────────────
        st.session_state.scan_results = dork_results
        st.session_state.breach_results = breach_data
        st.session_state.risk_data = risk_data
        st.session_state.social_data = social_data
        st.session_state.phone_intel_data = phone_intel_data
        st.session_state.last_scan_input = {
            "name": full_name, "phone": phone, "email": email,
            "instagram": username_instagram, "tiktok": username_tiktok,
            "facebook": username_facebook, "twitter": username_twitter,
            "linkedin": username_linkedin,
        }
        mode_used = "API" if (api_key and cx) else ("Real Scraper" if engine_status.get("ready") else "Demo")

        # ── AUTO-SAVE ke Database ────────────────────────────
        try:
            total_dork_found = sum(r.get("found_count", 0) for r in (dork_results or []))
            found_platforms = (social_data or {}).get("found_platforms", [])
            db.save_scan(
                target_name=full_name,
                target_phone=phone,
                target_email=email,
                risk_score=risk_data.get("final_score", 0),
                risk_category=risk_data.get("category", ""),
                risk_color=risk_data.get("color", ""),
                dork_found=total_dork_found,
                breach_count=len(breaches),
                social_platforms=found_platforms,
                scan_mode=mode_used,
                result_json={"risk": risk_data, "breach_count": len(breaches)},
                target_instagram=username_instagram,
                target_tiktok=username_tiktok,
                target_facebook=username_facebook,
                target_twitter=username_twitter,
                target_linkedin=username_linkedin,
                spouse_family=spouse_family_name,
                keywords=additional_keywords,
            )
        except Exception as _e:
            pass  # Jangan gagalkan scan hanya karena DB error

        st.success(f"✅ Scan selesai! Mode: **{mode_used}** | Sumber data: {len([x for x in [dork_results, social_data, phone_intel_data, breaches] if x])} aktif | 💾 Tersimpan ke riwayat")
        st.rerun()

    # ── Tampilkan Hasil ────────────────────────────────────
    if st.session_state.risk_data:
        risk = st.session_state.risk_data
        dork_res = st.session_state.scan_results or []
        breach_res = st.session_state.breach_results or {}
        breaches = breach_res.get("breaches", [])

        ui.cyber_divider()
        col_res_head, col_res_clear = st.columns([3, 1])
        with col_res_head:
            st.markdown("### 📊 Hasil Diagnosa")
        with col_res_clear:
            if st.button("🗑️ Bersihkan Hasil", use_container_width=True):
                st.session_state.scan_results = None
                st.session_state.breach_results = None
                st.session_state.risk_data = None
                st.session_state.last_scan_input = {}
                st.rerun()

        last_input = st.session_state.last_scan_input

        # Susun info platform yang diisi
        platform_icons = {
            "instagram": "📸 IG", "tiktok": "🎵 TikTok",
            "facebook": "👤 FB", "twitter": "🐦 X",
            "linkedin": "💼 LinkedIn",
        }
        filled_platforms = [
            icon for key, icon in platform_icons.items()
            if last_input.get(key, "").strip()
        ]
        platforms_str = " · ".join(filled_platforms) if filled_platforms else "-"

        st.caption(
            f"📍 Target: **{last_input.get('name','-')}** | "
            f"📱 HP: {last_input.get('phone','-') or '-'} | "
            f"📧 Email: {last_input.get('email','-') or '-'} | "
            f"Platform: {platforms_str}"
        )


        # Gauge + ringkasan
        col_gauge, col_summary = st.columns([1, 2])
        with col_gauge:
            ui.render_risk_gauge(
                risk["final_score"],
                risk["category"],
                risk["color"],
            )
        with col_summary:
            # Status badge
            color_map = {"green": "#00E676", "orange": "#FFD740", "red": "#FF5252"}
            c = color_map.get(risk["color"], "#69B4FF")

            # Badge sumber data real
            has_real = risk.get("has_real_data", False)
            real_badge = (
                '<span style="background:#00E67622; color:#00E676; border:1px solid #00E67644; '
                'border-radius:20px; padding:2px 10px; font-size:0.7rem; font-weight:600;">⚡ DATA REAL</span>'
                if has_real else
                '<span style="background:#FFD74022; color:#FFD740; border:1px solid #FFD74044; '
                'border-radius:20px; padding:2px 10px; font-size:0.7rem; font-weight:600;">🧪 SIMULASI</span>'
            )

            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#0A1428,#0F1629);
                        border:1px solid {c}40; border-left:4px solid {c};
                        border-radius:12px; padding:20px; margin-top:8px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                    <div style="font-size:1rem; font-weight:700; color:{c};">
                        {risk['emoji']} Status: {risk['category']} - {risk['final_score']}/100
                    </div>
                    {real_badge}
                </div>
                <div style="font-size:0.88rem; color:#C5D0E0; line-height:1.6;">
                    {risk['summary']}
                </div>
                <hr style="border-color:#1E2D50; margin:12px 0 10px;">
                <div style="display:grid; grid-template-columns:repeat(5,1fr); gap:8px; text-align:center;">
                    <div>
                        <div style="font-size:1.05rem; font-weight:700; color:#69B4FF;">{risk['dork_score']}</div>
                        <div style="font-size:0.65rem; color:#6E7E9A; margin-top:2px;">🔍 Dork<br/>(30%)</div>
                    </div>
                    <div>
                        <div style="font-size:1.05rem; font-weight:700; color:#FFD740;">{risk['social_score']}</div>
                        <div style="font-size:0.65rem; color:#6E7E9A; margin-top:2px;">📱 Social<br/>(25%)</div>
                    </div>
                    <div>
                        <div style="font-size:1.05rem; font-weight:700; color:#00E676;">{risk.get('phone_score', 0)}</div>
                        <div style="font-size:0.65rem; color:#6E7E9A; margin-top:2px;">📞 Phone<br/>(20%)</div>
                    </div>
                    <div>
                        <div style="font-size:1.05rem; font-weight:700; color:#FF8A80;">{risk['breach_score']}</div>
                        <div style="font-size:0.65rem; color:#6E7E9A; margin-top:2px;">🔓 Breach<br/>(15%)</div>
                    </div>
                    <div>
                        <div style="font-size:1.05rem; font-weight:700; color:#FF5252;">{risk.get('doxing_active_score', 0)}</div>
                        <div style="font-size:0.65rem; color:#6E7E9A; margin-top:2px;">☠️ Doxing<br/>(10%)</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ── AI Cyber Intelligence & Google Exposure Analyzer ──────────
        ai_res = ai_engine.analyze_doxing_reputation(
            full_name=full_name,
            phone=phone,
            spouse_family_name=spouse_family_name,
            additional_keywords=additional_keywords,
            dork_results=dork_res
        )

        st.markdown(f"""
        <div style="background:linear-gradient(135deg, #0F172A, #1E293B); border:1px solid #334155;
                    border-left:5px solid {ai_res['risk_color']}; border-radius:12px; padding:18px; margin-top:14px; margin-bottom:14px;">
            <div style="font-size:1.05rem; font-weight:700; color:{ai_res['risk_color']}; margin-bottom:8px;">
                {ai_res['doxing_risk_level']}
            </div>
            <div style="font-size:0.92rem; color:#E2E8F0; line-height:1.6;">
                {ai_res['ai_summary']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        if ai_res.get("google_live_queries"):
            st.markdown("##### 🚀 Akses Kueri Google Asli & Google AI Overview (1-Klik)")
            g_cols = st.columns(len(ai_res["google_live_queries"]))
            for idx, gq in enumerate(ai_res["google_live_queries"]):
                with g_cols[idx]:
                    st.markdown(f'<a href="{gq["url"]}" target="_blank" style="display:block; text-align:center; padding:10px; background:#1E40AF; color:#fff; font-weight:700; border-radius:8px; text-decoration:none; font-size:0.85rem;">{gq["label"]} &rarr;</a>', unsafe_allow_html=True)

        ui.cyber_divider()

        # ── Tabs Hasil ─────────────────────────────────────
        social_data_state = st.session_state.get("social_data") or {}
        phone_intel_state = st.session_state.get("phone_intel_data") or {}
        found_platforms = social_data_state.get("found_platforms", [])
        phone_findings = risk.get("phone_findings", [])

        tab_labels = [
            "🔍 Google Dork",
            f"💥 Breach ({len(breaches)})",
            "📱 Social Media",
            "📞 Phone Intel",
            "🛡️ Rekomendasi",
        ]
        res_tab1, res_tab2, res_tab3, res_tab4, res_tab5 = st.tabs(tab_labels)

        with res_tab1:
            if not dork_res:
                st.info("Belum ada hasil dork. Jalankan scan terlebih dahulu.")
            else:
                total_found = sum(r.get("found_count", 0) for r in dork_res)
                st.metric("Total Temuan Terindeks", total_found)
                for result in dork_res:
                    ui.render_dork_result_card(result)

                # ── Quick Action: Send to Removal Case ──
                all_found_items = []
                for r in dork_res:
                    for it in r.get("result", {}).get("items", []):
                        if it.get("url"):
                            all_found_items.append(it)

                if all_found_items:
                    st.markdown("<br>", unsafe_allow_html=True)
                    with st.expander("➕ **Kirim Temuan Ini ke Case Pembersihan Data (1-Klik)**"):
                        st.caption("Pilih salah satu temuan terindeks di atas untuk langsung diproses ke sistem Case Pembersihan & Monitoring Progress.")
                        sel_item_idx = st.selectbox(
                            "Pilih Link Temuan Target",
                            range(len(all_found_items)),
                            format_func=lambda x: f"[{all_found_items[x].get('display_url','url')}] {all_found_items[x].get('title','')[:60]}",
                            key="qc_sel_item"
                        )
                        target_it = all_found_items[sel_item_idx]
                        col_qc1, col_qc2 = st.columns(2)
                        with col_qc1:
                            qc_name = st.text_input("Nama Client / Target", value=full_name, key="qc_name_inp")
                            qc_url = st.text_input("URL Target", value=target_it.get("url",""), key="qc_url_inp")
                        with col_qc2:
                            qc_type = st.selectbox("Jenis Pengajuan", ["Google Outdated Content (Gagal Cache)", "Google Legal Formal (Privacy)", "DM Admin Medsos"], key="qc_type_inp")
                            qc_kw = st.text_input("Kata Kunci", value=f"BAYAR HUTANG {full_name}".strip(), key="qc_kw_inp")

                        if st.button("🚀 Buat Case Pembersihan Sekarang", key="btn_qc_create", type="primary", use_container_width=True):
                            new_id, new_code = db.create_removal_case(
                                client_name=qc_name or full_name,
                                client_phone=phone,
                                target_url=qc_url,
                                target_snippet=target_it.get("snippet",""),
                                target_keyword=qc_kw,
                                removal_type=qc_type,
                                status="Draft",
                                progress_percent=10
                            )
                            success_msg = f"🎉 **BERHASIL DISIMPAN!** Case Pembersihan **{new_code}** berhasil dibuat & tersimpan ke sistem. Buka **Tab Asisten Removal** untuk melihat progress."
                            st.session_state["rmv_case_created_success"] = success_msg
                            st.toast(f"💾 Case {new_code} Berhasil Disimpan!", icon="✅")
                            st.rerun()

        with res_tab2:
            if breach_res.get("demo_mode"):
                st.warning("⚠️ **Data Demo** - Masukkan HIBP API Key di Pengaturan untuk hasil nyata.")
            if not breaches:
                msg = breach_res.get("message", "")
                if msg:
                    st.success(f"✅ {msg}")
                else:
                    st.info("Tidak ada kebocoran data ditemukan.")
            else:
                st.error(f"⚠️ Ditemukan **{len(breaches)} kebocoran data** untuk email ini!")
                for b in breaches:
                    ui.render_breach_card(b)

        with res_tab3:
            # ── Social Media Results ──────────────────────────
            if not social_data_state:
                st.info("Data social media belum tersedia. Jalankan scan dengan memasukkan username sosmed.")
            else:
                platforms = social_data_state.get("platforms", {})
                total_score = social_data_state.get("total_social_score", 0)
                found = social_data_state.get("found_platforms", [])

                st.metric("Social Exposure Score", f"{total_score}/100",
                          delta=f"{len(found)} platform ditemukan",
                          delta_color="inverse")

                if not platforms:
                    st.info("Tidak ada data platform sosmed. Isi username sosmed di form scan.")
                else:
                    for platform_name, pdata in platforms.items():
                        icon_map = {
                            "instagram": "📸", "facebook": "👤", "tiktok": "🎵",
                            "twitter": "🐦", "whatsapp": "📱", "cekrekening": "⚠️"
                        }
                        icon = icon_map.get(platform_name, "🌐")
                        score = pdata.get("exposure_score", 0)
                        color = "#FF5252" if score > 60 else "#FFD740" if score > 30 else "#00E676"

                        with st.expander(
                            f"{icon} **{platform_name.upper()}** - Exposure Score: {score}/100",
                            expanded=(score > 50)
                        ):
                            col_a, col_b = st.columns([2, 1])
                            with col_a:
                                if pdata.get("url"):
                                    st.markdown(f"🔗 [Buka Profil]({pdata['url']})")
                                if pdata.get("full_name"):
                                    st.markdown(f"👤 **Nama:** {pdata['full_name']}")
                                if pdata.get("followers", 0) > 0:
                                    st.markdown(f"👥 **Followers:** {pdata['followers']:,}")
                                if pdata.get("bio"):
                                    st.markdown(f"📝 **Bio:** {pdata['bio'][:200]}")
                                if pdata.get("is_public") is not None:
                                    pub_status = "🔓 PUBLIK" if pdata["is_public"] else "🔒 Privat"
                                    st.markdown(f"**Status:** {pub_status}")
                                if pdata.get("has_report"):
                                    st.error(f"🚨 {pdata.get('report_count', 1)} laporan penipuan ditemukan!")
                                for detail in (pdata.get("exposure_details") or pdata.get("details") or []):
                                    st.markdown(f"• {detail}")
                            with col_b:
                                st.markdown(
                                    f'<div style="text-align:center; padding:16px;'
                                    f'background:linear-gradient(135deg,#0A1428,#0F1629);'
                                    f'border:1px solid {color}40; border-radius:12px;">'
                                    f'<div style="font-size:2rem; font-weight:800; color:{color};">{score}</div>'
                                    f'<div style="font-size:0.7rem; color:#6E7E9A;">/ 100</div>'
                                    f'<div style="font-size:0.65rem; color:{color}; margin-top:4px;">Exposure</div>'
                                    f'</div>',
                                    unsafe_allow_html=True
                                )

                if risk.get("social_findings"):
                    st.markdown("---")
                    st.markdown("**📋 Temuan Social Media:**")
                    for f in risk["social_findings"]:
                        st.markdown(f"• {f}")

        with res_tab4:
            # ── Phone Intelligence Results ────────────────────
            if not phone_intel_state:
                st.info("Data Phone Intelligence belum tersedia. Isi nomor HP di form scan.")
            else:
                phone_norm = phone_intel_state.get("phone_normalized", {})
                total_phone = phone_intel_state.get("total_phone_score", 0)
                indicators = phone_intel_state.get("risk_indicators", [])

                col_ps, col_pi = st.columns([1, 2])
                with col_ps:
                    phone_color = "#FF5252" if total_phone > 60 else "#FFD740" if total_phone > 30 else "#00E676"
                    st.markdown(
                        f'<div style="text-align:center; padding:20px;'
                        f'background:linear-gradient(135deg,#0A1428,#0F1629);'
                        f'border:2px solid {phone_color}40; border-radius:12px; margin-bottom:8px;">'
                        f'<div style="font-size:0.75rem; color:#6E7E9A; margin-bottom:4px;">PHONE EXPOSURE SCORE</div>'
                        f'<div style="font-size:3rem; font-weight:800; color:{phone_color};">{total_phone}</div>'
                        f'<div style="font-size:0.7rem; color:#6E7E9A;">/ 100</div>'
                        f'</div>',
                        unsafe_allow_html=True
                    )
                    if phone_norm:
                        st.caption(f"Format E.164: `{phone_norm.get('e164', '-')}`")
                        st.caption(f"Format Lokal: `{phone_norm.get('local', '-')}`")

                with col_pi:
                    if indicators:
                        st.markdown("**🚨 Risk Indicators:**")
                        for ind in indicators:
                            st.markdown(f"• {ind}")
                    else:
                        st.success("✅ Tidak ada indikator risiko kritis dari nomor HP ini")

                st.markdown("---")

                # Detail per sumber
                sources = {
                    "Truecaller": phone_intel_state.get("truecaller", {}),
                    "GetContact": phone_intel_state.get("getcontact", {}),
                    "Google Mentions": phone_intel_state.get("google_mentions", {}),
                    "Laporan Penipuan": phone_intel_state.get("fraud_reports", {}),
                }
                for src_name, src_data in sources.items():
                    if not src_data:
                        continue
                    src_score = src_data.get("exposure_score", 0)
                    with st.expander(f"📊 **{src_name}** - Score: {src_score}/100"):
                        for det in src_data.get("details", []):
                            st.markdown(f"• {det}")
                        if src_data.get("url"):
                            st.markdown(f"🔗 [Buka halaman]({src_data['url']})")
                        if src_data.get("saved_names"):
                            st.markdown(f"**Nama yang tersimpan:** {', '.join(src_data['saved_names'][:5])}")
                        if src_data.get("urls_found"):
                            st.markdown(f"**URL ditemukan:** {src_data.get('total_mentions', 0)}")

                if risk.get("phone_findings"):
                    st.markdown("---")
                    st.markdown("**📋 Temuan Phone Intelligence:**")
                    for f in risk["phone_findings"]:
                        st.markdown(f"• {f}")

        with res_tab5:
            recs = risk.get("recommendations", [])
            if not recs:
                st.info("Tidak ada rekomendasi khusus saat ini.")
            else:
                st.markdown(f"**{len(recs)} rekomendasi mitigasi berdasarkan hasil scan 5 dimensi:**")
                for rec in recs:
                    ui.render_recommendation_card(rec)


# ══════════════════════════════════════════════════════════
# TAB 3 - ASISTEN REMOVAL GOOGLE & MEDSOS
# ══════════════════════════════════════════════════════════
def render_tab_removal_assistant():
    st.markdown("### 📑 Asisten Pembersihan Data & Case Removal Monitoring")
    st.caption(
        "Kelola seluruh proses pengajuan pembersihan index Google dan media sosial untuk korban doxing / teror pinjol. "
        "Pantau progress penanganan secara real-time dari status Draft hingga Berhasil Dihapus (De-indexed)."
    )

    ui.cyber_divider()

    # ── Notifikasi Flash Tersimpan (Persistence across st.rerun) ──
    if "rmv_case_created_success" in st.session_state:
        flash_msg = st.session_state.pop("rmv_case_created_success")
        st.success(flash_msg)
        st.toast("💾 Data Tersimpan ke Database!", icon="✅")

    # Ambil data stats
    try:
        stats = db.get_dashboard_stats()
    except Exception:
        stats = {}

    # Auto-load data dari session state jika ada
    last_input = st.session_state.get("last_scan_input", {})
    last_name = last_input.get("name", "")
    last_phone = last_input.get("phone", "")
    last_email = last_input.get("email", "")

    dork_results = st.session_state.get("scan_results") or []
    dox_items = []
    for r in dork_results:
        for item in r.get("result", {}).get("items", []):
            if item.get("url"):
                dox_items.append(item)

    # ── Sub-tabs Asisten Removal ──────────────────────────────────────────
    tab_rmv1, tab_rmv2, tab_rmv3, tab_rmv4 = st.tabs([
        f"📊 Dashboard & Monitoring Case ({stats.get('total_removal_cases', 0)})",
        "➕ Buat Case Pembersihan Baru",
        "🤖 AI Legal Generator & Panduan",
        "🔍 Live Status Checker (Google)",
    ])

    # ══════════════════════════════════════════════════════════════════════
    # SUBTAB 1 - DASHBOARD & MONITORING CASE
    # ══════════════════════════════════════════════════════════════════════
    with tab_rmv1:
        # Mini metrics
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f"""<div class="stat-mini"><div class="val">{stats.get('total_removal_cases', 0)}</div><div class="lbl">Total Case Pembersihan</div></div>""", unsafe_allow_html=True)
        with m2:
            st.markdown(f"""<div class="stat-mini"><div class="val" style="color:#FFD740">{stats.get('active_cases', 0)}</div><div class="lbl">Sedang Diproses / Dalam Peninjauan</div></div>""", unsafe_allow_html=True)
        with m3:
            st.markdown(f"""<div class="stat-mini"><div class="val" style="color:#00E676">{stats.get('completed_cases', 0)}</div><div class="lbl">Berhasil Dihapus (De-indexed)</div></div>""", unsafe_allow_html=True)
        with m4:
            st.markdown(f"""<div class="stat-mini"><div class="val" style="color:#00D4FF">UU PDP & ITE</div><div class="lbl">Landasan Hukum Hak Privasi</div></div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Filter & Search Controls
        f_col1, f_col2 = st.columns([2, 3])
        with f_col1:
            status_filter = st.selectbox(
                "Filter Status Penanganan",
                ["Semua Status", "Draft", "Diajukan", "Dalam Peninjauan", "Berhasil Dihapus", "Ditolak"],
                key="rmv_filter_status"
            )
        with f_col2:
            search_query = st.text_input(
                "🔎 Cari Kode Case / Nama Client / URL",
                placeholder="Ketik kode (misal RMV-20260906-001) atau nama...",
                key="rmv_search_query"
            )

        # Ambil daftar cases dari DB
        try:
            cases = db.get_removal_cases(status_filter=status_filter, search_query=search_query)
        except Exception as e:
            cases = []
            st.error(f"Gagal memuat data case: {e}")

        if not cases:
            st.markdown("""
            <div style="text-align:center; padding:50px 20px; background:#070C1A; border:1px solid #0F1E3A; border-radius:12px; margin-top:16px;">
                <div style="font-size:3rem; margin-bottom:12px;">📑</div>
                <div style="font-size:1rem; font-weight:700; color:#A0B8D0;">Belum Ada Case Pembersihan Data</div>
                <div style="font-size:0.83rem; color:#5A7090; margin-top:6px;">
                    Buat case pembersihan baru melalui tab <b>'➕ Buat Case Pembersihan Baru'</b> atau impor dari hasil Diagnosa.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"##### 📋 Daftar Case Aktif ({len(cases)} data)")
            for c_item in cases:
                c_id = c_item["id"]
                c_code = c_item.get("case_code", f"RMV-{c_id:03d}")
                c_status = c_item.get("status", "Draft")
                c_prog = c_item.get("progress_percent", 10)
                c_name = c_item.get("client_name", "Tanpa Nama")
                c_url = c_item.get("target_url", "")
                c_platform = c_item.get("platform", "Google")
                c_type = c_item.get("removal_type", "Google Outdated Content")
                c_date = c_item.get("created_at", "")
                c_http = c_item.get("http_status_code")
                c_indexed = c_item.get("is_indexed")

                # Color badges
                status_colors = {
                    "Draft": "#00D4FF",
                    "Diajukan": "#FFD740",
                    "Dalam Peninjauan": "#7B61FF",
                    "Berhasil Dihapus": "#00E676",
                    "Ditolak": "#FF5252",
                }
                badge_col = status_colors.get(c_status, "#00D4FF")

                # Live HTTP badge
                if c_http == 200:
                    live_badge = "🔴 HTTP 200 - Halaman Masih Tayang"
                elif c_http in (404, 410):
                    live_badge = "🟢 HTTP 404/410 - TERHAPUS Dari Web Sumber"
                elif c_http:
                    live_badge = f"🟡 HTTP {c_http}"
                else:
                    live_badge = "⚪ Live Check Belum Dijalankan"

                st.markdown(f"""
                <div style="background:#070C1A; border:1px solid #0F1E3A; border-left:4px solid {badge_col}; border-radius:10px; padding:14px; margin:10px 0;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                        <div>
                            <span style="font-family:'JetBrains Mono',monospace; font-weight:700; color:#00D4FF; font-size:0.92rem;">{c_code}</span>
                            <span style="color:#E2E8F0; font-weight:600; margin-left:10px; font-size:0.9rem;">👤 {c_name}</span>
                            <span style="color:#5A7090; font-size:0.75rem; margin-left:10px;">📅 {c_date}</span>
                        </div>
                        <div>
                            <span style="background:{badge_col}20; border:1px solid {badge_col}; color:{badge_col}; font-weight:700; padding:3px 10px; border-radius:12px; font-size:0.75rem;">
                                {c_status.upper()} ({c_prog}%)
                            </span>
                        </div>
                    </div>
                    <div style="font-size:0.8rem; color:#A0B8D0; margin-bottom:6px; word-break:break-all;">
                        🔗 <b>URL Target:</b> <a href="{c_url}" target="_blank" style="color:#69B4FF; text-decoration:none;">{c_url}</a>
                    </div>
                    <div style="font-size:0.75rem; color:#6A80A0; display:flex; gap:16px;">
                        <span>📌 Jenis: <b>{c_type}</b></span>
                        <span>🌐 Platform: <b>{c_platform or 'Google Search'}</b></span>
                        <span>🔍 Live Check: <b>{live_badge}</b></span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Progress bar
                st.progress(c_prog / 100, text=f"Progress Penanganan: {c_prog}%")

                # Expander Detail & Update Status
                with st.expander(f"⚙️ Kelola Progress, Update Status & Log Penanganan ({c_code})"):
                    col_u1, col_u2 = st.columns([3, 2])
                    with col_u1:
                        st.markdown("##### 🔄 Update Status Penanganan")
                        new_status = st.selectbox(
                            "Status Baru",
                            ["Draft", "Diajukan", "Dalam Peninjauan", "Berhasil Dihapus", "Ditolak"],
                            index=["Draft", "Diajukan", "Dalam Peninjauan", "Berhasil Dihapus", "Ditolak"].index(c_status) if c_status in ["Draft", "Diajukan", "Dalam Peninjauan", "Berhasil Dihapus", "Ditolak"] else 0,
                            key=f"status_sel_{c_id}"
                        )
                        new_prog = st.slider(
                            "Persentase Progress (%)",
                            min_value=0, max_value=100, value=c_prog, step=5,
                            key=f"prog_sl_{c_id}"
                        )
                        update_notes = st.text_area(
                            "Catatan Progress / Alasan Perubahan Status",
                            placeholder="Contoh: Form Google Legal berhasil dikirim dengan no referensi 98213...",
                            key=f"notes_ta_{c_id}",
                            height=70
                        )

                        btn_save_status = st.button("💾 Simpan Perubahan Status", key=f"btn_update_{c_id}", type="primary", use_container_width=True)
                        if btn_save_status:
                            success = db.update_removal_case_status(
                                case_id=c_id,
                                new_status=new_status,
                                progress_percent=new_prog,
                                notes=update_notes,
                                actor="Operator"
                            )
                            if success:
                                msg = f"✅ Status case **{c_code}** berhasil diperbarui ke **'{new_status}'** ({new_prog}%)!"
                                st.session_state["rmv_case_created_success"] = msg
                                st.toast(f"💾 Case {c_code} Diperbarui ke {new_status}", icon="✅")
                                st.rerun()

                    with col_u2:
                        st.markdown("##### 🔍 Live Indexing Check")
                        st.caption("Uji secara langsung apakah URL target masih memberikan respon HTTP 200 atau sudah terhapus (HTTP 404).")
                        btn_live_chk = st.button("🔍 Cek Indexing Google Sekarang", key=f"btn_chk_{c_id}", use_container_width=True)
                        if btn_live_chk:
                            with st.spinner("Menguji koneksi ke URL target..."):
                                chk_res = rmv.check_url_indexing_status(c_url)
                                db.update_case_live_check(
                                    case_id=c_id,
                                    http_code=chk_res.get("status_code", 0),
                                    is_indexed=chk_res.get("is_live", True),
                                    actor="AI Live Checker"
                                )
                                msg = f"🔍 Live Check Result: {chk_res.get('message')}"
                                st.session_state["rmv_case_created_success"] = msg
                                st.toast("🔍 Live Check Selesai!", icon="🌐")
                                st.rerun()

                        st.markdown("---")
                        st.markdown("##### 🗑️ Hapus Case")
                        if st.button("🗑️ Hapus Case Pembersihan Ini", key=f"btn_del_case_{c_id}", use_container_width=True):
                            db.delete_removal_case(c_id)
                            msg = f"🗑️ Case **{c_code}** berhasil dihapus dari database."
                            st.session_state["rmv_case_created_success"] = msg
                            st.toast(f"🗑️ Case {c_code} Dihapus", icon="🗑️")
                            st.rerun()

                    # Log Timeline Table
                    st.markdown("##### 📜 Riwayat Timeline Penanganan & Progress Log")
                    case_detail = db.get_removal_case_detail(c_id)
                    c_logs = case_detail.get("logs", [])
                    if c_logs:
                        for lg in c_logs:
                            st.markdown(f"""
                            <div style="background:#040711; border-left:3px solid #00D4FF; padding:8px 12px; margin:4px 0; font-size:0.8rem; border-radius:4px;">
                                <div style="color:#00D4FF; font-weight:600;">⏱️ {lg.get('created_at')} - {lg.get('action_type')} <span style="color:#5A7090;">({lg.get('actor')})</span></div>
                                <div style="color:#C0D8F0; margin-top:2px;">{lg.get('description')}</div>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.caption("Belum ada log riwayat.")

    # ══════════════════════════════════════════════════════════════════════
    # SUBTAB 2 - BUAT CASE PEMBERSIHAN BARU
    # ══════════════════════════════════════════════════════════════════════
    with tab_rmv2:
        st.markdown("#### ➕ Buat Case Pembersihan Data & Tracking Baru")
        st.caption("Impor hasil dorking dari Diagnosa sebelumnya atau masukkan URL / kata kunci secara manual.")

        # Opsi Impor dari Diagnosa
        selected_url_imp = ""
        selected_snippet_imp = ""
        if dox_items:
            st.info(f"💡 Ditemukan **{len(dox_items)} temuan** dari scan Diagnosa sebelumnya. Anda bisa memilih dari daftar di bawah untuk autofill.")
            options_imp = ["-- Input Manual / Bebas --"] + [f"[{i.get('display_url','url')}] {i.get('title','')[:60]}" for i in dox_items]
            sel_idx_imp = st.selectbox("Impor Temuan Scan Diagnosa", range(len(options_imp)), format_func=lambda x: options_imp[x], key="rmv_imp_sel")
            if sel_idx_imp > 0:
                item_imp = dox_items[sel_idx_imp - 1]
                selected_url_imp = item_imp.get("url", "")
                selected_snippet_imp = item_imp.get("snippet", "")

        with st.form("form_create_removal_case"):
            col_c1, col_c2 = st.columns(2)
            with col_c1:
                c_client_name = st.text_input("👤 Nama Lengkap Client / Pemohon *", value=last_name or "Yusep Maulana", placeholder="Contoh: Yusep Maulana")
                c_client_phone = st.text_input("📱 Nomor HP Client", value=last_phone or "", placeholder="Contoh: 081234567890")
                c_target_url = st.text_input("🔗 URL Halaman / Komentar Target *", value=selected_url_imp, placeholder="Contoh: https://www.instagram.com/p/DD_7iamqwzf/")
            with col_c2:
                c_platform = st.selectbox("🌐 Platform Sumber", ["Instagram", "Facebook", "TikTok", "Google Search", "Twitter / X", "Website Publik", "Lainnya"])
                c_removal_type = st.selectbox("📌 Jenis Pengajuan Removal", ["Google Outdated Content (Gagal Cache/AI Overview)", "Google Legal Formal (Privacy/Defamation)", "DM / Email Admin Medsos", "Takedown Host/Webmaster"])
                c_keyword = st.text_input("🔤 Teks / Kata Kunci Doxing", value=f"BAYAR HUTANG {last_name}".strip() if last_name else "BAYAR HUTANG", placeholder="Contoh: BAYAR HUTANG, YUSEP MAULANA")

            c_snippet = st.text_area("📝 Snippet / Isi Komentar Doxing", value=selected_snippet_imp, placeholder="Contoh: Komentar teror dari DC pinjol...", height=70)
            c_notes = st.text_area("📋 Catatan Awal Kasus", placeholder="Catatan internal mengenai kronologi atau bukti yang dimiliki client...", height=60)

            btn_submit_case = st.form_submit_button("🚀 Simpan & Buat Case Pembersihan", type="primary", use_container_width=True)

            if btn_submit_case:
                if not c_client_name.strip() or not c_target_url.strip():
                    st.error("❌ Nama Client dan URL Target wajib diisi!")
                else:
                    new_id, new_code = db.create_removal_case(
                        client_name=c_client_name.strip(),
                        client_phone=c_client_phone.strip(),
                        target_url=c_target_url.strip(),
                        target_snippet=c_snippet.strip(),
                        target_keyword=c_keyword.strip(),
                        platform=c_platform,
                        removal_type=c_removal_type,
                        status="Draft",
                        progress_percent=10,
                        notes=c_notes.strip()
                    )
                    success_msg = f"🎉 **BERHASIL DISIMPAN!** Case Pembersihan **{new_code}** untuk *{c_client_name.strip()}* telah tersimpan ke database."
                    st.session_state["rmv_case_created_success"] = success_msg
                    st.toast(f"💾 Case {new_code} Berhasil Disimpan!", icon="✅")
                    st.rerun()

    # ══════════════════════════════════════════════════════════════════════
    # SUBTAB 3 - AI LEGAL GENERATOR & PANDUAN
    # ══════════════════════════════════════════════════════════════════════
    with tab_rmv3:
        st.markdown("#### 🤖 AI Removal Assistant & Generator Berkas Legal")
        st.caption("Pilih case pembersihan yang ada untuk membuat draf permohonan legal resmi berdasarkan UU PDP & UU ITE.")

        try:
            active_cases = db.get_removal_cases(limit=100)
        except Exception:
            active_cases = []

        if not active_cases:
            st.info("Belum ada case pembersihan di database. Buat case terlebih dahulu di tab sebelah.")
        else:
            case_options = [f"{c.get('case_code')} - {c.get('client_name')} ({c.get('target_url')[:40]}...)" for c in active_cases]
            sel_c_idx = st.selectbox("Pilih Case Pembersihan Data Target", range(len(case_options)), format_func=lambda x: case_options[x], key="rmv_ai_case_sel")

            selected_c_data = active_cases[sel_c_idx]

            g_url = selected_c_data.get("target_url", "")
            g_name = selected_c_data.get("client_name", "")
            g_phone = selected_c_data.get("client_phone", "")
            g_kw = selected_c_data.get("target_keyword", "")
            g_snip = selected_c_data.get("target_snippet", "")

            st.markdown("---")

            rmv_mode1, rmv_mode2, rmv_mode3 = st.tabs([
                "🤖 Jalur A: Google Outdated Content Tool",
                "⚖️ Jalur B: Form Google Legal Removal (UU PDP)",
                "📱 Jalur C: Pesan DM ke Admin Medsos",
            ])

            with rmv_mode1:
                st.markdown("##### 🤖 Panduan Google Outdated Content Removal Tool")
                st.caption("Gunakan metode ini jika komentar di Instagram/medsos **sudah dihapus/tidak ada**, namun **MASIH TERBACA di Google Search / AI Overview**.")
                outdated_info = rmv.generate_google_outdated_guide(g_url or "URL Target", g_kw)

                col_a1, col_a2 = st.columns([2, 1])
                with col_a1:
                    for step in outdated_info["steps"]:
                        st.markdown(step)
                with col_a2:
                    st.markdown("""
                    <div style="background:#0F1629; border:1px solid #00D4FF40; border-radius:12px; padding:16px; text-align:center;">
                        <div style="font-size:2rem; margin-bottom:8px;">🔗</div>
                        <div style="font-size:0.88rem; font-weight:700; color:#00D4FF;">Portal Resmi Google</div>
                        <div style="font-size:0.75rem; color:#8A9AB0; margin:8px 0;">Google Search Console Outdated Tool</div>
                        <a href="https://search.google.com/search-console/remove-outdated-content" target="_blank" style="
                            display:inline-block; padding:8px 16px; background:#00D4FF; color:#000; font-weight:700;
                            border-radius:8px; text-decoration:none; margin-top:8px;">
                            🚀 Buka Google Tool &rarr;
                        </a>
                    </div>
                    """, unsafe_allow_html=True)

            with rmv_mode2:
                st.markdown("##### ⚖️ Generator Surat Legal Removal (Google Privacy Form)")
                st.caption("Gunakan metode ini jika komentar/postingan teror **masih aktif** dan ingin minta Google menghapus berdasarkan UU PDP & ITE.")

                evidence_desc = st.text_area(
                    "Deskripsi Bukti Doxing / Pencemaran Nama Baik",
                    value=f"Postingan/komentar memuat tuduhan utang pinjol palsu, kata-kata ancaman, dan penyebaran data pribadi tanpa izin di URL {g_url}. Snippet: {g_snip}",
                    height=80,
                    key=f"ev_desc_{selected_c_data.get('id')}"
                )

                letter_text = rmv.generate_legal_removal_letter(
                    full_name=g_name,
                    nik="",
                    phone=g_phone,
                    email="",
                    target_url=g_url,
                    doxing_evidence_desc=evidence_desc,
                    platform_name="Google LLC / Tim Legal Compliance",
                )

                st.markdown("###### 📄 Draf Surat Permohonan Formal (Siap Disalin):")
                st.code(letter_text, language="markdown")

                st.markdown(
                    '<a href="https://support.google.com/legal/troubleshooter/1114905" target="_blank" style="'
                    'display:block; text-align:center; padding:10px; background:#00D4FF; color:#000; '
                    'font-weight:700; border-radius:8px; text-decoration:none;">'
                    '🌐 Buka Form Google Legal Removal &rarr;</a>',
                    unsafe_allow_html=True,
                )

            with rmv_mode3:
                st.markdown("##### 📱 Generator Pesan DM / WhatsApp ke Admin Media Sosial")
                dm_text = rmv.generate_admin_dm_message(
                    full_name=g_name,
                    target_post_link=g_url,
                    comment_text=g_snip or g_kw or "komentar teror utang/pinjol",
                )
                st.markdown("###### 💬 Draf Pesan ke Admin Medsos (Siap Kirim):")
                st.code(dm_text, language="text")

    # ══════════════════════════════════════════════════════════════════════
    # SUBTAB 4 - LIVE STATUS CHECKER
    # ══════════════════════════════════════════════════════════════════════
    with tab_rmv4:
        st.markdown("#### 🔍 Live Status Checker (Deteksi Quick HTTP & Indexing Google)")
        st.caption("Uji URL apapun secara independen untuk melihat apakah halaman web sumber masih aktif (HTTP 200) atau sudah terhapus (HTTP 404/410).")

        chk_input_url = st.text_input("🔗 URL Target Pengecekan", placeholder="https://www.instagram.com/p/xxxx/ atau URL web publik...")
        if st.button("🔍 Jalankan Live Check HTTP", type="primary"):
            if not chk_input_url.strip():
                st.error("Masukkan URL target terlebih dahulu.")
            else:
                with st.spinner("Menguji koneksi HTTP ke URL target..."):
                    res = rmv.check_url_indexing_status(chk_input_url.strip())
                    if res.get("success"):
                        st.info(f"### {res.get('message')}")
                        st.markdown(f"**Kode Status HTTP:** `{res.get('status_code')}`")
                        st.markdown(f"**Status Live Web:** `{'MASIH TAYANG' if res.get('is_live') else 'TERHAPUS / NOT FOUND'}`")
                    else:
                        st.warning(f"❌ {res.get('message')}")



# ══════════════════════════════════════════════════════════
# TAB 4 - INVESTIGASI DC & LAPORAN POLISI
# ══════════════════════════════════════════════════════════
def render_tab_investigasi():
    st.markdown("### 📡 Investigasi Nomor DC & Generator Laporan Polisi")
    st.caption(
        "Masukkan nomor HP DC (Debt Collector) peneror dan data kasus untuk "
        "mendapatkan profil intelijen dan membuat laporan pengaduan resmi."
    )

    ui.cyber_divider()

    # ── Section 1: Profil Nomor DC ─────────────────────────
    st.markdown("#### 📞 Profiling Nomor DC Peneror")

    col1, col2 = st.columns([2, 1])
    with col1:
        dc_phone_input = st.text_input(
            "🎯 Nomor HP DC Target",
            placeholder="Contoh: 081234567890 atau +6281234567890",
            help="Masukkan nomor HP DC/pinjol yang melakukan teror",
        )
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        btn_profile = st.button("🔍 Profil Nomor", use_container_width=True, type="primary")

    if btn_profile:
        if not dc_phone_input.strip():
            st.error("❌ Masukkan nomor HP DC terlebih dahulu.")
        else:
            with st.spinner("📡 Menganalisis intelijen HLR, GetContact, dan jejak web nomor DC..."):
                profile = phonep.profile_phone_number(dc_phone_input.strip())
                intel = pintel.run_phone_intelligence(dc_phone_input.strip())
                st.session_state.phone_profile = profile
                st.session_state.phone_intel_res = intel

            # ── AUTO-SAVE Investigasi DC ke Database ─────────
            try:
                tc_data = intel.get("truecaller", {}) if intel else {}
                gc_data = intel.get("getcontact", {}) if intel else {}
                fraud_data = intel.get("fraud_reports", {}) if intel else {}
                db.save_dc_investigation(
                    dc_phone=dc_phone_input.strip(),
                    operator=profile.get("carrier", "") if profile else "",
                    region=profile.get("region", "") if profile else "",
                    phone_type=profile.get("network_type", "") if profile else "",
                    truecaller_name=tc_data.get("name", ""),
                    is_spam=bool(tc_data.get("is_spam", False)),
                    getcontact_count=gc_data.get("save_count", 0),
                    has_fraud_report=bool(fraud_data.get("has_report", False)),
                    phone_score=intel.get("total_phone_score", 0) if intel else 0,
                    result_json={"profile": profile, "intel": intel},
                )
            except Exception as _e:
                pass

            st.success("✅ Profil intelijen nomor DC berhasil dibuat! 💾 Tersimpan ke riwayat")

    # Tampilkan profil jika ada
    if st.session_state.get("phone_profile"):
        profile = st.session_state.phone_profile
        intel_data = st.session_state.get("phone_intel_res") or {}
        
        ui.render_intel_card(profile)

        if intel_data:
            st.markdown("##### 🔍 Hasil Intelijen Tambahan (Reputasi & Jejak Digital)")
            cols_i1, cols_i2 = st.columns(2)
            with cols_i1:
                tc = intel_data.get("truecaller", {})
                tc_name = tc.get('name') or 'Tidak Terdaftar Publik'
                st.markdown(f"**Truecaller Name:** `{tc_name}`")
                st.markdown(f"**Status Spammer:** {'🚨 Ya (Di-flag Spam)' if tc.get('is_spam') else '🟢 Normal'}")
            with cols_i2:
                gc = intel_data.get("getcontact", {})
                gc_count = gc.get('save_count', 0)
                st.markdown(f"**GetContact Tags Count:** `{gc_count} simpanan nama`")
                st.markdown(f"**Laporan Fraud CekRekening / Kredibel:** {'🚨 Ditemukan Laporan' if intel_data.get('fraud_reports',{}).get('has_report') else '🟢 Belum Ada Laporan'}")

            # Tampilkan tag GetContact jika ada
            if gc.get("saved_names"):
                st.info(f"🏷️ **Tag GetContact Ditemukan:** {', '.join(gc['saved_names'])}")
            elif gc.get("details"):
                for dt in gc["details"]:
                    st.caption(f"ℹ️ GetContact OSINT: {dt}")

            # Direct Action Probe Buttons
            raw_input_ph = dc_phone_input.strip().replace(" ", "").replace("-", "")
            if raw_input_ph.startswith("62"):
                local_num = "0" + raw_input_ph[2:]
                e164_num = raw_input_ph
            elif raw_input_ph.startswith("+62"):
                local_num = "0" + raw_input_ph[3:]
                e164_num = raw_input_ph[1:]
            elif raw_input_ph.startswith("0"):
                local_num = raw_input_ph
                e164_num = "62" + raw_input_ph[1:]
            else:
                local_num = "0" + raw_input_ph
                e164_num = "62" + raw_input_ph

            dork_search_query = f'"{local_num}" OR "{e164_num}" OR "+{e164_num}"'
            from urllib.parse import quote_plus
            dork_encoded = quote_plus(dork_search_query)
            gc_encoded = quote_plus("+" + e164_num)

            st.markdown("##### 🚀 Akses Langsung Profil & Direct Live Probe")
            col_act1, col_act2, col_act3 = st.columns(3)
            with col_act1:
                st.markdown(f'<a href="https://getcontact.com/en/search?q={gc_encoded}" target="_blank" style="display:block; text-align:center; padding:10px; background:#4B0082; color:#fff; font-weight:700; border-radius:8px; text-decoration:none;">📲 Probe GetContact App/Web &rarr;</a>', unsafe_allow_html=True)
            with col_act2:
                st.markdown(f'<a href="https://www.truecaller.com/search/id/{local_num}" target="_blank" style="display:block; text-align:center; padding:10px; background:#0087FF; color:#fff; font-weight:700; border-radius:8px; text-decoration:none;">📞 Probe Truecaller Web &rarr;</a>', unsafe_allow_html=True)
            with col_act3:
                st.markdown(f'<a href="https://www.kredibel.co/search/phone/{local_num}" target="_blank" style="display:block; text-align:center; padding:10px; background:#E53935; color:#fff; font-weight:700; border-radius:8px; text-decoration:none;">🛡️ Cek Fraud Kredibel &rarr;</a>', unsafe_allow_html=True)

            col_act4, col_act5, col_act6 = st.columns(3)
            with col_act4:
                st.markdown(f'<a href="https://wa.me/{e164_num}" target="_blank" style="display:block; text-align:center; padding:10px; background:#25D366; color:#fff; font-weight:700; border-radius:8px; text-decoration:none;">📱 Buka WhatsApp Direct &rarr;</a>', unsafe_allow_html=True)
            with col_act5:
                st.markdown(f'<a href="https://www.google.com/search?q={dork_encoded}" target="_blank" style="display:block; text-align:center; padding:10px; background:#4285F4; color:#fff; font-weight:700; border-radius:8px; text-decoration:none;">🔍 Dorking Google ({local_num}) &rarr;</a>', unsafe_allow_html=True)
            with col_act6:
                st.markdown(f'<a href="https://t.me/s/{local_num}" target="_blank" style="display:block; text-align:center; padding:10px; background:#0088cc; color:#fff; font-weight:700; border-radius:8px; text-decoration:none;">✈️ Cek Telegram &rarr;</a>', unsafe_allow_html=True)

        if profile.get("success"):
            # Template permohonan data teknis
            with st.expander("📋 Template Permohonan Data Teknis (CDR/Cell-ID) untuk Penyidik Kepolisian"):
                bts_template = phonep.get_bts_request_template(
                    profile.get("format_e164", dc_phone_input),
                    profile.get("carrier", "Operator Terkait"),
                    profile.get("region", "Tidak Teridentifikasi"),
                )
                st.code(bts_template, language="text")
                st.caption("📄 Teks ini dilampirkan dalam Surat Pengaduan Polisi resmi agar penyidik dapat meminta Data BTS/Cell-ID ke Operator.")

    ui.cyber_divider()

    # ── Section 2: Generator Laporan Polisi ──────────────────
    st.markdown("#### 📄 Generator Laporan Pengaduan Siber (PDF)")
    st.info(
        "💡 Isi form di bawah untuk membuat dokumen laporan pengaduan siber yang dapat "
        "digunakan sebagai pendukung pelaporan ke Polres/Bareskrim Polri."
    )

    with st.form("form_laporan_polisi"):
        st.markdown("##### 👤 Identitas Pelapor")
        col1, col2 = st.columns(2)
        with col1:
            reporter_name = st.text_input("Nama Lengkap Pelapor *", placeholder="Nama sesuai KTP")
            reporter_nik = st.text_input("NIK / Nomor KTP *", placeholder="16 digit NIK")
        with col2:
            reporter_phone = st.text_input("Nomor HP Aktif Pelapor *", placeholder="081xxxxxxxxx")
            reporter_address = st.text_area(
                "Alamat Domisili *",
                placeholder="Jl. Contoh No. 1, Kelurahan, Kecamatan, Kota/Kab, Provinsi",
                height=80,
            )

        st.markdown("##### 🎯 Data Pelaku / DC")
        col3, col4 = st.columns(2)
        with col3:
            dc_phone_report = st.text_input(
                "Nomor HP DC Peneror *",
                value=dc_phone_input if dc_phone_input else "",
                placeholder="081xxxxxxxxx",
            )
        with col4:
            st.markdown("<br>", unsafe_allow_html=True)
            st.caption("💡 Akan diisi otomatis dari hasil profiling di atas jika sudah dijalankan.")

        st.markdown("##### 📝 Kronologi & Bukti")
        incident_summary = st.text_area(
            "Kronologi Kejadian *",
            placeholder=(
                "Contoh: Pada tanggal DD/MM/YYYY pukul HH:MM WIB, saya menerima panggilan "
                "dari nomor +62xxx yang mengaku sebagai DC dari aplikasi pinjol [Nama App]. "
                "DC tersebut mengancam akan menyebarkan foto saya kepada seluruh kontak HP..."
            ),
            height=150,
            help="Ceritakan kronologi secara runtut dan detail",
        )
        terror_messages = st.text_area(
            "Contoh Pesan Teror (copy-paste dari chat)",
            placeholder=(
                'Contoh:\n"Kalau tidak bayar hari ini, kami akan sebar fotomu ke semua kontak!"\n'
                '"Hutangmu sekarang menjadi Rp 5.000.000, harus lunas jam 12 siang!"\n'
                '"Kami sudah punya semua data kamu, keluarga kamu juga kami hubungi!"'
            ),
            height=120,
        )

        st.markdown("##### 📎 Upload Bukti (Opsional)")
        uploaded_files = st.file_uploader(
            "Upload tangkapan layar atau bukti dokumen",
            type=["jpg", "jpeg", "png", "pdf"],
            accept_multiple_files=True,
            help="Maksimum 50MB per file. Format: JPG, PNG, PDF",
        )

        col_btn1, col_btn2 = st.columns([3, 1])
        with col_btn2:
            generate_pdf = st.form_submit_button(
                "📄 Generate PDF",
                use_container_width=True,
                type="primary",
            )

    # ── Generate PDF ────────────────────────────────────────
    if generate_pdf:
        # Validasi
        errors = []
        if not reporter_name.strip():
            errors.append("Nama Lengkap Pelapor")
        if not reporter_nik.strip():
            errors.append("NIK / Nomor KTP")
        if not reporter_phone.strip():
            errors.append("Nomor HP Pelapor")
        if not reporter_address.strip():
            errors.append("Alamat Domisili")
        if not dc_phone_report.strip():
            errors.append("Nomor HP DC Peneror")
        if not incident_summary.strip():
            errors.append("Kronologi Kejadian")

        if errors:
            st.error(f"❌ Field wajib belum diisi: **{', '.join(errors)}**")
        else:
            with st.spinner("📝 Menyusun dokumen laporan PDF..."):
                # Profil nomor DC (gunakan yang sudah ada atau parse ulang)
                if (
                    st.session_state.phone_profile
                    and st.session_state.phone_profile.get("success")
                    and dc_phone_report.strip() in [
                        dc_phone_input,
                        st.session_state.phone_profile.get("input_original", ""),
                    ]
                ):
                    phone_profile = st.session_state.phone_profile
                else:
                    phone_profile = phonep.profile_phone_number(dc_phone_report.strip())

                # Info file upload
                files_info = []
                if uploaded_files:
                    for f in uploaded_files:
                        ext = f.name.split(".")[-1].upper()
                        file_type = "Gambar (Screenshot)" if ext in ["JPG", "JPEG", "PNG"] else "Dokumen PDF"
                        files_info.append({
                            "name": f.name,
                            "type": file_type,
                            "description": f"Bukti digital: {f.name}",
                            "date": datetime.now().strftime("%d/%m/%Y"),
                        })

                # Generate PDF
                try:
                    pdf_bytes = rgen.generate_police_report(
                        reporter_name=reporter_name.strip(),
                        reporter_nik=reporter_nik.strip(),
                        reporter_phone=reporter_phone.strip(),
                        reporter_address=reporter_address.strip(),
                        dc_phone_raw=dc_phone_report.strip(),
                        phone_profile=phone_profile,
                        incident_summary=incident_summary.strip(),
                        terror_messages=terror_messages.strip(),
                        uploaded_files_info=files_info,
                        report_date=datetime.now().strftime("%d %B %Y"),
                    )

                    filename = (
                        f"Laporan_Pinjol_{reporter_name.replace(' ','_')}"
                        f"_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                    )

                    # ── AUTO-SAVE Laporan Polisi ke Database ──
                    try:
                        db.save_police_report(
                            reporter_name=reporter_name.strip(),
                            reporter_nik=reporter_nik.strip(),
                            reporter_phone=reporter_phone.strip(),
                            dc_phone=dc_phone_report.strip(),
                            incident_summary=incident_summary.strip(),
                            filename=filename,
                        )
                    except Exception as _e:
                        pass

                    st.success("✅ Laporan PDF berhasil dibuat! 💾 Tersimpan ke riwayat")
                    st.markdown("---")
                    col_dl1, col_dl2 = st.columns([2, 1])
                    with col_dl1:
                        st.info(
                            "📋 **Cara Menggunakan Laporan Ini:**\n\n"
                            "1. Unduh file PDF menggunakan tombol di samping\n"
                            "2. Print / cetak dokumen (bisa hitam-putih)\n"
                            "3. Tandatangani di atas materai Rp 10.000\n"
                            "4. Datang ke **SPKT Polres/Polda** terdekat dengan membawa:\n"
                            "   - Dokumen laporan ini\n"
                            "   - KTP asli\n"
                            "   - Screenshot/bukti teror asli di HP Anda"
                        )
                    with col_dl2:
                        st.download_button(
                            label="⬇️ Unduh Laporan PDF",
                            data=pdf_bytes,
                            file_name=filename,
                            mime="application/pdf",
                            use_container_width=True,
                        )
                except Exception as e:
                    st.error(f"❌ Gagal membuat PDF: {str(e)}")
                    st.exception(e)


# ══════════════════════════════════════════════════════════
# TAB 5 - RIWAYAT & TRACKING
# ══════════════════════════════════════════════════════════
def render_tab_riwayat():
    # ── Stats Summary ────────────────────────────────────────
    try:
        stats = db.get_dashboard_stats()
    except Exception:
        stats = {}

    st.markdown("""
    <div style="margin-bottom:20px;">
        <div class="section-header">📋 Riwayat & Tracking</div>
        <div class="section-sub">Semua aktivitas tersimpan otomatis. Lihat detail, proses ulang, atau hapus record.</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Stat Cards ────────────────────────────────────────────
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(f"""<div class="stat-mini"><div class="val">{stats.get('total_scans', 0)}</div>
        <div class="lbl">Total Diagnosa</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="stat-mini"><div class="val" style="color:#FF5252">{stats.get('high_risk_count', 0)}</div>
        <div class="lbl">Risiko Tinggi</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="stat-mini"><div class="val" style="color:#7B61FF">{stats.get('total_dc', 0)}</div>
        <div class="lbl">Investigasi DC</div></div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="stat-mini"><div class="val" style="color:#FFD740">{stats.get('total_removals', 0)}</div>
        <div class="lbl">Removal Request</div></div>""", unsafe_allow_html=True)
    with c5:
        st.markdown(f"""<div class="stat-mini"><div class="val" style="color:#00E676">{stats.get('total_reports', 0)}</div>
        <div class="lbl">Laporan PDF</div></div>""", unsafe_allow_html=True)

    ui.cyber_divider()

    # ── Sub-tabs Riwayat ──────────────────────────────────────
    rtab1, rtab2, rtab3, rtab4 = st.tabs([
        f"🔍 Diagnosa ({stats.get('total_scans', 0)})",
        f"📡 Investigasi DC ({stats.get('total_dc', 0)})",
        f"📑 Removal ({stats.get('total_removals', 0)})",
        f"📄 Laporan PDF ({stats.get('total_reports', 0)})",
    ])

    # ── Tab Riwayat Diagnosa ──────────────────────────────────
    with rtab1:
        scan_history = db.get_scan_history(limit=50)
        if not scan_history:
            st.markdown("""
            <div style="text-align:center; padding:60px 20px; color:#2A4060;">
                <div style="font-size:3rem; margin-bottom:12px;">🔍</div>
                <div style="font-size:1rem; font-weight:600; color:#3A5070;">Belum Ada Riwayat Diagnosa</div>
                <div style="font-size:0.82rem; margin-top:6px;">Jalankan scan di tab Diagnosa Jejak Digital untuk melihat riwayat di sini.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Filter & Search
            col_search, col_sort, col_del = st.columns([3, 1, 1])
            with col_search:
                search_scan = st.text_input("🔎 Cari nama / nomor", placeholder="Ketik untuk filter...", key="search_scan_hist", label_visibility="collapsed")
            with col_sort:
                sort_risk = st.selectbox("Sort", ["Terbaru", "Risiko Tertinggi", "Risiko Terendah"], key="sort_scan_hist", label_visibility="collapsed")
            with col_del:
                if st.button("🗑️ Hapus Semua", key="del_all_scans", use_container_width=True):
                    st.session_state["confirm_del_all_scans"] = True

            if st.session_state.get("confirm_del_all_scans"):
                st.warning("⚠️ Yakin hapus **SEMUA** riwayat diagnosa?")
                ca, cb = st.columns(2)
                with ca:
                    if st.button("✅ Ya, Hapus Semua", key="confirm_del_all_y"):
                        db.delete_all_scans()
                        st.session_state.pop("confirm_del_all_scans", None)
                        st.rerun()
                with cb:
                    if st.button("❌ Batal", key="confirm_del_all_n"):
                        st.session_state.pop("confirm_del_all_scans", None)
                        st.rerun()

            # Filter
            filtered = scan_history
            if search_scan:
                q = search_scan.lower()
                filtered = [r for r in scan_history if q in (r.get("target_name","") or "").lower()
                            or q in (r.get("target_phone","") or "").lower()
                            or q in (r.get("target_email","") or "").lower()]
            if sort_risk == "Risiko Tertinggi":
                filtered = sorted(filtered, key=lambda x: x.get("risk_score", 0), reverse=True)
            elif sort_risk == "Risiko Terendah":
                filtered = sorted(filtered, key=lambda x: x.get("risk_score", 0))

            st.caption(f"Menampilkan {len(filtered)} dari {len(scan_history)} record")
            for i, row in enumerate(filtered):
                ui.render_scan_history_row(row, i)

    # ── Tab Riwayat Investigasi DC ────────────────────────────
    with rtab2:
        dc_history = db.get_dc_history(limit=50)
        if not dc_history:
            st.markdown("""
            <div style="text-align:center; padding:60px 20px; color:#2A4060;">
                <div style="font-size:3rem; margin-bottom:12px;">📡</div>
                <div style="font-size:1rem; font-weight:600; color:#3A5070;">Belum Ada Riwayat Investigasi DC</div>
                <div style="font-size:0.82rem; margin-top:6px;">Jalankan investigasi nomor DC di tab Investigasi DC & Laporan.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            col_s, col_d = st.columns([4, 1])
            with col_s:
                search_dc = st.text_input("🔎 Cari nomor DC", placeholder="Ketik nomor HP DC...", key="search_dc_hist", label_visibility="collapsed")
            with col_d:
                if st.button("🗑️ Hapus Semua", key="del_all_dc", use_container_width=True):
                    st.session_state["confirm_del_all_dc"] = True

            if st.session_state.get("confirm_del_all_dc"):
                st.warning("⚠️ Yakin hapus **SEMUA** riwayat investigasi DC?")
                ca, cb = st.columns(2)
                with ca:
                    if st.button("✅ Ya, Hapus Semua", key="confirm_del_all_dc_y"):
                        db.delete_all_dc()
                        st.session_state.pop("confirm_del_all_dc", None)
                        st.rerun()
                with cb:
                    if st.button("❌ Batal", key="confirm_del_all_dc_n"):
                        st.session_state.pop("confirm_del_all_dc", None)
                        st.rerun()

            filtered_dc = dc_history
            if search_dc:
                filtered_dc = [r for r in dc_history if search_dc.lower() in (r.get("dc_phone","") or "").lower()]

            st.caption(f"Menampilkan {len(filtered_dc)} dari {len(dc_history)} record")
            for i, row in enumerate(filtered_dc):
                ui.render_dc_history_row(row, i)

    # ── Tab Riwayat Removal ───────────────────────────────────
    with rtab3:
        removal_history = db.get_removal_history(limit=50)
        if not removal_history:
            st.markdown("""
            <div style="text-align:center; padding:60px 20px; color:#2A4060;">
                <div style="font-size:3rem; margin-bottom:12px;">📑</div>
                <div style="font-size:1rem; font-weight:600; color:#3A5070;">Belum Ada Riwayat Removal</div>
                <div style="font-size:0.82rem; margin-top:6px;">Generate surat removal di tab Asisten Removal untuk melihat riwayat di sini.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.caption(f"{len(removal_history)} request tersimpan | Update status sesuai progress tindak lanjut")
            for i, row in enumerate(removal_history):
                ui.render_removal_history_row(row, i)

    # ── Tab Riwayat Laporan PDF ───────────────────────────────
    with rtab4:
        report_history = db.get_police_report_history(limit=50)
        if not report_history:
            st.markdown("""
            <div style="text-align:center; padding:60px 20px; color:#2A4060;">
                <div style="font-size:3rem; margin-bottom:12px;">📄</div>
                <div style="font-size:1rem; font-weight:600; color:#3A5070;">Belum Ada Riwayat Laporan</div>
                <div style="font-size:0.82rem; margin-top:6px;">Generate laporan PDF di tab Investigasi DC & Laporan.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.caption(f"{len(report_history)} laporan telah digenerate")
            for i, row in enumerate(report_history):
                ui.render_police_report_history_row(row, i)


# ══════════════════════════════════════════════════════════
# TAB 6 - PENGATURAN API
# ══════════════════════════════════════════════════════════
def render_tab_settings():
    st.markdown("### ⚙️ Pengaturan API & Konfigurasi Sistem")
    st.caption("Konfigurasi API Key untuk mengaktifkan fitur scan dan breach checking.")

    ui.cyber_divider()

    # ── Status API ─────────────────────────────────────────
    st.markdown("#### 📊 Status Konfigurasi Saat Ini")
    api_status = cfg.get_api_status()
    cols = st.columns(len(api_status))
    for col, (name, is_active) in zip(cols, api_status.items()):
        with col:
            status_color = "#00E676" if is_active else "#FF5252"
            status_text = "AKTIF" if is_active else "BELUM DIKONFIGURASI"
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#0A1428,#0F1629);
                        border:1px solid {status_color}40; border-top:3px solid {status_color};
                        border-radius:12px; padding:16px; text-align:center;">
                <div style="font-size:1.3rem;">{'✅' if is_active else '❌'}</div>
                <div style="font-size:0.8rem; font-weight:700; color:{status_color}; margin:4px 0;">
                    {status_text}
                </div>
                <div style="font-size:0.75rem; color:#6E7E9A;">{name}</div>
            </div>
            """, unsafe_allow_html=True)

    ui.cyber_divider()

    # ── Form API Keys ──────────────────────────────────────
    st.markdown("#### 🔑 Input API Key")

    with st.form("form_api_keys"):
        # Google Search API
        st.markdown("##### 🔍 Google Custom Search API (Opsional)")
        col1, col2 = st.columns(2)
        with col1:
            google_api_key = st.text_input(
                "Google API Key",
                value=cfg.get_api_key("google_api_key"),
                type="password",
                placeholder="AIza...",
                help="Dapatkan di: console.cloud.google.com → Custom Search JSON API",
            )
        with col2:
            google_cx = st.text_input(
                "Search Engine ID (CX)",
                value=cfg.get_api_key("google_cx"),
                type="password",
                placeholder="xxxxxxxxxxxxxxxx:xxxxxxxxxxx",
                help="Dapatkan di: programmablesearchengine.google.com",
            )

        st.markdown("""
        <div style="background:#0A1428; border:1px solid #1E2D50; border-radius:8px;
                    padding:12px 16px; margin: 8px 0; font-size:0.82rem; color:#8A9AB0;">
            💡 <b>Cara mendapatkan Google Custom Search API:</b><br>
            1. Buka <a href="https://console.cloud.google.com" target="_blank" style="color:#00D4FF;">console.cloud.google.com</a>
               → Aktifkan "Custom Search JSON API"<br>
            2. Buat API Key di menu <i>Credentials</i><br>
            3. Buka <a href="https://programmablesearchengine.google.com" target="_blank" style="color:#00D4FF;">programmablesearchengine.google.com</a>
               → Buat Search Engine → Salin CX ID<br>
            4. Kuota gratis: <b>100 query/hari</b>. Rp 500/1000 query selanjutnya.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # HIBP API
        st.markdown("##### 💥 HaveIBeenPwned API")
        hibp_api_key = st.text_input(
            "HIBP API Key",
            value=cfg.get_api_key("hibp_api_key"),
            type="password",
            placeholder="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            help="Dapatkan di: haveibeenpwned.com/API/Key (berbayar ~$3.50/bulan)",
        )
        st.markdown("""
        <div style="background:#0A1428; border:1px solid #1E2D50; border-radius:8px;
                    padding:12px 16px; margin: 8px 0; font-size:0.82rem; color:#8A9AB0;">
            💡 Langganan HIBP mulai dari <b>$3.50/bulan</b> untuk personal use. Daftar di
            <a href="https://haveibeenpwned.com/API/Key" target="_blank" style="color:#00D4FF;">haveibeenpwned.com/API/Key</a>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # SerpAPI (Opsional)
        st.markdown("##### 🔎 SerpAPI (Opsional - Alternatif Google Search)")
        serp_api_key = st.text_input(
            "SerpAPI Key (Opsional)",
            value=cfg.get_api_key("serp_api_key"),
            type="password",
            placeholder="xxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            help="Opsional. Dapatkan di: serpapi.com. 100 query/bulan gratis.",
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # Info penting sebelum tombol
        st.markdown("""
        <div style="background:rgba(0,212,255,0.05); border:1px solid rgba(0,212,255,0.2);
                    border-radius:10px; padding:12px 16px; margin-bottom:12px; font-size:0.82rem; color:#6A9AB0;">
            💡 <b style="color:#00D4FF;">Simpan Permanen</b> akan menulis ke file <code>.env</code> sehingga
            API Key tidak hilang meski browser ditutup atau halaman di-reload.
        </div>
        """, unsafe_allow_html=True)

        col_save1, col_save2 = st.columns([2, 1])
        with col_save1:
            save_file = st.form_submit_button(
                "💾 Simpan Permanen (ke .env)",
                use_container_width=True,
                type="primary",
                help="Menyimpan ke file .env - permanen, tidak hilang saat reload"
            )
        with col_save2:
            save_session = st.form_submit_button(
                "⚡ Simpan Sesi Saja",
                use_container_width=True,
                help="Hanya untuk sesi ini - hilang saat halaman di-reload"
            )

    if save_file:
        success, msg = cfg.save_to_env_file(google_api_key, google_cx, hibp_api_key, serp_api_key)
        if success:
            st.success(f"{msg}")
            st.info("🔄 API Key sudah aktif. Halaman akan di-refresh...")
            st.rerun()
        else:
            st.error(f"❌ {msg}")

    if save_session:
        cfg.save_api_keys(google_api_key, google_cx, hibp_api_key, serp_api_key)
        st.success("⚡ API Key disimpan ke sesi ini (tidak permanen - akan hilang saat reload).")
        st.rerun()

    ui.cyber_divider()

    # ── Info Keamanan ──────────────────────────────────────
    st.markdown("#### 🔒 Catatan Keamanan")
    st.warning(
        "⚠️ **Penting:** API Key disimpan secara lokal di session Streamlit atau file `.env`. "
        "Jangan bagikan API Key Anda kepada siapapun. "
        "Jika menggunakan Streamlit Cloud, gunakan fitur **Secrets** di dashboard deployment."
    )

    st.markdown("""
    **📝 Cara penggunaan aman:**
    - **Lokal (Recommended):** Simpan ke `.env` → otomatis ter-load setiap kali app restart
    - **Streamlit Cloud:** Tambahkan key di *App Settings → Secrets* dalam format TOML
    - Jangan commit file `.env` ke Git/GitHub - sudah ada di `.gitignore`
    """)

    ui.cyber_divider()

    # ── Reset Session ──────────────────────────────────────
    st.markdown("#### 🗑️ Reset Data Sesi")
    col_r1, col_r2 = st.columns([3, 1])
    with col_r2:
        if st.button("🔄 Hapus Semua Hasil Scan", use_container_width=True):
            for key in ["scan_results", "breach_results", "risk_data", "phone_profile", "last_scan_input"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.success("✅ Data sesi berhasil dihapus.")
            st.rerun()
    with col_r1:
        st.caption("Hapus semua hasil scan dan profil nomor dari memori sesi saat ini.")

    ui.cyber_divider()

    # ── Manajemen Akses Admin & Password ──────────────────────
    st.markdown("#### 🔑 Ubah Password Admin")
    st.caption("Perbarui kata sandi akun admin aktif untuk menjaga keamanan sistem.")

    with st.form("form_change_admin_pw"):
        import modules.auth as auth
        curr_u = auth.get_current_user()
        username_str = curr_u.get("username", "admin") if curr_u else "admin"

        st.info(f"Mengubah password untuk akun admin aktif: **{username_str}**")
        old_pw = st.text_input("Password Lama", type="password", key="input_old_pw")
        new_pw = st.text_input("Password Baru (Min. 6 karakter)", type="password", key="input_new_pw")
        confirm_pw = st.text_input("Konfirmasi Password Baru", type="password", key="input_conf_pw")

        btn_change_pw = st.form_submit_button("🔒 Simpan Password Baru", use_container_width=True)
        if btn_change_pw:
            if not old_pw or not new_pw:
                st.error("❌ Semua field password harus diisi!")
            elif new_pw != confirm_pw:
                st.error("❌ Password baru dan konfirmasi password tidak cocok!")
            elif len(new_pw) < 6:
                st.error("❌ Password baru minimal 6 karakter!")
            else:
                user_obj = db.get_admin_user(username_str)
                if not user_obj or not auth.verify_password(old_pw, user_obj['password_hash'], user_obj['salt']):
                    st.error("❌ Password lama salah!")
                else:
                    new_hash, new_salt = auth.hash_password(new_pw)
                    if db.update_admin_password(username_str, new_hash, new_salt):
                        st.success("✅ Password admin berhasil diperbarui!")
                    else:
                        st.error("❌ Gagal memperbarui password di database.")


# ══════════════════════════════════════════════════════════
# MAIN APP
# ══════════════════════════════════════════════════════════
def main():
    # Inisialisasi database & session
    db.init_database()
    init_session_state()
    ui.inject_css()

    # Auth Gatekeeper - Restrict access to logged-in admin only
    import modules.auth as auth
    if not auth.is_authenticated():
        auth.render_login_screen()
        st.stop()

    # Render sidebar
    render_sidebar()

    # Header utama
    ui.render_app_header()

    # Navigasi tabs (7 Tab Utama)
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "🏠 Dashboard",
        "👥 Data Klien",
        "🔍 Diagnosa Jejak Digital",
        "📑 Asisten Removal",
        "📡 Investigasi DC & Laporan",
        "📋 Riwayat & Tracking",
        "⚙️ Pengaturan",
    ])

    with tab1:
        render_tab_dashboard()
    with tab2:
        render_tab_clients()
    with tab3:
        render_tab_diagnosa()
    with tab4:
        render_tab_removal_assistant()
    with tab5:
        render_tab_investigasi()
    with tab6:
        render_tab_riwayat()
    with tab7:
        render_tab_settings()


if __name__ == "__main__":
    main()

