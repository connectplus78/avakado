import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def get_m3u8_from_page(driver, kanal_url):
    """Verilen sayfayı açar ve m3u8 linkini bulmaya çalışır."""
    try:
        driver.get(kanal_url)
        time.sleep(5)  # Sayfanın yüklenmesi için bekle
        
        # Sayfa kaynağında m3u8 uzantılı link ara
        page_source = driver.page_source
        match = re.search(r'https?://[^\s"\'<>]+?\.m3u8', page_source)
        
        return match.group(0) if match else None
    except Exception:
        return None

def main():
    # Kanal listenizi buraya ekleyin
    kanallar = [
        {"adi": "Kanal 7", "url": "https://www.canlitv.diy/tr/kanal7"},
        # Diğer kanalları buraya ekleyebilirsiniz...
    ]

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    with open("kanallar.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        
        for kanal in kanallar:
            print(f"{kanal['adi']} işleniyor...")
            m3u8_link = get_m3u8_from_page(driver, kanal['url'])
            
            if m3u8_link:
                f.write(f"#EXTINF:-1,{kanal['adi']}\n")
                f.write(f"{m3u8_link}\n")
                print(f"-> Başarılı: {m3u8_link}")
            else:
                print(f"-> Hata: Link bulunamadı.")

    driver.quit()
    print("\nİşlem tamamlandı. 'kanallar.m3u' dosyası oluşturuldu.")

if __name__ == "__main__":
    main()
