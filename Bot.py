import telebot
from telebot import types
import os
from datetime import datetime
import re

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

def buat_laporan(input_text):
    lines = input_text.strip().split("\n")
    
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

        # Deteksi waktu (format 07.00 dll)
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

    for item in kegiatan:
        laporan += f"{nomor}.  Pukul {item['waktu']} WIB\n"
        laporan += f"{item['judul']}\n"
        for d in item["detail"]:
            laporan += f"{d}\n"
        laporan += "\n"
        nomor += 1

    laporan += "Demikian kami laporkan   terimakasih selamat malam."

    return laporan


bot.infinity_polling()
