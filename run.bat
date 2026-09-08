@echo off
echo ===================================================
echo   Menjalankan Menyalahati Cyber - Forensik System
echo ===================================================
echo.

echo [1] Mengecek dan Menginstall Library Python...
pip install -r requirements.txt
echo.

echo [2] Menjalankan Aplikasi Streamlit...
streamlit run app.py

pause
