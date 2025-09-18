import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

# Inisialisasi aplikasi FastAPI
app = FastAPI(
    title="Server Data Penjualan",
    description="Server untuk menyediakan data penjualan dari file CSV.",
    version="1.0.0"
)

# Lokasi file CSV
CSV_FILE_PATH = "data_penjualan.csv"

@app.get("/get-sales-data", tags=["Data"])
def get_sales_data():
    """
    Endpoint untuk membaca data penjualan dari file CSV dan mengirimkannya sebagai JSON.
    """
    try:
        # Membaca data dari file CSV menggunakan pandas
        df = pd.read_csv(CSV_FILE_PATH)
        
        # Mengubah dataframe menjadi format JSON
        data_json = df.to_dict(orient="records")
        
        print("Berhasil membaca data dan mengirimkannya ke client.")
        return JSONResponse(content=data_json)

    except FileNotFoundError:
        print(f"Error: File {CSV_FILE_PATH} tidak ditemukan.")
        raise HTTPException(status_code=404, detail=f"File {CSV_FILE_PATH} tidak ditemukan.")
    except Exception as e:
        print(f"Terjadi error: {e}")
        raise HTTPException(status_code=500, detail=f"Terjadi kesalahan internal di server: {str(e)}")

