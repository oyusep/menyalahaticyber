"""
OSINT Cyber Guardian - Phone Number Profiler
Menggunakan libphonenumber untuk parsing dan intelijen nomor telepon Indonesia
"""
import phonenumbers
from phonenumbers import geocoder, carrier, timezone, PhoneNumberType
from typing import Dict, Optional


# Mapping prefix nomor HP Indonesia ke operator
INDONESIA_CARRIER_MAP = {
    # Telkomsel
    "0811": "Telkomsel (Halo)",
    "0812": "Telkomsel (Simpati)",
    "0813": "Telkomsel (Simpati)",
    "0821": "Telkomsel (As/Loop)",
    "0822": "Telkomsel (As)",
    "0823": "Telkomsel (As)",
    "0851": "Telkomsel (As)",
    "0852": "Telkomsel (Simpati)",
    "0853": "Telkomsel (Simpati)",
    # Indosat Ooredoo Hutchison
    "0814": "Indosat (Matrix)",
    "0815": "Indosat (Mentari)",
    "0816": "Indosat (Mentari)",
    "0855": "Indosat (IM3)",
    "0856": "Indosat (IM3 Ooredoo)",
    "0857": "Indosat (IM3 Ooredoo)",
    "0858": "Indosat (IM3 Ooredoo)",
    # XL Axiata
    "0817": "XL Axiata (XL)",
    "0818": "XL Axiata (XL)",
    "0819": "XL Axiata (XL)",
    "0859": "XL Axiata (XL)",
    "0877": "XL Axiata (XL)",
    "0878": "XL Axiata (XL)",
    # Axis (XL Axiata)
    "0831": "Axis (XL Axiata)",
    "0832": "Axis (XL Axiata)",
    "0833": "Axis (XL Axiata)",
    "0838": "Axis (XL Axiata)",
    # Smartfren
    "0881": "Smartfren",
    "0882": "Smartfren",
    "0883": "Smartfren",
    "0884": "Smartfren",
    "0885": "Smartfren",
    "0886": "Smartfren",
    "0887": "Smartfren",
    "0888": "Smartfren",
    "0889": "Smartfren",
    # Tri (3)
    "0895": "Tri (3 / Hutchison)",
    "0896": "Tri (3 / Hutchison)",
    "0897": "Tri (3 / Hutchison)",
    "0898": "Tri (3 / Hutchison)",
    "0899": "Tri (3 / Hutchison)",
    # By.U (Telkomsel Digital)
    "0851": "By.U / Telkomsel",
}

# Mapping wilayah berdasarkan kode area telepon rumah Indonesia
INDONESIA_AREA_CODE_MAP = {
    "021": "DKI Jakarta",
    "022": "Bandung, Jawa Barat",
    "024": "Semarang, Jawa Tengah",
    "031": "Surabaya, Jawa Timur",
    "061": "Medan, Sumatera Utara",
    "0411": "Makassar, Sulawesi Selatan",
    "0274": "Yogyakarta",
    "0341": "Malang, Jawa Timur",
    "0231": "Cirebon, Jawa Barat",
}

NETWORK_TYPE_MAP = {
    PhoneNumberType.MOBILE: "Telepon Seluler (Mobile)",
    PhoneNumberType.FIXED_LINE: "Telepon Rumah (Fixed Line)",
    PhoneNumberType.FIXED_LINE_OR_MOBILE: "Seluler / Rumah",
    PhoneNumberType.TOLL_FREE: "Bebas Pulsa (Toll Free)",
    PhoneNumberType.PREMIUM_RATE: "Premium Rate",
    PhoneNumberType.SHARED_COST: "Shared Cost",
    PhoneNumberType.VOIP: "VoIP / Internet",
    PhoneNumberType.UNKNOWN: "Tidak Diketahui",
}


def normalize_phone(phone_input: str) -> str:
    """Normalisasi format nomor HP Indonesia ke format standar."""
    phone = phone_input.strip().replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    if phone.startswith("08"):
        phone = "+62" + phone[1:]
    elif phone.startswith("8") and len(phone) >= 9:
        phone = "+62" + phone
    elif phone.startswith("62"):
        phone = "+" + phone
    return phone


def get_carrier_from_prefix(phone_local: str) -> str:
    """Cari operator berdasarkan 4 digit prefix."""
    if phone_local.startswith("0"):
        prefix4 = phone_local[:4]
        return INDONESIA_CARRIER_MAP.get(prefix4, "Operator Tidak Dikenali")
    return "Tidak Diketahui"


def profile_phone_number(phone_input: str) -> Dict:
    """
    Profil lengkap nomor telepon.
    
    Returns:
        dict berisi info format, operator, wilayah, dll.
    """
    if not phone_input or len(phone_input.strip()) < 8:
        return {"success": False, "error": "Nomor telepon terlalu pendek atau kosong"}

    normalized = normalize_phone(phone_input)

    try:
        parsed = phonenumbers.parse(normalized, "ID")
    except phonenumbers.NumberParseException as e:
        # Fallback: coba parse langsung
        try:
            parsed = phonenumbers.parse(phone_input, "ID")
        except:
            return {"success": False, "error": f"Nomor tidak dapat diparsing: {str(e)}"}

    is_valid = phonenumbers.is_valid_number(parsed)
    is_possible = phonenumbers.is_possible_number(parsed)

    # Format output
    e164 = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
    national = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)
    international = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)

    # Deteksi operator via phonenumbers library
    carrier_name = carrier.name_for_number(parsed, "id")
    if not carrier_name or carrier_name == "":
        # Fallback ke mapping manual
        local_num = "0" + str(parsed.national_number)
        carrier_name = get_carrier_from_prefix(local_num)

    # Wilayah
    region = geocoder.description_for_number(parsed, "id")
    if not region:
        region = geocoder.description_for_number(parsed, "en")

    # Zona waktu
    try:
        timezones = timezone.time_zones_for_number(parsed)
        tz_str = ", ".join(timezones) if timezones else "Tidak Diketahui"
    except:
        tz_str = "Tidak Diketahui"

    # Tipe jaringan
    number_type = phonenumbers.number_type(parsed)
    network_type = NETWORK_TYPE_MAP.get(number_type, "Tidak Diketahui")

    # Country code
    country_code = parsed.country_code
    country = "Indonesia" if country_code == 62 else f"Kode Negara +{country_code}"

    # Prefix analysis
    local_num_str = "0" + str(parsed.national_number)
    carrier_from_prefix = get_carrier_from_prefix(local_num_str)

    return {
        "success": True,
        "is_valid": is_valid,
        "is_possible": is_possible,
        "input_original": phone_input,
        "format_e164": e164,
        "format_national": national,
        "format_international": international,
        "country_code": f"+{country_code}",
        "country": country,
        "carrier": carrier_name or carrier_from_prefix,
        "carrier_from_prefix": carrier_from_prefix,
        "region": region or "Tidak Teridentifikasi",
        "timezone": tz_str,
        "network_type": network_type,
        "national_number": str(parsed.national_number),
        "prefix_4digit": local_num_str[:4] if len(local_num_str) >= 4 else local_num_str,
    }


def get_bts_request_template(phone_e164: str, carrier_name: str, region: str) -> str:
    """
    Generate template permohonan data teknis CDR/Cell-ID untuk penyidik.
    """
    return f"""
PERMOHONAN DATA TEKNIS JARINGAN TELEKOMUNIKASI

Nomor Target     : {phone_e164}
Operator         : {carrier_name}
Estimasi Wilayah : {region}

Data yang dimohon untuk keperluan penyidikan:

1. Call Detail Record (CDR) - Riwayat panggilan dan pesan
2. Cell ID / BTS Location - Lokasi BTS saat komunikasi berlangsung
3. IMEI History - Riwayat perangkat yang menggunakan nomor ini
4. Subscriber Data - Data pendaftaran nomor (KTP, nama pemilik)
5. IP Address Log - Jika menggunakan layanan data (WhatsApp, dll)

Dasar Hukum:
- UU No. 19 Tahun 2016 tentang ITE Pasal 43
- UU No. 36 Tahun 1999 tentang Telekomunikasi Pasal 42
- KUHAP Pasal 7 ayat (1) huruf j

Permohonan resmi harus diajukan melalui surat resmi Kepolisian
kepada operator {carrier_name} dengan dilampiri SPDP dan SP3K.
"""
