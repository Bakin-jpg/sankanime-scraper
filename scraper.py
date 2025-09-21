import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

API_KEY = os.getenv("SCRAPINGBEE_API_KEY")
url = "https://sankanime.com/watch/nine-rulers-crown-19741"  # URL baru

params = {
    'api_key': API_KEY,
    'url': url,
    'render_js': 'true',
    'wait': '20000',  # Tunggu 20 detik agar halaman termuat
    'wait_for': '.app-container',
    'premium_proxy': 'true',
}

try:
    print("🚀 Mengirim request ke ScrapingBee...")
    response = requests.get('https://app.scrapingbee.com/api/v1/', params=params)

    if response.status_code == 200:
        print("✅ Berhasil mengambil halaman!")
        
        # Simpan HTML mentah untuk debugging
        with open("debug_page.html", "w", encoding="utf-8") as f:
            f.write(response.text)
        print("🔍 HTML halaman disimpan ke debug_page.html")

        soup = BeautifulSoup(response.text, 'html.parser')

        qualities = ['360p', '480p', '720p', '1080p']
        found_links = {}

        for quality in qualities:
            link_element = soup.find('a', text=quality)
            if link_element and link_element.has_attr('href'):
                found_links[quality] = link_element['href']
                print(f"✅ Ditemukan: {quality} -> {link_element['href']}")
            else:
                print(f"❌ Link untuk {quality} tidak ditemukan")

        # Simpan hasil ke JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"links_{timestamp}.json"

        with open(filename, 'w') as f:
            json.dump(found_links, f, indent=2)

        print(f"✅ Hasil disimpan ke {filename}")

    else:
        print(f"❌ Gagal mengambil halaman. Status code: {response.status_code}")
        print("Response:", response.text)

except Exception as e:
    print(f"❌ Terjadi error: {e}")
