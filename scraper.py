import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

# Token API ScrapingBee
API_KEY = os.getenv("SCRAPINGBEE_API_KEY")

# URL target episode anime
url = "https://sankanime.com/anime/episode-xxx"  # Ganti dengan URL episode yang valid

# Parameter request ke ScrapingBee
params = {
    'api_key': API_KEY,
    'url': url,
    'render_js': 'true',
    'wait': '15000',
    'wait_for': '.app-container',
    'premium_proxy': 'true',
}

try:
    print("🚀 Mengirim request ke ScrapingBee...")
    response = requests.get('https://app.scrapingbee.com/api/v1/', params=params)

    if response.status_code == 200:
        print("✅ Berhasil mengambil halaman!")
        soup = BeautifulSoup(response.text, 'html.parser')

        qualities = ['360p', '480p', '720p', '1080p']
        found_links = {}

        for quality in qualities:
            link_element = soup.find('a', text=quality)
            if link_element and link_element.has_attr('href'):
                found_links[quality] = link_element['href']
                print(f"✅ Ditemukan: {quality} -> {link_element['href']}")

        # Simpan hasil ke JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"links_{timestamp}.json"

        with open(filename, 'w') as f:
            json.dump(found_links, f, indent=2)

        print(f"✅ Hasil disimpan ke {filename}")

    else:
        print(f"❌ Gagal mengambil halaman. Status code: {response.status_code}")

except Exception as e:
    print(f"❌ Terjadi error: {e}")
