import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def get_m3u8_links():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # Ağ trafiğini izlemek için loglama özelliği
    chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    # Kanal listesi
    kanallar = [
        {"adi": "Kanal 7", "url": "https://www.canlitv.diy/tr/kanal7"}
    ]
    
    sonuc = []
    
    for k in kanallar:
        print(f"{k['adi']} taranıyor...")
        driver.get(k['url'])
        time.sleep(10) # Videonun yüklenmesi için bekle
        
        logs = driver.get_log('performance')
        for entry in logs:
            log = json.loads(entry['message'])['message']
            if log['method'] == 'Network.requestWillBeSent':
                url = log['params']['request']['url']
                if ".m3u8" in url:
                    sonuc.append({"adi": k['adi'], "url": url})
                    break
    
    driver.quit()
    return sonuc

def kaydet(veri):
    with open("kanallar.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for k in veri:
            f.write(f"#EXTINF:-1,{k['adi']}\n{k['url']}\n")

if __name__ == "__main__":
    veriler = get_m3u8_links()
    if veriler:
        kaydet(veriler)
    else:
        print("Hiç link bulunamadı!")
