import requests

def kanal_listesini_guncelle():
    # IPTV-Org Türkiye kanalları listesi
    url = "https://iptv-org.github.io/iptv/countries/tr.m3u"
    
    try:
        print("Kanallar güncelleniyor...")
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            with open("kanallar.m3u", "w", encoding="utf-8") as f:
                f.write(response.text)
            print("İşlem başarılı: 'kanallar.m3u' dosyası güncellendi.")
        else:
            print(f"Sunucu hatası: {response.status_code}")
            
    except Exception as e:
        print(f"Bağlantı hatası: {e}")

if __name__ == "__main__":
    kanal_listesini_guncelle()
