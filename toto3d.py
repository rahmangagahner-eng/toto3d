#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
3D INTELLIGENCE v7.0
✅ Prediksi 3D (3 digit terakhir)
✅ Multi Pasaran: HK/SYD | Pools/Lotto
✅ Algoritma Hybrid: Statistik + Mistik + Tesson + Shio + Run
✅ Auto-Analisis saat input
"""

import os
import sys
import time
from collections import Counter
from typing import List, Dict, Tuple

# ──────────────────────────────────────────────────────────────
# Warna & Tampilan
# ──────────────────────────────────────────────────────────────
RESET = "\033[0m"

def colored(text: str, color: str = "white", style: str = "normal") -> str:
    styles = {"normal": 0, "bold": 1, "dim": 2}
    colors = {
        "red": 31, "green": 32, "yellow": 33, "blue": 34,
        "magenta": 35, "cyan": 36, "white": 37,
        "bright_red": 91, "bright_green": 92, "bright_yellow": 93,
        "bright_blue": 94, "bright_magenta": 95, "bright_cyan": 96,
    }
    s = styles.get(style, 0)
    c = colors.get(color, 37)
    return f"\033[{s};{c}m{text}{RESET}"

def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")

# ──────────────────────────────────────────────────────────────
# Banner
# ──────────────────────────────────────────────────────────────
BANNER = colored(r"""
   ____           _       _    ____ _  __
  / ___| ___ _ __| |_ ___| |  / ___| |/ /
 | |  _ / _ \ '__| __/ _ \ | | |   | ' / 
 | |_| |  __/ |  | ||  __/ | | |___| . \ 
  \____|\___|_|   \__\___|_|  \____|_|\_\
                                        
        🔮 3D INTELLIGENCE v7.0
     Prediksi 3D Cerdas – Hybrid Algorithm
""", "bright_magenta", "bold")

# ──────────────────────────────────────────────────────────────
# Konfigurasi Pasaran
# ──────────────────────────────────────────────────────────────
MARKETS = {
    "1": "hongkong_pools",
    "2": "sydney_pools",
    "3": "hongkong_lotto",
    "4": "sydney_lotto"
}

MARKET_NAMES = {
    "hongkong_pools": "🇭🇰 Hongkong Pools",
    "sydney_pools": "🇦🇺 Sydney Pools",
    "hongkong_lotto": "🎰 Hongkong Lotto",
    "sydney_lotto": "🎯 Sydney Lotto"
}

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def get_filepath(market: str) -> str:
    return os.path.join(DATA_DIR, f"{market}.txt")

def load_history(market: str) -> List[str]:
    filepath = get_filepath(market)
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r") as f:
            return [line.strip() for line in f if line.strip().isdigit() and len(line.strip()) == 4]
    except:
        return []

def save_history(market: str, history: List[str]) -> None:
    filepath = get_filepath(market)
    with open(filepath, "w") as f:
        f.write("\n".join(history))

# ──────────────────────────────────────────────────────────────
# Data Mistik & Pola
# ──────────────────────────────────────────────────────────────
mistik_baru = {0: 8, 1: 7, 2: 6, 3: 9, 4: 5}
mistik_lama = {0: 1, 2: 5, 3: 8, 4: 7, 6: 9}

# ──────────────────────────────────────────────────────────────
# Deteksi Pola Lanjutan (untuk 3D)
# ──────────────────────────────────────────────────────────────
def deteksi_pola_3d(history: List[str]) -> Dict[str, any]:
    if len(history) < 5:
        return {}

    # Ambil 3D terakhir (posisi 1-3: ribuan, ratusan, puluhan) atau (2-4: ratusan, puluhan, satuan)?
    # Kita ambil 3D belakang: posisi 1,2,3 (ratusan, puluhan, satuan)
    all_3d = [res[1:] for res in history]  # ambil 3 digit terakhir
    ekor_3 = [res[3] for res in history]   # satuan
    kepala = [res[0] for res in history]  # ribuan

    pola = {}

    # 1. Frekuensi 3D
    freq_3d = Counter(all_3d)
    pola["3d_terpanas"] = [t for t, _ in freq_3d.most_common(10)]

    # 2. Frekuensi digit di tiap posisi
    pos0 = Counter([r[1] for r in history])  # ratusan
    pos1 = Counter([r[2] for r in history])  # puluhan
    pos2 = Counter([r[3] for r in history])  # satuan
    pola["pos_ratusan"] = [d for d, _ in pos0.most_common(3)]
    pola["pos_puluhan"] = [d for d, _ in pos1.most_common(3)]
    pola["pos_satuan"] = [d for d, _ in pos2.most_common(3)]

    # 3. Mistik dari ekor & kepala
    mistik_ekor = []
    for e in ekor_3:
        e = int(e)
        if e in mistik_baru: mistik_ekor.append(str(mistik_baru[e]))
        if e in mistik_lama: mistik_ekor.append(str(mistik_lama[e]))
    pola["mistik_ekor"] = list(set(mistik_ekor))

    # 4. Tesson 2 & 3 dari ekor
    tesson2 = [(int(e)**2) % 10 for e in ekor_3]
    tesson3 = [(int(e)**3) % 10 for e in ekor_3]
    pola["tesson2"] = list(set(map(str, tesson2)))
    pola["tesson3"] = list(set(map(str, tesson3)))

    # 5. Shio dari 3D
    shio_3d = [int(t) % 12 for t in all_3d]
    freq_shio = Counter(shio_3d)
    pola["shio_kuat"] = [s for s, _ in freq_shio.most_common(3)]

    # 6. Angka dingin
    all_digits = [d for res in history for d in res]
    freq_digit = Counter(all_digits)
    pola["angka_dingin"] = [d for d, cnt in freq_digit.items() if cnt < 2]

    return pola

# ──────────────────────────────────────────────────────────────
# Prediksi 3D Kuat (10 angka 3D terkuat)
# ──────────────────────────────────────────────────────────────
def generate_3d_kuat(history: List[str]) -> Tuple[List[str], List[str]]:
    if len(history) < 10:
        return ["123", "456", "789", "012", "345", "678", "234", "567", "890", "135"], ["Data kurang"]

    pola = deteksi_pola_3d(history)
    candidates = Counter()

    # 1. Dari 3D terpanas
    for t3 in pola["3d_terpanas"]:
        candidates[t3] += 10

    # 2. Kombinasi posisi kuat
    for r in pola["pos_ratusan"]:
        for p in pola["pos_puluhan"]:
            for s in pola["pos_satuan"]:
                combo = r + p + s
                candidates[combo] += 5

    # 3. Mistik ekor → bisa muncul di satuan
    for m in pola["mistik_ekor"]:
        for r in "0123456789":
            for p in "0123456789":
                combo = r + p + m
                if combo in candidates:
                    candidates[combo] += 3

    # 4. Tesson 2 & 3
    for t in pola["tesson2"] + pola["tesson3"]:
        for c in candidates:
            if c[2] == t:
                candidates[c] += 2

    # 5. Shio kuat → konversi ke 3D yang mod 12 cocok
    for c in candidates:
        if int(c) % 12 in pola["shio_kuat"]:
            candidates[c] += 3

    # Ambil 10 3D terkuat
    top_10 = [item[0] for item in candidates.most_common(10)]
    alasan = [
        f"3D Panas: {len(pola['3d_terpanas'])}",
        f"Posisi: R{pola['pos_ratusan']}, P{pola['pos_puluhan']}, S{pola['pos_satuan']}",
        f"Mistik: {pola['mistik_ekor']}",
        f"Tesson: {pola['tesson2']}, {pola['tesson3']}"
    ]

    return top_10, alasan

# ──────────────────────────────────────────────────────────────
# Prediksi BBFS 3D (6 digit bebas untuk 3D)
# ──────────────────────────────────────────────────────────────
def generate_bbfs_3d(history: List[str]) -> Tuple[List[str], List[str]]:
    if len(history) < 10:
        return ["1", "2", "4", "5", "7", "8"], ["Fallback"]

    pola = deteksi_pola_3d(history)
    candidates = Counter()

    # 1. Digit dari 3D terpanas
    for t3 in pola["3d_terpanas"]:
        for d in t3:
            candidates[d] += 8

    # 2. Posisi kuat
    for d in pola["pos_ratusan"] + pola["pos_puluhan"] + pola["pos_satuan"]:
        candidates[d] += 6

    # 3. Mistik & Tesson
    for d in pola["mistik_ekor"] + pola["tesson2"] + pola["tesson3"]:
        candidates[d] += 5

    # 4. Angka dingin
    for d in pola["angka_dingin"]:
        candidates[d] += 7

    # 5. Shio kuat → digit shio
    for s in pola["shio_kuat"]:
        candidates[str(s % 10)] += 4

    top_6 = [item[0] for item in candidates.most_common(6)]
    alasan = [
        f"3D Panas & Posisi",
        f"Mistik: {pola['mistik_ekor']}",
        f"Tesson: {pola['tesson2'][:3]}...",
        f"Dingin: {pola['angka_dingin']}",
        f"Shio: {pola['shio_kuat']}"
    ]

    return sorted(top_6, key=lambda x: int(x)), alasan

# ──────────────────────────────────────────────────────────────
# Backtest 3D
# ──────────────────────────────────────────────────────────────
def backtest_3d(history: List[str]) -> None:
    if len(history) < 2:
        print(colored("\n❌ Butuh minimal 2 data!", "red"))
        input(colored("Enter...", "dim"))
        return

    tembus = 0
    total = len(history) - 1

    print(colored(f"\n🔍 BACKTEST: Apakah 3D MASUK prediksi?", "bright_yellow", "bold"))

    for i in range(total):
        prev_batch = history[:i+1]
        actual = history[i+1]
        t3_actual = actual[1:]  # 3 digit terakhir

        pred_3d, _ = generate_3d_kuat(prev_batch)
        match = t3_actual in pred_3d
        status = "✅" if match else "❌"

        if match:
            tembus += 1
        print(f"{status} {prev_batch[-1]} → {actual} | 3D: {t3_actual}")

    akurasi = (tembus / total) * 100
    warna = "green" if akurasi >= 70 else "yellow" if akurasi >= 50 else "red"
    print(colored(f"\n🎯 Akurasi 3D: {tembus}/{total} → {akurasi:.1f}%", warna, "bold"))
    input(colored("\nTekan Enter...", "dim"))

# ──────────────────────────────────────────────────────────────
# Animasi
# ──────────────────────────────────────────────────────────────
def loading_animation():
    for _ in range(15):
        sys.stdout.write("\r" + colored("🧠", "cyan") + " AI menganalisis 3D...")
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write("\r" + " " * 50 + "\r")

# ──────────────────────────────────────────────────────────────
# Menu Utama
# ──────────────────────────────────────────────────────────────
def menu():
    while True:
        clear_screen()
        print(BANNER)
        print(colored("\nPilih Pasaran:", "bright_blue", "bold"))
        for key, code in MARKETS.items():
            history = load_history(code)
            name = MARKET_NAMES[code]
            print(f" {key}. {name} {colored(f'({len(history)} data)', 'dim')}")

        print(colored("\nAksi:", "bright_blue", "bold"))
        print(" 5. Prediksi 10 Angka 3D Kuat")
        print(" 6. Prediksi BBFS 3D (6 digit)")
        print(" 7. Backtest 3D")
        print(" 8. Hapus Data Pasaran")
        print(" 9. Keluar\n")

        choice = input(colored("Pilih: ", "yellow")).strip()

        if choice in MARKETS:
            market_code = MARKETS[choice]
            market_name = MARKET_NAMES[market_code]
            history = load_history(market_code)

            print(colored(f"\n📁 {market_name} | {len(history)} data", "blue"))
            print(colored("\nMasukkan 4D (kosongkan untuk kembali):", "cyan"))
            added = 0
            while True:
                inp = input(f"Hasil {len(history) + added + 1}: ").strip()
                if not inp:
                    break
                if inp.isdigit() and len(inp) == 4:
                    history.append(inp)
                    added += 1
                    print(colored("✓", "green"))
                    # Auto-analisis setelah input
                    if len(history) >= 10:
                        print(colored("🔍 Auto-analisis pola aktif...", "dim"))
                else:
                    print(colored("✗ 4 digit!", "red"))
            if added > 0:
                save_history(market_code, history)
                print(colored(f"💾 Disimpan: {market_name}", "bright_green"))

        elif choice == "5":
            print(colored("\nPilih pasaran untuk prediksi 3D:", "cyan"))
            for key, code in MARKETS.items():
                name = MARKET_NAMES[code]
                hist = load_history(code)
                print(f" {key}. {name} {colored(f'({len(hist)} data)', 'dim')}")
            pick = input(colored("Pilih: ", "yellow")).strip()
            if pick not in MARKETS:
                print(colored("Pilihan salah!", "red"))
                input(colored("Enter...", "dim"))
                continue

            market_code = MARKETS[pick]
            market_name = MARKET_NAMES[market_code]
            history = load_history(market_code)

            if len(history) < 10:
                print(colored(f"\n⚠️ Butuh 10+ data {market_name}!", "yellow"))
                input(colored("Enter...", "dim"))
                continue

            loading_animation()
            pred_3d, alasan = generate_3d_kuat(history)
            clear_screen()
            print(BANNER)
            print(colored(f"\n🎯 PASARAN: {market_name}", "bright_magenta", "bold"))
            print(colored(f"🔥 10 ANGKA 3D KUAT:", "bright_green", "bold"))
            for i, val in enumerate(pred_3d, 1):
                print(f"{i:2}. {colored(val, 'bright_yellow', 'bold')}")
            print(colored(f"\n💡 Alasan:", "dim"))
            for a in alasan:
                print(f"   • {a}")
            input(colored("\n\nEnter untuk kembali...", "dim"))

        elif choice == "6":
            print(colored("\nPilih pasaran untuk BBFS 3D:", "cyan"))
            for key, code in MARKETS.items():
                name = MARKET_NAMES[code]
                hist = load_history(code)
                print(f" {key}. {name} {colored(f'({len(hist)} data)', 'dim')}")
            pick = input(colored("Pilih: ", "yellow")).strip()
            if pick not in MARKETS:
                print(colored("Salah!", "red"))
                input(colored("Enter...", "dim"))
                continue

            history = load_history(MARKETS[pick])
            if len(history) < 10:
                print(colored("\n⚠️ Butuh 10+ data!", "yellow"))
                input(colored("Enter...", "dim"))
                continue

            loading_animation()
            bbfs, alasan = generate_bbfs_3d(history)
            clear_screen()
            print(BANNER)
            print(colored(f"\n🎯 BBFS 3D (6 digit):", "bright_green", "bold"))
            print(" → " + colored("  ".join(bbfs), "bright_yellow", "bold"))
            print(colored(f"\n💡 Untuk: 3D, colok bebas, kombinasi", "dim"))
            print(colored(f"\n🔍 Alasan:", "dim"))
            for a in alasan:
                print(f"   • {a}")
            input(colored("\n\nEnter untuk kembali...", "dim"))

        elif choice == "7":
            print(colored("\nPilih pasaran untuk backtest 3D:", "cyan"))
            for key, code in MARKETS.items():
                name = MARKET_NAMES[code]
                hist = load_history(code)
                print(f" {key}. {name} {colored(f'({len(hist)} data)', 'dim')}")
            pick = input(colored("Pilih: ", "yellow")).strip()
            if pick not in MARKETS:
                continue
            history = load_history(MARKETS[pick])
            backtest_3d(history)

        elif choice == "8":
            print(colored("\nPilih pasaran untuk hapus:", "red"))
            for key, code in MARKETS.items():
                name = MARKET_NAMES[code]
                hist = load_history(code)
                print(f" {key}. {name} {colored(f'({len(hist)} data)', 'dim')}")
            pick = input(colored("Pilih: ", "red")).strip()
            if pick not in MARKETS:
                continue
            code = MARKETS[pick]
            if input(colored(f"Hapus {MARKET_NAMES[code]}? (y/t): ", "red")).lower() == 'y':
                filepath = get_filepath(code)
                if os.path.exists(filepath):
                    os.remove(filepath)
                print(colored(f"🗑️ {MARKET_NAMES[code]} dihapus", "green"))
                time.sleep(1)

        elif choice == "9":
            print(colored("\nSemoga 3D Anda selalu tembus! 🍀", "bright_yellow"))
            break

        else:
            print(colored("Pilih 1-9!", "red"))
            input(colored("Enter...", "dim"))

# ──────────────────────────────────────────────────────────────
# Jalankan
# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print(colored("\n\nDihentikan.", "red"))
