import os
import json
import requests
from bs4 import BeautifulSoup

def kanallari_cek():
    url = "https://www.canlitv.diy/tr"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    print("Veriler çekiliyor...")
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            print(status_code)
            return []
        
        soup = BeautifulSoup(response.content, "html.parser")
        kanal_listesi = []
        
        # Sitedeki kanal kartlarını veya linklerini hedef alıyoruz
        # Not: Sitenin HTML yapısına göre bu seçiciler (selector) değişiklik gösterebilir.
        # Genellikle canlı TV sitelerinde kanallar 'a' etiketleri içinde yer alır.
        for link in soup.find_all("a", href=True):
            href = link['href']
            # Sadece kanal sayfalarını filtrelemek için bir kontrol (örn: sonu .html biten veya belirli klasördeki linkler)
            if "/canli-" in href or "tv" in href:
                kanal_adi = link.text.strip() if link.text else "Bilinmeyen Kanal"
                
                # Tam URL'yi oluşturma
                tam_url = href if href.startswith("http") else f"https://www.canlitv.diy{href}"
                
                # Mükerrer (tekrar eden) kayıtları önlemek için kontrol
                if not any(k['url'] == tam_url for k in listesi):
                    kanal_listesi.append({
                        "kanal_adi": kanal_adi,
                        "url": tam_url
                    })
        
        return kanal_listesi

    except Exception as e:
        print(f"Hata oluştu: {e}")
        return []

def kaydet(veri):
    if veri:
        # Çıktıyı JSON formatında kaydediyoruz
        with open("kanallar.json", "w", encoding="utf-8") as f:
            json.dump(veri, f, ensure_ascii=False, indent=4)
        print(f"Başarıyla {len(veri)} kanal 'kanallar.json' dosyasına kaydedildi.")
    else:
        print("Kaydedilecek veri bulunamadı.")

if __name__ == "__main__":
    kanallar = kanallari_cek()
    kaydet(kanallar)
