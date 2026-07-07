import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def get_m3u8_links():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") # Modern headless modu (Daha stabil)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    kanallar = [
        {"adi": "Kanal 7", "url": "https://www.canlitv.diy/tr/kanal7"}
    ]
    
    sonuc = []
    
    for k in kanallar:
        print(f"{k['adi']} taranıyor...")
        driver.get(k['url'])
        time.sleep(15) # Sayfa ve JS yüklenmesi için yeterli süre
        
        # 1. YÖNTEM: Sayfa kaynağında regex ile ara
        page_source = driver.page_source
        linkler = re.findall(r'https?://[^\s"\'<>]+?\.m3u8', page_source)
        
        # 2. YÖNTEM: Eğer ana sayfada yoksa iframe'leri kontrol et
        if not linkler:
            iframes = driver.find_elements(by="tag name", value="iframe")
            for iframe in iframes:
                try:
                    driver.switch_to.frame(iframe)
                    linkler += re.findall(r'https?://[^\s"\'<>]+?\.m3u8', driver.page_source)
                    driver.switch_to.default_content()
                except:
                    continue
        
        # Benzersiz linkleri al ve kaydet
        for link in list(set(linkler)):
            sonuc.append({"adi": k['adi'], "url": link})
            break # Her kanal için ilk bulunan link yeterlidir
    
    driver.quit()
    return sonuc

def kaydet(veri):
    with open("kanallar.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for k in veri:
            f.write(f"#EXTINF:-1,{k['adi']}\n{k['url']}\n")
    print(f"Toplam {len(veri)} kanal kaydedildi.")

if __name__ == "__main__":
    veriler = get_m3u8_links()
    if veriler:
        kaydet(veriler)
    else:
        print("Link bulunamadı! Sayfa yapısı değişmiş olabilir.")
