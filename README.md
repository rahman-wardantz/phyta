# Pytha

![Python](https://img.shields.io/badge/python-3.7%2B-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

**Pytha** adalah chatbot GUI berbasis Python yang dirancang untuk membantu mengotomasi tugas sederhana, menjawab pertanyaan, dan menyediakan antarmuka interaktif yang mudah digunakan. Proyek ini mengutamakan kemudahan kustomisasi dan perluasan fitur, cocok untuk asisten pribadi, edukasi, atau integrasi sistem sederhana.

---

## Fitur Utama

- **Antarmuka Chat GUI Modern** (Tkinter, responsif, mendukung fullscreen)
- **Balasan Otomatis** dengan keyword dan fallback default
- **Simpan, Buka, dan Copy Riwayat Chat**
- **Download File dari URL** langsung dari chat
- **Struktur Modular** (mudah dikembangkan)
- **Mudah Dikustomisasi** (cukup edit file `responses.py` untuk menambah/mengubah balasan)

---

## Prasyarat

- Python 3.7 atau lebih tinggi
- `pip` untuk instalasi dependensi
- Paket yang diperlukan:
  - `requests`
  - (opsional) `flask` jika ingin integrasi web

---

## Instalasi

1. **Clone repositori:**

   ```bash
   git clone https://github.com/rahman-wardantz/phyta.git
   cd phyta
   ```

2. **Instal dependensi:**

   ```bash
   pip install requests
   # atau
   pip install -r requirements.txt
   ```

---

## Menjalankan Bot

Jalankan aplikasi GUI dengan perintah berikut:

```bash
python Main.py
```

---

## Penggunaan

- Ketik pesan di kolom input, tekan Enter atau klik **Kirim**.
- Gunakan tombol **Bersihkan Chat** untuk menghapus riwayat chat.
- Gunakan tombol **Simpan Chat** untuk menyimpan riwayat ke file `.txt`.
- Gunakan tombol **Buka Chat** untuk memuat riwayat chat dari file.
- Gunakan tombol **Copy Chat** untuk menyalin seluruh chat ke clipboard.
- Untuk download file, ketik: `download <url>`
- Untuk keluar, ketik: `exit` atau `quit`.

---

## Kustomisasi Balasan

Edit file `responses.py` untuk menambah/mengubah keyword dan balasan. Tambahkan variasi keyword agar bot lebih responsif.

---

## Kontribusi

Kontribusi sangat terbuka!
- Fork repositori ini dan buat branch baru untuk fitur/bugfix.
- Buat pull request dengan penjelasan perubahan.
- Ikuti style dan dokumentasi yang ada.

Jika menemukan bug/masalah, silakan buka **issue** di GitHub.

---

## Lisensi

Proyek ini dirilis di bawah lisensi [MIT License](LICENSE).

---

Selamat menggunakan **Pytha**! Jika butuh bantuan atau ingin mengembangkan fitur, silakan hubungi pengembang melalui GitHub.
