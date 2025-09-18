import os
import requests
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

# Muat environment variables dari file .env
load_dotenv()

# Inisialisasi aplikasi FastAPI
app = FastAPI(
    title="Client Analisis Penjualan",
    description="Client untuk meminta data penjualan dan menganalisisnya dengan Gemini AI.",
    version="1.0.0"
)

# Konfigurasi Gemini AI dengan API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY tidak ditemukan. Pastikan ada di file .env")
genai.configure(api_key=GEMINI_API_KEY)

# URL endpoint server data
SERVER_URL = "http://127.0.0.1:8000/get-sales-data"

@app.get("/analyze-sales", tags=["Analisis"])
def analyze_sales():
    """
    Endpoint untuk mengambil data dari server dan menganalisisnya menggunakan Gemini.
    """
    # 1. Meminta data dari server
    try:
        print(f"Mengambil data dari server di {SERVER_URL}...")
        response_server = requests.get(SERVER_URL)
        response_server.raise_for_status()  # Akan error jika status code bukan 2xx
        sales_data = response_server.json()
        print("Berhasil mendapatkan data dari server.")
    except requests.exceptions.RequestException as e:
        print(f"Error saat menghubungi server: {e}")
        raise HTTPException(status_code=503, detail=f"Tidak dapat terhubung ke server data: {e}")

    # 2. Mengirim data ke Gemini untuk dianalisis
    try:
        print("Mengirim data ke Gemini untuk dianalisis...")
        model = genai.GenerativeModel('gemini-2.5-pro')
        
        # Membuat prompt yang jelas untuk Gemini
        prompt = f"""
        Anda adalah seorang analis data yang ahli.
        Berikut adalah data penjualan dalam format JSON:
        {sales_data}

        Tolong berikan analisis singkat dari data tersebut. Sertakan poin-poin berikut:
        1. Produk mana yang paling banyak terjual (berdasarkan 'Jumlah')?
        2. Berapa total pendapatan dari semua transaksi?
        3. Berikan satu insight atau rekomendasi bisnis berdasarkan data ini.
        
        Sajikan jawaban dalam format JSON.
        """
        
        response_gemini = model.generate_content(prompt)
        
        # Membersihkan output dari Gemini (terkadang ada markdown)
        cleaned_response = response_gemini.text.strip().replace("```json", "").replace("```", "")
        
        print("Berhasil mendapatkan analisis dari Gemini.")
        return JSONResponse(content={"analisis_gemini": cleaned_response})

    except Exception as e:
        print(f"Error saat menghubungi Gemini API: {e}")
        raise HTTPException(status_code=500, detail=f"Terjadi kesalahan saat berkomunikasi dengan Gemini: {str(e)}")

