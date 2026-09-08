"""
Menyalahati Cyber Intelligence - Professional UI Components
Enterprise Dark Theme (SaaS Dashboard Aesthetic)
"""
import streamlit as st
from typing import Dict, List, Optional
from datetime import datetime


# ─── Injeksi CSS Global - Modern Enterprise Theme ──────────────────
GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* ─── Base Canvas ───────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #F8FAFC;
}

.stApp {
    background-color: #0F172A;
}

/* ─── Sidebar Styling ───────────────────────────── */
section[data-testid="stSidebar"] {
    background-color: #111827 !important;
    border-right: 1px solid #1F2937 !important;
}
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #9CA3AF;
}

/* ─── Main Container ───────────────────────────── */
.main .block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1240px;
}

/* ─── Tab Styling (Modern Segmented / Pill style) ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    background: #1E293B;
    border: 1px solid #334155;
    border-radius: 10px;
    padding: 6px;
    margin-bottom: 1.5rem;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 6px;
    color: #94A3B8;
    font-weight: 600;
    font-size: 0.85rem;
    padding: 8px 16px;
    border: none;
    transition: all 0.15s ease-in-out;
}
.stTabs [data-baseweb="tab"]:hover {
    color: #F8FAFC;
    background: rgba(255,255,255,0.05);
}
.stTabs [aria-selected="true"] {
    color: #FFFFFF !important;
    background: #2563EB !important;
    font-weight: 700 !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.3);
}
.stTabs [data-baseweb="tab-panel"] {
    padding-top: 0.5rem;
    background: transparent;
}

/* ─── Metric Cards ─────────────────────────────── */
[data-testid="metric-container"] {
    background: #1E293B;
    border: 1px solid #334155;
    border-radius: 10px;
    padding: 16px 20px;
    transition: all 0.2s ease;
    box-shadow: 0 1px 3px rgba(0,0,0,0.2);
}
[data-testid="metric-container"]:hover {
    border-color: #475569;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}
[data-testid="metric-container"] label {
    color: #94A3B8 !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
    text-transform: uppercase !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #F8FAFC !important;
    font-size: 1.75rem !important;
    font-weight: 700 !important;
}
[data-testid="metric-container"] [data-testid="stMetricDelta"] {
    font-size: 0.78rem !important;
}

/* ─── Buttons ──────────────────────────────────── */
.stButton > button[kind="primary"] {
    background: #2563EB;
    color: #FFFFFF;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.88rem;
    padding: 10px 20px;
    transition: all 0.15s ease;
    box-shadow: 0 1px 2px rgba(0,0,0,0.2);
}
.stButton > button[kind="primary"]:hover {
    background: #1D4ED8;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
}
.stButton > button[kind="secondary"], .stButton > button:not([kind]) {
    background: #1E293B;
    color: #E2E8F0;
    border: 1px solid #334155;
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.85rem;
    padding: 9px 18px;
    transition: all 0.15s ease;
}
.stButton > button[kind="secondary"]:hover, .stButton > button:not([kind]):hover {
    border-color: #64748B;
    background: #334155;
    color: #FFFFFF;
}

/* ─── Download Button ──────────────────────────── */
.stDownloadButton > button {
    background: #059669;
    color: #FFFFFF;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    padding: 10px 20px;
    transition: all 0.15s ease;
}
.stDownloadButton > button:hover {
    background: #047857;
    box-shadow: 0 4px 12px rgba(5, 150, 105, 0.3);
}

/* ─── Form Inputs ──────────────────────────────── */
.stTextInput input, .stTextArea textarea, .stSelectbox select {
    background: #0F172A !important;
    border: 1px solid #334155 !important;
    border-radius: 8px !important;
    color: #F8FAFC !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.88rem !important;
    padding: 10px 14px !important;
    transition: border-color 0.15s ease;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #3B82F6 !important;
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
    background: #0F172A !important;
}
.stTextInput label, .stTextArea label, .stSelectbox label {
    color: #94A3B8 !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    margin-bottom: 4px !important;
}

/* ─── Expander ─────────────────────────────────── */
.streamlit-expanderHeader {
    background: #1E293B !important;
    border: 1px solid #334155 !important;
    border-radius: 8px !important;
    font-weight: 600;
    color: #E2E8F0 !important;
    padding: 12px 16px !important;
}
.streamlit-expanderHeader:hover {
    border-color: #475569 !important;
    color: #FFFFFF !important;
}
.streamlit-expanderContent {
    background: #111827 !important;
    border: 1px solid #334155 !important;
    border-top: none !important;
    border-radius: 0 0 8px 8px !important;
    padding: 16px !important;
}

/* ─── Form Container ────────────────────────────── */
[data-testid="stForm"] {
    background: #1E293B;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.2);
}

/* ─── Divider ──────────────────────────────────── */
.cyber-divider {
    height: 1px;
    background: #334155;
    margin: 20px 0;
}

/* ─── Scrollbar ────────────────────────────────── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0F172A; }
::-webkit-scrollbar-thumb { background: #334155; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #475569; }
</style>
"""


def inject_css():
    """Injeksikan CSS global ke halaman Streamlit."""
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


def cyber_divider():
    """Garis pembatas komponen."""
    st.markdown('<div class="cyber-divider"></div>', unsafe_allow_html=True)


def render_app_header():
    """Header utama aplikasi - Dashboard Pro."""
    now_str = datetime.now().strftime("%d %b %Y, %H:%M WIB")
    st.markdown(f"""
    <div style="
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.2);
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 16px;
    ">
        <div style="display:flex; align-items:center; gap:14px;">
            <div style="
                width:46px; height:46px;
                background: #2563EB;
                border-radius: 10px;
                display:flex; align-items:center; justify-content:center;
                font-size:1.4rem;
                color: #FFFFFF;
            ">🔍</div>
            <div>
                <div style="
                    font-size: 1.4rem;
                    font-weight: 800;
                    color: #F8FAFC;
                    line-height: 1.2;
                ">Menyalahati Cyber Intelligence</div>
                <div style="font-size: 0.78rem; color: #94A3B8; font-weight: 500; margin-top: 2px;">
                    OSINT &bull; Anti Doxing &bull; DC Profiler &bull; Sistem Monitoring Kasus
                </div>
            </div>
        </div>
        <div style="display:flex; align-items:center; gap:12px;">
            <div style="text-align:right;">
                <div style="font-size:0.7rem; color:#94A3B8; text-transform:uppercase; letter-spacing:0.5px;">Status Sistem</div>
                <div style="font-size:0.85rem; font-weight:600; color:#E2E8F0; font-family:'JetBrains Mono',monospace;">{now_str}</div>
            </div>
            <div style="
                padding: 5px 12px;
                background: rgba(16, 185, 129, 0.1);
                border: 1px solid rgba(16, 185, 129, 0.3);
                border-radius: 6px;
                font-size: 0.75rem;
                color: #10B981;
                font-weight: 600;
            ">ONLINE</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_metric_card(label: str, value: str, subtext: str = "", icon: str = "📊", accent_color: str = "#3B82F6"):
    """Render kartu metrik custom."""
    st.markdown(f"""
    <div style="
        background: #1E293B;
        border: 1px solid #334155;
        border-top: 3px solid {accent_color};
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 12px;
    ">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <div style="font-size:0.75rem; font-weight:600; color:#94A3B8; text-transform:uppercase; letter-spacing:0.5px;">{label}</div>
            <div style="font-size:1.1rem;">{icon}</div>
        </div>
        <div style="font-size:1.6rem; font-weight:800; color:#F8FAFC;">{value}</div>
        {f'<div style="font-size:0.75rem; color:#64748B; margin-top:4px;">{subtext}</div>' if subtext else ''}
    </div>
    """, unsafe_allow_html=True)


def render_risk_gauge(score: int, category: str, color_name: str):
    """Render risk gauge visual."""
    if color_name == "green":
        stroke_color = "#10B981"
        bg_badge = "rgba(16, 185, 129, 0.1)"
    elif color_name == "orange":
        stroke_color = "#F59E0B"
        bg_badge = "rgba(245, 158, 11, 0.1)"
    else:
        stroke_color = "#EF4444"
        bg_badge = "rgba(239, 68, 68, 0.1)"

    emoji = "🟢" if color_name == "green" else ("🟡" if color_name == "orange" else "🔴")

    st.markdown(f"""
    <div style="
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    ">
        <div style="font-size: 0.8rem; font-weight:600; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 12px;">
            Exposure Risk Score
        </div>
        <div style="
            display: inline-block;
            padding: 8px 24px;
            background: {bg_badge};
            border: 1px solid {stroke_color};
            border-radius: 30px;
            margin-bottom: 12px;
        ">
            <span style="font-size: 2.2rem; font-weight: 800; color: {stroke_color};">{score}</span>
            <span style="font-size: 0.9rem; color: #94A3B8;">/100</span>
        </div>
        <div style="font-size: 1.1rem; font-weight: 700; color: {stroke_color};">
            {emoji} {category}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_intel_card(phone_data: Dict):
    """Render kartu profil intelijen nomor target."""
    if not phone_data.get("success"):
        st.error(f"Gagal memparsing nomor: {phone_data.get('error', '-')}")
        return

    is_valid_icon = "✓" if phone_data.get("is_valid") else "!"
    valid_color = "#10B981" if phone_data.get("is_valid") else "#F59E0B"

    st.markdown(f"""
    <div style="
        background: #1E293B;
        border: 1px solid #334155;
        border-left: 4px solid #3B82F6;
        border-radius: 10px;
        padding: 18px;
        margin: 12px 0;
    ">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
            <div>
                <div style="font-size:1.1rem; font-weight:700; color:#F8FAFC; font-family:'JetBrains Mono',monospace;">
                    {phone_data.get('format_e164', phone_data.get('input_original', '-'))}
                </div>
                <div style="font-size:0.75rem; color:#94A3B8;">Phone Intelligence Profile</div>
            </div>
            <div style="padding:4px 10px; background:rgba(255,255,255,0.05); border:1px solid #334155; border-radius:6px; font-size:0.75rem; color:{valid_color}; font-weight:600;">
                {is_valid_icon} {'VALID' if phone_data.get('is_valid') else 'UNVERIFIED'}
            </div>
        </div>
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:8px;">
            {_intel_field('Format Nasional', phone_data.get('format_national', '-'))}
            {_intel_field('Format Internasional', phone_data.get('format_international', '-'))}
            {_intel_field('Operator Provider', phone_data.get('carrier', '-'))}
            {_intel_field('Tipe Jaringan', phone_data.get('network_type', '-'))}
            {_intel_field('Estimasi Wilayah', phone_data.get('region', '-'))}
            {_intel_field('Zona Waktu', phone_data.get('timezone', '-'))}
        </div>
    </div>
    """, unsafe_allow_html=True)


def _intel_field(label: str, value: str) -> str:
    return f"""
    <div style="background:#0F172A; border:1px solid #334155; border-radius:6px; padding:8px 12px;">
        <div style="font-size:0.7rem; color:#94A3B8; margin-bottom:2px;">{label}</div>
        <div style="font-size:0.85rem; font-weight:600; color:#E2E8F0; font-family:'JetBrains Mono',monospace;">{value}</div>
    </div>
    """


def render_breach_card(breach: Dict):
    """Render kartu hasil breach HIBP."""
    from modules.breach_audit import get_severity_from_data_classes, format_pwn_count

    severity = get_severity_from_data_classes(breach.get("data_classes", []))
    if severity == "critical":
        border_color = "#EF4444"
        badge_text = "KRITIS"
    elif severity == "high":
        border_color = "#F59E0B"
        badge_text = "TINGGI"
    else:
        border_color = "#3B82F6"
        badge_text = "SEDANG"

    pwn_formatted = format_pwn_count(breach.get("pwn_count", 0))
    data_chips = "".join([
        f'<span style="background:#0F172A; border:1px solid #334155; color:#CBD5E1; padding:2px 8px; '
        f'border-radius:4px; font-size:0.7rem; margin-right:4px;">{dc}</span>'
        for dc in breach.get("data_classes", [])[:6]
    ])

    st.markdown(f"""
    <div style="
        background: #1E293B;
        border: 1px solid #334155;
        border-left: 3px solid {border_color};
        border-radius: 8px;
        padding: 14px 16px;
        margin: 8px 0;
    ">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <div>
                <span style="font-size:0.95rem; font-weight:700; color:#F8FAFC;">
                    {breach.get('title', 'Unknown Service')}
                </span>
                <span style="font-size:0.78rem; color:#94A3B8; margin-left:8px;">
                    {breach.get('domain', '')}
                </span>
            </div>
            <div style="display:flex; gap:8px; align-items:center;">
                <span style="background:#0F172A; border:1px solid {border_color}; border-radius:4px; padding:2px 8px; font-size:0.7rem; font-weight:600; color:{border_color};">{badge_text}</span>
                <span style="font-size:0.75rem; color:#94A3B8;">Tgl: {breach.get('breach_date', '-')}</span>
                <span style="font-size:0.75rem; color:#E2E8F0; font-weight:600;">{pwn_formatted} akun</span>
            </div>
        </div>
        <div style="margin-top:6px;">{data_chips}</div>
    </div>
    """, unsafe_allow_html=True)


def render_dork_result_card(result: Dict):
    """Render hasil pencarian kueri Dork."""
    risk = result.get("risk", "medium")
    found_count = result.get("found_count", 0)
    items = result.get("result", {}).get("items", [])

    if risk == "critical":
        indicator_color = "#EF4444"
        risk_badge = "KRITIS"
    elif risk == "high":
        indicator_color = "#F59E0B"
        risk_badge = "TINGGI"
    elif risk == "low":
        indicator_color = "#10B981"
        risk_badge = "RENDAH"
    else:
        indicator_color = "#3B82F6"
        risk_badge = "SEDANG"

    status_icon = "⚠️" if found_count > 0 else "✓"
    status_text = f"{found_count} temuan" if found_count > 0 else "Bersih"

    with st.expander(
        f"{status_icon} {result.get('label', 'Query')} | {status_text}",
        expanded=(found_count > 0 and risk in ["critical", "high"]),
    ):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.caption(f"Deskripsi: {result.get('description', '-')}")
            st.code(result.get("query", ""), language="bash")
            direct_url = result.get("direct_url", "")
            if direct_url:
                st.markdown(
                    f'<a href="{direct_url}" target="_blank" style="'
                    f'display:inline-block; padding:5px 14px; margin-top:6px; '
                    f'background:#2563EB; border-radius:6px; color:#FFFFFF; font-size:0.78rem; '
                    f'text-decoration:none; font-weight:600;">'
                    f'Buka Profil Langsung &rarr;</a>',
                    unsafe_allow_html=True,
                )
        with col2:
            st.markdown(f"""
            <div style="text-align:center; padding:8px; background:#0F172A; border:1px solid #334155; border-radius:6px;">
                <div style="font-size:1.4rem; font-weight:800; color:{indicator_color};">{found_count}</div>
                <div style="font-size:0.68rem; color:#94A3B8;">TEMUAN</div>
                <div style="margin-top:2px; font-size:0.7rem; font-weight:700; color:{indicator_color};">{risk_badge}</div>
            </div>
            """, unsafe_allow_html=True)

        result_data = result.get("result", {})
        if not result_data.get("success") and not result_data.get("demo_mode"):
            error_msg = result_data.get("error", "Error tidak diketahui")
            st.warning(f"Info: {error_msg}")

        if items:
            for item in items:
                tags = item.get("intel_tags", [])
                tags_html = ""
                if tags:
                    tags_html = "<div style='margin-top:6px; display:flex; flex-wrap:wrap; gap:4px;'>" + "".join(
                        f'<span style="background:#0F172A; border:1px solid #334155; border-radius:4px; padding:2px 8px; font-size:0.7rem; color:#93C5FD;">{t}</span>'
                        for t in tags
                    ) + "</div>"

                st.markdown(f"""
                <div style="background:#0F172A; border:1px solid #334155; border-radius:6px; padding:10px 12px; margin:6px 0;">
                    <a href="{item.get('url', '#')}" target="_blank" style="color:#60A5FA; font-size:0.88rem; font-weight:600; text-decoration:none;">{item.get('title', 'Tanpa Judul')}</a>
                    <div style="font-size:0.73rem; color:#94A3B8; margin:2px 0;">
                        URL: {item.get('display_url', item.get('url', ''))}
                    </div>
                    <div style="font-size:0.8rem; color:#CBD5E1; margin-top:4px;">
                        {item.get('snippet', '')}
                    </div>
                    {tags_html}
                </div>
                """, unsafe_allow_html=True)


def render_recommendation_card(rec: Dict):
    """Render kartu rekomendasi mitigasi."""
    priority = rec.get("priority", "sedang")
    if priority == "kritis":
        border = "#EF4444"
        badge = "PRIORITAS KRITIS"
    elif priority == "tinggi":
        border = "#F59E0B"
        badge = "PRIORITAS TINGGI"
    else:
        border = "#3B82F6"
        badge = "SEDANG"

    st.markdown(f"""
    <div style="
        background: #1E293B;
        border: 1px solid #334155;
        border-left: 3px solid {border};
        border-radius: 8px;
        padding: 14px;
        margin: 8px 0;
    ">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
            <div style="font-size:0.95rem; font-weight:700; color:#F8FAFC;">
                {rec.get('icon','')} {rec.get('title', '')}
            </div>
            <span style="font-size:0.7rem; color:{border}; background:#0F172A; border:1px solid {border}; padding:2px 8px; border-radius:4px; font-weight:600;">{badge}</span>
        </div>
        <div style="font-size:0.83rem; color:#94A3B8; line-height:1.5;">
            {rec.get('detail', '')}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_emergency_banner():
    """Banner panduan darurat pinjol."""
    st.markdown("""
    <div style="
        background: #1E293B;
        border: 1px solid #EF4444;
        border-radius: 10px;
        padding: 18px 20px;
        margin: 12px 0;
    ">
        <div style="font-size:1.05rem; font-weight:700; color:#EF4444; margin-bottom:12px;">
            Panduan Darurat Teror Pinjol Ilegal
        </div>
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap: 12px;">
            <div style="background:#0F172A; padding:12px; border-radius:6px; border:1px solid #334155;">
                <div style="font-weight:600; color:#F8FAFC; margin-bottom:4px;">Blokir & Amankan</div>
                <div style="font-size:0.8rem; color:#94A3B8; line-height:1.5;">
                    &bull; Blokir nomor DC di aplikasi telepon<br>
                    &bull; Cabut izin aplikasi pinjol (Kontak, Gambar)<br>
                    &bull; Tangkap layar (screenshot) semua teror
                </div>
            </div>
            <div style="background:#0F172A; padding:12px; border-radius:6px; border:1px solid #334155;">
                <div style="font-weight:600; color:#F8FAFC; margin-bottom:4px;">Hubungi Layanan Resmi</div>
                <div style="font-size:0.8rem; color:#94A3B8; line-height:1.5;">
                    &bull; Kontak OJK: <strong>157</strong> (Bebas Pulsa)<br>
                    &bull; Bareskrim Polri: <strong>0800-1000-00</strong><br>
                    &bull; LBH Jakarta: 021-3145-518
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_api_status_sidebar(status: Dict):
    """Render status API di sidebar."""
    st.sidebar.markdown("### Status API")
    for name, is_active in status.items():
        icon = "✓" if is_active else "✗"
        label = "Aktif" if is_active else "Belum Konfigurasi"
        color = "#10B981" if is_active else "#EF4444"
        st.sidebar.markdown(f"<span style='color:{color}; font-weight:600;'>{icon} {name}</span>: {label}", unsafe_allow_html=True)


def status_badge_html(status: str) -> str:
    """Hasilkan HTML badge status berwarna."""
    s = (status or "").lower()
    if s in ("selesai", "generated", "done", "success"):
        color = "#10B981"
        label = "Selesai"
    elif s in ("pending", "draft", "proses", "penanganan"):
        color = "#F59E0B"
        label = "Proses"
    elif s in ("error", "gagal", "failed"):
        color = "#EF4444"
        label = "Gagal"
    else:
        color = "#3B82F6"
        label = status or "Aktif"
    return f'<span style="background:#0F172A; border:1px solid {color}; color:{color}; padding:2px 8px; border-radius:4px; font-size:0.72rem; font-weight:600;">{label}</span>'


def risk_badge_html(score: int) -> str:
    """Badge risk score berwarna."""
    if score >= 70:
        color = "#EF4444"
    elif score >= 40:
        color = "#F59E0B"
    else:
        color = "#10B981"
    return f'<span style="background:#0F172A; border:1px solid {color}; color:{color}; padding:2px 8px; border-radius:4px; font-size:0.72rem; font-weight:600;">Risk: {score}/100</span>'


def render_scan_history_row(row: dict, idx: int):
    """Render satu baris riwayat scan dengan tombol aksi."""
    risk_score = row.get("risk_score", 0)
    target = row.get("target_name", "-")
    phone = row.get("target_phone", "") or "-"
    email = row.get("target_email", "") or "-"
    ts = row.get("created_at", "-")
    status = row.get("status", "selesai")
    dork_found = row.get("dork_found", 0)
    breach = row.get("breach_count", 0)
    scan_id = row.get("id", 0)
    notes = row.get("notes", "") or ""

    badge_html = status_badge_html(status)
    risk_html = risk_badge_html(risk_score)

    st.markdown(f"""
    <div style="
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 14px 16px;
        margin: 6px 0;
    ">
        <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:8px;">
            <div>
                <div style="font-weight:700; color:#F8FAFC; font-size:0.95rem;">{target}</div>
                <div style="font-size:0.75rem; color:#94A3B8; margin-top:2px;">
                    HP: {phone} | Email: {email}
                </div>
            </div>
            <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
                {risk_html}
                {badge_html}
                <span style="font-size:0.72rem; color:#64748B;">{ts}</span>
                <span style="font-size:0.72rem; color:#94A3B8;">
                    Dork: {dork_found} | Breach: {breach}
                </span>
            </div>
        </div>
        {f'<div style="margin-top:6px; font-size:0.78rem; color:#94A3B8; font-style:italic;">Catatan: {notes}</div>' if notes else ''}
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    with col2:
        detail_key = f"detail_scan_{scan_id}_{idx}"
        if st.button("Detail", key=detail_key, use_container_width=True):
            st.session_state[f"show_scan_detail_{scan_id}"] = not st.session_state.get(f"show_scan_detail_{scan_id}", False)
    with col3:
        reprocess_key = f"reprocess_scan_{scan_id}_{idx}"
        if st.button("Ulang", key=reprocess_key, use_container_width=True):
            st.session_state["reprocess_scan_data"] = row
            st.session_state["active_tab_goto"] = "diagnosa"
            st.rerun()
    with col4:
        delete_key = f"delete_scan_{scan_id}_{idx}"
        if st.button("Hapus", key=delete_key, use_container_width=True):
            st.session_state[f"confirm_delete_scan_{scan_id}"] = True

    if st.session_state.get(f"confirm_delete_scan_{scan_id}"):
        st.warning(f"Konfirmasi hapus riwayat scan untuk target {target}?")
        cc1, cc2 = st.columns(2)
        with cc1:
            if st.button("Ya, Hapus", key=f"confirm_yes_scan_{scan_id}_{idx}"):
                from modules import database as db
                db.delete_scan(scan_id)
                del st.session_state[f"confirm_delete_scan_{scan_id}"]
                st.rerun()
        with cc2:
            if st.button("Batal", key=f"confirm_no_scan_{scan_id}_{idx}"):
                del st.session_state[f"confirm_delete_scan_{scan_id}"]
                st.rerun()

    if st.session_state.get(f"show_scan_detail_{scan_id}"):
        from modules import database as db
        detail = db.get_scan_detail(scan_id)
        with st.expander(f"Detail Scan #{scan_id} - {target}", expanded=True):
            d1, d2, d3 = st.columns(3)
            with d1:
                st.markdown(f"**Target:** {target}")
                st.markdown(f"**HP:** {detail.get('target_phone','-') or '-'}")
                st.markdown(f"**Email:** {detail.get('target_email','-') or '-'}")
            with d2:
                st.markdown(f"**Risk Score:** {risk_score}/100")
                st.markdown(f"**Kategori:** {detail.get('risk_category','-')}")
                st.markdown(f"**Mode Scan:** {detail.get('scan_mode','-')}")
            with d3:
                st.markdown(f"**Dork Temuan:** {dork_found}")
                st.markdown(f"**Breach:** {breach}")
                st.markdown(f"**Tanggal:** {ts}")

            ig = detail.get("target_instagram","") or "-"
            tiktok = detail.get("target_tiktok","") or "-"
            fb = detail.get("target_facebook","") or "-"
            tw = detail.get("target_twitter","") or "-"
            li = detail.get("target_linkedin","") or "-"
            st.caption(f"Social Media: IG: {ig} | TikTok: {tiktok} | FB: {fb} | Twitter: {tw} | LinkedIn: {li}")

            st.markdown("---")
            new_notes = st.text_area("Catatan", value=notes, key=f"notes_scan_{scan_id}_{idx}", height=60)
            if st.button("Simpan Catatan", key=f"save_notes_scan_{scan_id}_{idx}"):
                db.update_scan_notes(scan_id, new_notes)
                st.success("Catatan disimpan!")
                st.rerun()


def render_dc_history_row(row: dict, idx: int):
    """Render satu baris riwayat investigasi DC."""
    dc_phone = row.get("dc_phone", "-")
    operator = row.get("operator", "-") or "-"
    region = row.get("region", "-") or "-"
    truecaller = row.get("truecaller_name", "-") or "-"
    is_spam = bool(row.get("is_spam", 0))
    gc_count = row.get("getcontact_count", 0)
    has_fraud = bool(row.get("has_fraud_report", 0))
    phone_score = row.get("phone_score", 0)
    ts = row.get("created_at", "-")
    status = row.get("status", "selesai")
    dc_id = row.get("id", 0)
    notes = row.get("notes", "") or ""

    badge_html = status_badge_html(status)
    spam_badge = '<span style="background:#0F172A; border:1px solid #EF4444; color:#EF4444; padding:2px 8px; border-radius:4px; font-size:0.72rem; font-weight:600;">SPAM</span>' if is_spam else '<span style="background:#0F172A; border:1px solid #10B981; color:#10B981; padding:2px 8px; border-radius:4px; font-size:0.72rem; font-weight:600;">Normal</span>'

    st.markdown(f"""
    <div style="
        background: #1E293B;
        border: 1px solid #334155;
        border-left: 3px solid {'#EF4444' if is_spam or has_fraud else '#3B82F6'};
        border-radius: 8px;
        padding: 14px 16px;
        margin: 6px 0;
    ">
        <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:8px;">
            <div>
                <div style="font-weight:700; color:#F8FAFC; font-size:0.95rem; font-family:'JetBrains Mono',monospace;">{dc_phone}</div>
                <div style="font-size:0.75rem; color:#94A3B8; margin-top:2px;">
                    Operator: {operator} | Wilayah: {region} | Truecaller: {truecaller}
                </div>
            </div>
            <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
                {spam_badge}
                {risk_badge_html(phone_score)}
                {badge_html}
                <span style="font-size:0.72rem; color:#64748B;">{ts}</span>
            </div>
        </div>
        {f'<div style="margin-top:6px; font-size:0.78rem; color:#94A3B8; font-style:italic;">Catatan: {notes}</div>' if notes else ''}
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([3, 1, 1])
    with col2:
        if st.button("Detail", key=f"detail_dc_{dc_id}_{idx}", use_container_width=True):
            st.session_state[f"show_dc_detail_{dc_id}"] = not st.session_state.get(f"show_dc_detail_{dc_id}", False)
    with col3:
        if st.button("Hapus", key=f"delete_dc_{dc_id}_{idx}", use_container_width=True):
            st.session_state[f"confirm_delete_dc_{dc_id}"] = True

    if st.session_state.get(f"confirm_delete_dc_{dc_id}"):
        st.warning(f"Yakin hapus investigasi nomor DC {dc_phone}?")
        cc1, cc2 = st.columns(2)
        with cc1:
            if st.button("Ya, Hapus", key=f"confirm_yes_dc_{dc_id}_{idx}"):
                from modules import database as db
                db.delete_dc(dc_id)
                del st.session_state[f"confirm_delete_dc_{dc_id}"]
                st.rerun()
        with cc2:
            if st.button("Batal", key=f"confirm_no_dc_{dc_id}_{idx}"):
                del st.session_state[f"confirm_delete_dc_{dc_id}"]
                st.rerun()

    if st.session_state.get(f"show_dc_detail_{dc_id}"):
        from modules import database as db
        detail = db.get_dc_detail(dc_id)
        with st.expander(f"Detail Investigasi DC #{dc_id} - {dc_phone}", expanded=True):
            d1, d2, d3 = st.columns(3)
            with d1:
                st.markdown(f"**Nomor DC:** `{dc_phone}`")
                st.markdown(f"**Operator:** {operator}")
                st.markdown(f"**Wilayah:** {region}")
            with d2:
                st.markdown(f"**Truecaller:** {truecaller}")
                st.markdown(f"**Status Spam:** {'Ya' if is_spam else 'Tidak'}")
            with d3:
                st.markdown(f"**GetContact Tags:** {gc_count}")
                st.markdown(f"**Phone Score:** {phone_score}/100")
                st.markdown(f"**Tanggal:** {ts}")


def render_removal_history_row(row: dict, idx: int):
    """Render satu baris riwayat removal request."""
    rm_id = row.get("id", 0)
    target_name = row.get("target_name", "-") or "-"
    target_url = row.get("target_url", "-") or "-"
    removal_type = row.get("removal_type", "-") or "-"
    status = row.get("status", "draft")
    ts = row.get("created_at", "-")
    notes = row.get("notes", "") or ""

    badge_html = status_badge_html(status)

    st.markdown(f"""
    <div style="
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 14px 16px;
        margin: 6px 0;
    ">
        <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:8px;">
            <div>
                <div style="font-weight:700; color:#F8FAFC; font-size:0.92rem;">{target_name}</div>
                <div style="font-size:0.75rem; color:#94A3B8; margin-top:2px;">
                    URL: {target_url[:70]}{'...' if len(target_url) > 70 else ''}
                </div>
                <div style="font-size:0.72rem; color:#64748B; margin-top:2px;">Tipe: {removal_type}</div>
            </div>
            <div style="display:flex; align-items:center; gap:8px;">
                {badge_html}
                <span style="font-size:0.72rem; color:#64748B;">{ts}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    with col2:
        status_options = ["draft", "terkirim", "diproses", "selesai", "ditolak"]
        new_status = st.selectbox("Status", status_options,
                                  index=status_options.index(status) if status in status_options else 0,
                                  key=f"status_rm_{rm_id}_{idx}", label_visibility="collapsed")
    with col3:
        if st.button("Update", key=f"update_rm_{rm_id}_{idx}", use_container_width=True):
            from modules import database as db
            db.update_removal_status(rm_id, new_status, notes)
            st.success("Status diperbarui!")
            st.rerun()
    with col4:
        if st.button("Hapus", key=f"delete_rm_{rm_id}_{idx}", use_container_width=True):
            from modules import database as db
            db.delete_removal(rm_id)
            st.rerun()


def render_police_report_history_row(row: dict, idx: int):
    """Render satu baris riwayat laporan polisi."""
    rp_id = row.get("id", 0)
    reporter = row.get("reporter_name", "-") or "-"
    dc_phone = row.get("dc_phone", "-") or "-"
    filename = row.get("filename", "-") or "-"
    status = row.get("status", "generated")
    ts = row.get("created_at", "-")
    summary = row.get("incident_summary", "") or ""

    badge_html = status_badge_html(status)

    st.markdown(f"""
    <div style="
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 14px 16px;
        margin: 6px 0;
    ">
        <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:8px;">
            <div>
                <div style="font-weight:700; color:#F8FAFC; font-size:0.92rem;">Pelapor: {reporter}</div>
                <div style="font-size:0.75rem; color:#94A3B8; margin-top:2px;">
                    DC: {dc_phone} | File: {filename}
                </div>
            </div>
            <div style="display:flex; align-items:center; gap:8px;">
                {badge_html}
                <span style="font-size:0.72rem; color:#64748B;">{ts}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button("Hapus", key=f"delete_rp_{rp_id}_{idx}", use_container_width=True):
            from modules import database as db
            db.delete_police_report(rp_id)
            st.rerun()
