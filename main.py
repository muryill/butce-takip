
import csv
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

# Kayıt ekleme
def veri_ekle():
    print("\n--- Yeni Kayıt Ekle ---")
    tarih = input("Tarih (gg/aa/yyyy): ")
    aciklama = input("Açıklama: ")
    kategori = input("Kategori (Gelir/Gider): ").lower()

    try:
        miktar = float(input("Miktar (₺): "))
    except ValueError:
        print(" Miktar sayı olmalı.")
        return

    with open("veriler.csv", mode="a", newline="", encoding="utf-8") as dosya:
        yazici = csv.writer(dosya)
        yazici.writerow([tarih, aciklama, kategori, miktar])

    print(" Kayıt eklendi!")


# veri listeleme ve bakiye hesaplama
def verileri_listele():
    print("\n--- Kayıtlar ---")

    try:
        with open("veriler.csv", mode="r", encoding="utf-8") as dosya:
            okuyucu = csv.reader(dosya)
            toplam_gelir = 0
            toplam_gider = 0

            for satir in okuyucu:
                tarih, aciklama, kategori, miktar = satir
                miktar = float(miktar)

                if kategori == "gelir":
                    toplam_gelir += miktar
                elif kategori == "gider":
                    toplam_gider += miktar

                print(f"{tarih} | {kategori.title():<6} | {aciklama:<20} | ₺{miktar:.2f}")

            bakiye = toplam_gelir - toplam_gider
            print("\n-----------------------------")
            print(f"Toplam Gelir: ₺{toplam_gelir:.2f}")
            print(f"Toplam Gider: ₺{toplam_gider:.2f}")
            print(f" Bakiye: ₺{bakiye:.2f}")

    except FileNotFoundError:
        print("Henüz veri eklenmemiş.")


# grafik
def grafik_goster():
    try:
        df = pd.read_csv("veriler.csv", names=["Tarih", "Açıklama", "Kategori", "Miktar"])
        df = df[df["Tarih"].str.contains("/", na=False)]  # sadece geçerli tarihleri al
        df["Tarih"] = pd.to_datetime(df["Tarih"], format="%d/%m/%Y")
        df["Ay"] = df["Tarih"].dt.to_period("M")

        grup = df.groupby(["Ay", "Kategori"])["Miktar"].sum().unstack().fillna(0)

        grup.plot(kind="bar", stacked=True)
        plt.title("Aylık Gelir ve Gider")
        plt.xlabel("Ay")
        plt.ylabel("Miktar (₺)")
        plt.legend(["Gider", "Gelir"])
        plt.tight_layout()
        plt.show()

    except FileNotFoundError:
        print("veriler.csv bulunamadı.")
    except Exception as e:
        print(f"Hata oluştu: {e}")

def menu():
    while True:
        print("\n BÜTÇE TAKİP MENÜSÜ")
        print("1 - Yeni Kayıt Ekle")
        print("2 - Kayıtları Listele")
        print("3 - Aylık Gelir-Gider Grafiği")
        print("4 - Çıkış")

        secim = input("Seçiminiz (1-4): ")

        if secim == "1":
            veri_ekle()
        elif secim == "2":
            verileri_listele()
        elif secim == "3":
            grafik_goster()
        elif secim == "4":
            print("👋 Programdan çıkılıyor...")
            break
        else:
            print(" Geçersiz seçim. Lütfen 1-4 arası bir değer girin.")


menu()
