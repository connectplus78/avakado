import requests

def bot_kanal7_guncelle():
    api_url = "https://www.kanal7.com/api/get_live_info"
    yedek_link = "https://kanal7-live.daioncdn.net/kanal7/kanal7_1080p.m3u8"
    
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(api_url, headers=headers, timeout=10)
        
        # Hata ayıklama: Gelen cevabı ekrana yazdır (Actions loglarında görebilirsiniz)
        print(f"API Yanıt Kodu: {response.status_code}")
        
        if response.status_code == 200:
            # Cevabı JSON olarak değil, düz metin olarak kontrol etmeye çalışalım
            try:
                data = response.json()
                link = data.get("stream_url", yedek_link)
            except:
                link = yedek_link
        else:
            link = yedek_link
            
        with open("kanallar.m3u", "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            f.write(f"#EXTINF:-1,Kanal 7 (Bot)\n{link}\n")
        print(f"Başarıyla güncellendi. Kullanılan link: {link}")
            
    except Exception as e:
        print(f"Hata oluştu: {e}")
        # Hata olsa bile dosya boş kalmasın, yedek linki yaz
        with open("kanallar.m3u", "w", encoding="utf-8") as f:
            f.write(f"#EXTM3U\n#EXTINF:-1,Kanal 7 (Yedek)\n{yedek_link}\n")

if __name__ == "__main__":
    bot_kanal7_guncelle()
