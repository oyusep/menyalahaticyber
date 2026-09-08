"""
OSINT Cyber Guardian - PDF Report Generator
Membuat laporan polisi resmi menggunakan ReportLab
"""
import io
from datetime import datetime
from typing import Dict, List, Optional

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    PageBreak,
    KeepTogether,
)
from reportlab.platypus.flowables import HRFlowable


# ─── Warna tema ───────────────────────────────────────────────
COLOR_DARK_BLUE = colors.HexColor("#1A237E")
COLOR_MED_BLUE = colors.HexColor("#283593")
COLOR_ACCENT = colors.HexColor("#1565C0")
COLOR_RED = colors.HexColor("#C62828")
COLOR_LIGHT_GREY = colors.HexColor("#F5F5F5")
COLOR_MID_GREY = colors.HexColor("#BDBDBD")
COLOR_TABLE_HEADER = colors.HexColor("#1A237E")
COLOR_ROW_ALT = colors.HexColor("#E8EAF6")


def _build_styles():
    """Bangun style sheet kustom."""
    styles = getSampleStyleSheet()
    custom = {
        "KopTitle": ParagraphStyle(
            "KopTitle",
            parent=styles["Title"],
            fontSize=14,
            leading=18,
            textColor=COLOR_DARK_BLUE,
            alignment=TA_CENTER,
            fontName="Helvetica-Bold",
            spaceAfter=2,
        ),
        "KopSubtitle": ParagraphStyle(
            "KopSubtitle",
            parent=styles["Normal"],
            fontSize=10,
            textColor=COLOR_MED_BLUE,
            alignment=TA_CENTER,
            fontName="Helvetica",
            spaceAfter=4,
        ),
        "SectionHeader": ParagraphStyle(
            "SectionHeader",
            parent=styles["Heading2"],
            fontSize=11,
            textColor=colors.white,
            fontName="Helvetica-Bold",
            spaceAfter=6,
            spaceBefore=12,
            leftIndent=0,
        ),
        "BodyText": ParagraphStyle(
            "BodyText",
            parent=styles["Normal"],
            fontSize=9.5,
            leading=14,
            textColor=colors.HexColor("#212121"),
            alignment=TA_JUSTIFY,
            fontName="Helvetica",
        ),
        "LabelBold": ParagraphStyle(
            "LabelBold",
            parent=styles["Normal"],
            fontSize=9,
            fontName="Helvetica-Bold",
            textColor=COLOR_DARK_BLUE,
        ),
        "SmallText": ParagraphStyle(
            "SmallText",
            parent=styles["Normal"],
            fontSize=8,
            textColor=colors.HexColor("#757575"),
        ),
        "RedWarning": ParagraphStyle(
            "RedWarning",
            parent=styles["Normal"],
            fontSize=9,
            fontName="Helvetica-Bold",
            textColor=COLOR_RED,
            alignment=TA_CENTER,
        ),
        "TableCell": ParagraphStyle(
            "TableCell",
            parent=styles["Normal"],
            fontSize=8.5,
            leading=12,
            fontName="Helvetica",
        ),
        "TableCellBold": ParagraphStyle(
            "TableCellBold",
            parent=styles["Normal"],
            fontSize=8.5,
            leading=12,
            fontName="Helvetica-Bold",
        ),
    }
    return styles, custom


def _section_header_block(title: str, styles_custom: dict):
    """Buat blok header seksi berwarna biru."""
    return [
        Table(
            [[Paragraph(f"  {title}", styles_custom["SectionHeader"])]],
            colWidths=[17 * cm],
            style=TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), COLOR_TABLE_HEADER),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ]),
        ),
        Spacer(1, 4),
    ]


def _kv_table(data: List[tuple], styles_custom: dict, col_widths=None) -> Table:
    """Buat tabel key-value untuk data identitas."""
    if col_widths is None:
        col_widths = [5 * cm, 12 * cm]

    table_data = []
    for i, (key, val) in enumerate(data):
        table_data.append([
            Paragraph(key, styles_custom["LabelBold"]),
            Paragraph(str(val) if val else "-", styles_custom["TableCell"]),
        ])

    style = TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, COLOR_MID_GREY),
        ("BACKGROUND", (0, 0), (0, -1), COLOR_LIGHT_GREY),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ])

    # Warna baris alternating pada nilai
    for i in range(len(table_data)):
        if i % 2 == 1:
            style.add("BACKGROUND", (1, i), (1, i), COLOR_ROW_ALT)

    return Table(table_data, colWidths=col_widths, style=style)


def _evidence_table(screenshots_info: List[Dict], styles_custom: dict) -> Table:
    """Tabel daftar bukti."""
    headers = ["No.", "Jenis Bukti", "Deskripsi", "Tanggal Upload"]
    rows = [headers]
    for i, info in enumerate(screenshots_info, 1):
        rows.append([
            str(i),
            info.get("type", "Tangkapan Layar"),
            info.get("description", info.get("name", "Bukti digital")),
            info.get("date", datetime.now().strftime("%d/%m/%Y")),
        ])

    style = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), COLOR_TABLE_HEADER),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("GRID", (0, 0), (-1, -1), 0.5, COLOR_MID_GREY),
        ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, COLOR_ROW_ALT]),
    ])

    return Table(rows, colWidths=[1 * cm, 3.5 * cm, 8.5 * cm, 4 * cm], style=style)


def _bts_request_table(phone_profile: Dict, styles_custom: dict) -> Table:
    """Tabel permohonan data teknis CDR/Cell-ID."""
    headers = ["No.", "Data yang Dimohon", "Keterangan"]
    rows = [
        headers,
        ["1", "Call Detail Record (CDR)", "Riwayat panggilan masuk/keluar dan SMS periode teror"],
        ["2", "Cell ID / BTS Location", "Lokasi BTS aktif saat komunikasi teror berlangsung"],
        ["3", "IMEI History", "Riwayat perangkat yang menggunakan nomor telepon target"],
        ["4", "Subscriber Data", "Data pendaftaran (KTP, nama pemilik SIM card) dari operator"],
        ["5", "IP Address Log", "Log koneksi data internet (WhatsApp, Telegram) bila tersedia"],
        ["6", "Roaming History", "Riwayat perpindahan wilayah jaringan selama periode investigasi"],
    ]

    style = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), COLOR_RED),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("GRID", (0, 0), (-1, -1), 0.5, COLOR_MID_GREY),
        ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, COLOR_ROW_ALT]),
    ])

    return Table(rows, colWidths=[1 * cm, 6 * cm, 10 * cm], style=style)


def generate_police_report(
    # Identitas Pelapor
    reporter_name: str,
    reporter_nik: str,
    reporter_phone: str,
    reporter_address: str,
    # Data DC / Pelaku
    dc_phone_raw: str,
    phone_profile: Dict,
    # Kronologi
    incident_summary: str,
    terror_messages: str,
    # Bukti
    uploaded_files_info: List[Dict] = None,
    # Meta
    report_date: str = None,
    case_number: str = None,
) -> bytes:
    """
    Generate laporan polisi PDF.

    Returns:
        bytes PDF siap download
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        title="Laporan Pengaduan Pinjaman Online Ilegal",
        author="Menyalahati Cyber Intelligence",
    )

    styles, custom = _build_styles()
    uploaded_files_info = uploaded_files_info or []
    report_date = report_date or datetime.now().strftime("%d %B %Y")
    case_number = case_number or f"OCG-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    story = []

    # ── HEADER / KOP ─────────────────────────────────────────
    story.append(Paragraph("LAPORAN PENGADUAN TINDAK PIDANA", custom["KopTitle"]))
    story.append(Paragraph("Pinjaman Online Ilegal, Ancaman & Teror Siber", custom["KopSubtitle"]))
    story.append(HRFlowable(width="100%", thickness=3, color=COLOR_DARK_BLUE, spaceAfter=4))
    story.append(HRFlowable(width="100%", thickness=1, color=COLOR_ACCENT, spaceAfter=8))

    # Nomor laporan & tanggal
    meta_data = [
        [
            Paragraph("No. Dokumen:", custom["LabelBold"]),
            Paragraph(case_number, custom["BodyText"]),
            Paragraph("Tanggal:", custom["LabelBold"]),
            Paragraph(report_date, custom["BodyText"]),
        ]
    ]
    story.append(
        Table(
            meta_data,
            colWidths=[3.5 * cm, 5 * cm, 2.5 * cm, 6 * cm],
            style=TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), COLOR_LIGHT_GREY),
                ("GRID", (0, 0), (-1, -1), 0.5, COLOR_MID_GREY),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ]),
        )
    )
    story.append(Spacer(1, 10))

    # ── BAGIAN 1: IDENTITAS PELAPOR ──────────────────────────
    story += _section_header_block("I. IDENTITAS PELAPOR", custom)
    story.append(
        _kv_table([
            ("Nama Lengkap", reporter_name or "-"),
            ("NIK / No. KTP", reporter_nik or "-"),
            ("Nomor HP Aktif", reporter_phone or "-"),
            ("Alamat Domisili", reporter_address or "-"),
            ("Status", "Korban Pinjaman Online Ilegal"),
        ], custom)
    )
    story.append(Spacer(1, 10))

    # ── BAGIAN 2: PROFIL INTELIJEN NOMOR DC ──────────────────
    story += _section_header_block("II. PROFIL INTELIJEN NOMOR PELAKU / DC", custom)

    if phone_profile.get("success"):
        story.append(
            _kv_table([
                ("Input Nomor", dc_phone_raw or "-"),
                ("Format E.164", phone_profile.get("format_e164", "-")),
                ("Format Nasional", phone_profile.get("format_national", "-")),
                ("Format Internasional", phone_profile.get("format_international", "-")),
                ("Kode Negara", phone_profile.get("country_code", "-")),
                ("Negara", phone_profile.get("country", "-")),
                ("Operator / Provider", phone_profile.get("carrier", "-")),
                ("Prefix (4 digit)", phone_profile.get("prefix_4digit", "-")),
                ("Tipe Jaringan", phone_profile.get("network_type", "-")),
                ("Estimasi Wilayah", phone_profile.get("region", "-")),
                ("Zona Waktu", phone_profile.get("timezone", "-")),
                ("Status Validitas", "VALID ✓" if phone_profile.get("is_valid") else "Perlu Verifikasi"),
            ], custom)
        )
    else:
        story.append(Paragraph(
            f"⚠ Tidak dapat memparsing nomor: {phone_profile.get('error', 'Nomor tidak valid')}",
            custom["RedWarning"]
        ))
    story.append(Spacer(1, 10))

    # ── BAGIAN 3: KRONOLOGI KEJADIAN ─────────────────────────
    story += _section_header_block("III. KRONOLOGI & NARASI KEJADIAN", custom)
    story.append(Paragraph(
        "Dengan ini Pelapor menyatakan bahwa telah menjadi korban tindakan teror, ancaman, "
        "intimidasi, dan/atau penyebaran informasi hoaks yang dilakukan oleh oknum pinjaman online "
        "ilegal (Pinjol Ilegal), dengan kronologi sebagai berikut:",
        custom["BodyText"],
    ))
    story.append(Spacer(1, 6))

    if incident_summary:
        box_data = [[Paragraph(incident_summary, custom["BodyText"])]]
        story.append(
            Table(
                box_data,
                colWidths=[17 * cm],
                style=TableStyle([
                    ("BACKGROUND", (0, 0), (-1, -1), COLOR_LIGHT_GREY),
                    ("GRID", (0, 0), (-1, -1), 1, COLOR_ACCENT),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ("LEFTPADDING", (0, 0), (-1, -1), 10),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ]),
            )
        )
    story.append(Spacer(1, 8))

    # Pesan teror
    if terror_messages:
        story.append(Paragraph("Contoh Pesan / Bukti Teror:", custom["LabelBold"]))
        story.append(Spacer(1, 4))
        box_data = [[Paragraph(terror_messages.replace("\n", "<br/>"), custom["BodyText"])]]
        story.append(
            Table(
                box_data,
                colWidths=[17 * cm],
                style=TableStyle([
                    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFF3E0")),
                    ("GRID", (0, 0), (-1, -1), 1, COLOR_RED),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ("LEFTPADDING", (0, 0), (-1, -1), 10),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ]),
            )
        )
    story.append(Spacer(1, 10))

    # ── BAGIAN 4: DAFTAR BUKTI ───────────────────────────────
    story += _section_header_block("IV. DAFTAR ALAT BUKTI ELEKTRONIK", custom)
    if uploaded_files_info:
        story.append(_evidence_table(uploaded_files_info, custom))
    else:
        story.append(Paragraph(
            "Bukti tangkapan layar (screenshot) dan rekaman percakapan tersimpan pada perangkat "
            "Pelapor dan akan diserahkan kepada penyidik.",
            custom["BodyText"],
        ))
    story.append(Spacer(1, 10))

    # ── BAGIAN 5: PASAL YANG DILANGGAR ───────────────────────
    story += _section_header_block("V. DUGAAN TINDAK PIDANA", custom)
    pasal_data = [
        ["No.", "Pasal", "Uraian Pelanggaran"],
        ["1", "UU ITE No.19/2016 Pasal 27 ayat (3)", "Penghinaan/pencemaran nama baik melalui media elektronik"],
        ["2", "UU ITE No.19/2016 Pasal 29", "Pengiriman informasi elektronik yang mengandung ancaman kekerasan"],
        ["3", "KUHP Pasal 335", "Perbuatan tidak menyenangkan / ancaman (penghinaan)"],
        ["4", "KUHP Pasal 368", "Pemerasan dengan ancaman"],
        ["5", "UU No.4/2023 (POJK)", "Penyelenggaraan pinjaman online tanpa izin OJK"],
        ["6", "UU No.27/2022 (PDP)", "Pemrosesan data pribadi tanpa persetujuan (akses kontak HP)"],
    ]
    pasal_style = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), COLOR_TABLE_HEADER),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, COLOR_MID_GREY),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, COLOR_ROW_ALT]),
    ])
    story.append(Table(pasal_data, colWidths=[1 * cm, 7 * cm, 9 * cm], style=pasal_style))
    story.append(Spacer(1, 10))

    # ── BAGIAN 6: PERMOHONAN DATA TEKNIS ─────────────────────
    story.append(PageBreak())
    story += _section_header_block("VI. PERMOHONAN DATA TEKNIS (CDR / CELL-ID)", custom)
    story.append(Paragraph(
        "Dalam rangka penyidikan perkara ini, Pelapor memohon kepada Penyidik Siber yang berwenang "
        "untuk melakukan permohonan resmi kepada operator telekomunikasi guna mendapatkan data teknis "
        "sebagai berikut:",
        custom["BodyText"],
    ))
    story.append(Spacer(1, 6))
    story.append(_bts_request_table(phone_profile, custom))
    story.append(Spacer(1, 8))

    # Info operator
    if phone_profile.get("success"):
        story.append(Paragraph(
            f"Permohonan ditujukan kepada: <b>{phone_profile.get('carrier', 'Operator Terkait')}</b> "
            f"- Nomor target: <b>{phone_profile.get('format_e164', dc_phone_raw)}</b>",
            custom["BodyText"],
        ))

    story.append(Spacer(1, 8))
    legal_box = [[Paragraph(
        "Dasar Hukum Permintaan Data Teknis:<br/>"
        "• UU No. 19 Tahun 2016 tentang ITE - Pasal 43: kewenangan penyidik meminta data elektronik<br/>"
        "• UU No. 36 Tahun 1999 tentang Telekomunikasi - Pasal 42: kewajiban operator memberi data untuk kepentingan hukum<br/>"
        "• KUHAP Pasal 7 ayat (1) huruf j: kewenangan penyidik dalam penyidikan<br/>"
        "• Peraturan Pemerintah No. 52 Tahun 2000 tentang Penyelenggaraan Telekomunikasi",
        custom["SmallText"],
    )]]
    story.append(
        Table(legal_box, colWidths=[17 * cm], style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), COLOR_ROW_ALT),
            ("GRID", (0, 0), (-1, -1), 0.5, COLOR_ACCENT),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ]))
    )
    story.append(Spacer(1, 16))

    # ── BAGIAN 7: TANDA TANGAN ───────────────────────────────
    story += _section_header_block("VII. PERNYATAAN & TANDA TANGAN", custom)
    story.append(Paragraph(
        "Dengan ini saya menyatakan bahwa keterangan yang saya sampaikan dalam laporan ini adalah "
        "BENAR adanya dan dapat saya pertanggungjawabkan secara hukum.",
        custom["BodyText"],
    ))
    story.append(Spacer(1, 16))

    sign_data = [
        [
            Paragraph(f"Hormat Pelapor,\n\n\n\n\n({reporter_name or '...........................'})\nPelapor", custom["BodyText"]),
            Paragraph(f"{report_date}\n\n\n\n\n(...........................)\nPenerima Laporan / Penyidik", custom["BodyText"]),
        ]
    ]
    story.append(
        Table(sign_data, colWidths=[8.5 * cm, 8.5 * cm], style=TableStyle([
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
            ("GRID", (0, 0), (-1, -1), 0.5, COLOR_MID_GREY),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ]))
    )
    story.append(Spacer(1, 16))

    # ── FOOTER ───────────────────────────────────────────────
    story.append(HRFlowable(width="100%", thickness=1, color=COLOR_ACCENT))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "Dokumen ini dibuat oleh Menyalahati Cyber Intelligence - Anti Doxing & DC Profiler | "
        "Laporan hanya sah bila ditandatangani di hadapan penyidik yang berwenang. | "
        f"Dibuat: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} WIB",
        custom["SmallText"],
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer.read()
