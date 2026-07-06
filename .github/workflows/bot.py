name: Canlı TV Güncelleyici Bot (Saatlik)

on:
  schedule:
    # Her saatin başında (00:00, 01:00, 02:00...) otomatik çalışır
    - cron: '0 * * * *'
  workflow_dispatch: # İstediğin zaman manuel başlatabilmen için

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Depoyu Klonla
      uses: actions/checkout@v4

    - name: Python Kur
      uses: actions/setup-python@v5
      with:
        python-version: '3.10'

    - name: Bağımlılıkları Yükle
      run: |
        python -m pip install --upgrade pip
        pip install requests beautifulsoup4

    - name: Botu Çalıştır
      run: python güncelleme.py

    - name: Değişiklikleri Kaydet ve Gönder
      run: |
        git config --local user.email "github-actions[bot]@users.noreply.github.com"
        git config --local user.name "github-actions[bot]"
        git add kanallar.json
        # Eğer saat başı kontrolde yeni bir kanal eklenmediyse hata vermemesi için:
        git commit -m "Saatlik Güncelleme: Canlı TV Listesi Yenilendi" || echo "Değişiklik yok."
        git push
