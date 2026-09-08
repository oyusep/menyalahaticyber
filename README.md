# Menyalahati Cyber - Sistem Diagnosa Forensik

Aplikasi Streamlit untuk melakukan Diagnosa Jejak Digital (Doxing/DC Pinjol), Profiling Nomor HP, dan Pencatatan Kasus Pembersihan Data.

## 🚀 Cara Menjalankan Aplikasi di Laptop / PC Baru

Aplikasi ini sangat mudah dijalankan di device mana pun asalkan sudah terinstall **Python 3.10+**.

### Opsi 1: Menggunakan Script (Paling Mudah)

**Untuk Pengguna Windows:**
Cukup klik dua kali pada file `run.bat` atau jalankan dari terminal:
```cmd
run.bat
```
*(Script otomatis akan menginstall library yang kurang dan langsung menjalankan aplikasi).*

**Untuk Pengguna Mac / Linux:**
```bash
bash run.sh
```

---

### Opsi 2: Menjalankan Manual via Terminal

1. **Install dependensi (library Python):**
   ```bash
   pip install -r requirements.txt
   ```

2. **Jalankan Aplikasi Streamlit:**
   ```bash
   streamlit run app.py
   ```

3. **Buka di Browser:**
   Aplikasi akan otomatis terbuka di browser pada alamat:
   **http://localhost:8501**

## ⚙️ Konfigurasi (Opsional)
Jika Anda membutuhkan integrasi API (misalnya Google API), copy file `.env.example` menjadi `.env` lalu isi token yang diperlukan:
```bash
cp .env.example .env
```
*(Aplikasi tetap bisa berjalan 100% normal tanpa .env dengan menggunakan data fallback/lokal)*

## 🗄️ Database
Database aplikasi menggunakan **SQLite** yang sudah bawaan dari Python. Tidak perlu install database tambahan (MySQL/PostgreSQL). File database akan otomatis terbuat dengan nama `forensik_data.db` saat aplikasi pertama kali dijalankan.
