import requests

def bot_kanal7_guncelle():
    # Kanal 7'nin canlı yayın verisini sağlayan uç nokta
    api_url = "https://www.kanal7.com/api/get_live_info" 
    
    try:
        # Gerçek bir tarayıcı gibi görünmek için header ekliyoruz
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(api_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            # API'den gelen stream_url değerini al, yoksa yedek linki kullan
            link = data.get("stream_url", "https://kanal7-live.daioncdn.net/kanal7/kanal7_1080p.m3u8")
            
            with open("kanallar.m3u", "w", encoding="utf-8") as f:
                f.write("#EXTM3U\n")
                f.write(f"#EXTINF:-1,Kanal 7 (Bot)\n{link}\n")
            print(f"Bot çalıştı. Güncel link: {link}")
        else:
            print(f"API hatası: {response.status_code}")
            
    except Exception as e:
        print(f"Bağlantı hatası: {e}")

if __name__ == "__main__":
    bot_kanal7_guncelle()
