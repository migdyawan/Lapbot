import telebot
from telebot import types
import os
from datetime import datetime

# =========================
# Ambil token dari environment variable
# =========================
TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# =========================
# Fungsi parsing & format laporan
# =========================
def buat_laporan(input_text):
    lines = input_text.strip().split("\n")
    
    # Baris pertama = hari + tanggal
    header = lines[0].strip()
    laporan = f"Selamat malam Gubernur\n"
    laporan += f"mohon ijin melaporkan rengiat hari {header.replace('  ', ' ')} sbb:\n\n"

    nomor = 1
    kegiatan = []
    current = {}

    for line in lines[1:]:
        line = line.strip()
        if not line:
            if current:
                kegiatan.append(current)
                current = {}
            continue

        # Deteksi waktu (format 07.00, 15.30, dll)
        if line[:5].replace('.', '').isdigit():
            waktu, *judul = line.split(" ")
            current = {
                "waktu": waktu,
                "judul": " ".join(judul).strip() + ".",
                "detail": []
            }
        else:
            parts = line.split(" ")
            kata = parts[0].lower()
            isi_text = " ".join(parts[1:])

            mapping = {
                "irup": "Irup",
                "pimpinan": "Pimpinan",
                "tempat": "Tempat",
                "pakaian": "Pakaian"
            }

            if kata in mapping:
                if kata == "pakaian":
                    current["detail"].append(f"- {mapping[kata]} : {isi_text}")
                else:
                    current["detail"].append(f"- {mapping[kata]}: {isi_text}")

    if current:
        kegiatan.append(current)

    # Susun output laporan
    for item in kegiatan:
        laporan += f"{nomor}.  Pukul {item['waktu']} WIB\n"
        laporan += f"{item['judul']}\n"
        for d in item["detail"]:
            laporan += f"{d}\n"
        laporan += "\n"
        nomor += 1

    laporan += "Demikian kami laporkan   terimakasih selamat malam."
    return laporan

# =========================
# Handler Bot Telegram
# =========================

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Halo! Bot laporan harian siap digunakan.\nKetik laporan harian mulai dari hari dan tanggal.")

@bot.message_handler(func=lambda message: True)
def handle_laporan(message):
    input_text = message.text
    try:
        laporan = buat_laporan(input_text)
        bot.reply_to(message, laporan)
    except Exception as e:
        bot.reply_to(message, f"Ada error saat memproses laporan: {str(e)}")

# =========================
# Jalankan bot
# =========================
if __name__ == "__main__":
    print("Bot laporan harian aktif...")
    bot.infinity_polling()
