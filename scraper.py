import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
from playwright.sync_api import sync_playwright
import time

# Token API ScrapingBee
API_KEY = os.getenv("SCRAPINGBEE_API_KEY")

# URL target episode anime
url = "https://sankanime.com/watch/nine-rulers-crown-19741"

def scrape_with_playwright():
    print("🚀 Memulai scraping dengan Playwright...")
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Buka halaman
            page.goto(url)
            print("✅ Halaman terbuka, menunggu player muncul...")
            
            # Tunggu player video muncul
            page.wait_for_selector('.art-video-player', timeout=30000)
            print("✅ Player ditemukan!")
            
            # Tunggu beberapa detik biar player siap
            time.sleep(5)
            
            # Klik tombol setting
            page.click('.art-control-setting')
            print("🔧 Klik tombol setting...")
            
            # Tunggu menu quality muncul
            page.wait_for_selector('.art-setting-item[data-name="hls-quality"]', timeout=10000)
            print("📁 Menu quality ditemukan!")
            
            # Klik menu quality
            page.click('.art-setting-item[data-name="hls-quality"]')
            print("📂 Klik menu quality...")
            
            # Tunggu opsi resolusi muncul
            page.wait_for_selector('.art-setting-panel', timeout=10000)
            time.sleep(2)
            
            # Ambil semua opsi resolusi
            qualities = page.query_selector_all('.art-setting-item')
            found_links = {}
            
            for q in qualities:
                text = q.inner_text().strip()
                if any(res in text for res in ['360p', '480p', '720p', '1080p']):
                    # Coba ambil link dari atribut data-value atau href
                    link = q.get_attribute('data-value') or q.get_attribute('href')
                    if link:
                        found_links[text] = link
                        print(f"✅ Ditemukan: {text} -> {link}")
            
            browser.close()
            return found_links
            
    except Exception as e:
        print(f"❌ Error saat scraping: {e}")
        return {}

def scrape_with_scrapingbee():
    print("🚀 Memulai scraping dengan ScrapingBee...")
    
    params = {
        'api_key': API_KEY,
        'url': url,
        'render_js': 'true',
        'wait': '30000',
        'wait_for': '.art-video-player',
        'premium_proxy': 'true',
    }
    
    try:
        response = requests.get('https://app.scrapingbee.com/api/v1/', params=params)
        
        if response.status_code == 200:
            print("✅ Berhasil mengambil halaman!")
            soup = BeautifulSoup(response.text, 'html.parser')
            
            qualities = ['360p', '480p', '720p', '1080p']
            found_links = {}
            
            for quality in qualities:
                # Cari elemen yang mengandung teks resolusi
                elements = soup.find_all(text=lambda text: quality in text)
                for elem in elements:
                    parent = elem.parent
                    if parent.name == 'a' and parent.has_attr('href'):
                        found_links[quality] = parent['href']
                        print(f"✅ Ditemukan: {quality} -> {parent['href']}")
            
            return found_links
        else:
            print(f"❌ Gagal mengambil halaman. Status code: {response.status_code}")
            return {}
            
    except Exception as e:
        print(f"❌ Error saat scraping: {e}")
        return {}

def main():
    # Coba scraping dengan Playwright dulu
    result = scrape_with_playwright()
    
    # Kalau Playwright gagal, coba ScrapingBee
    if not result:
        print("⚠️ Playwright gagal, mencoba ScrapingBee...")
        result = scrape_with_scrapingbee()
    
    # Simpan hasil ke JSON
    if result:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"links_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(result, f, indent=2)
        
        print(f"✅ Hasil disimpan ke {filename}")
        print(f"📁 Isi file: {result}")
    else:
        print("❌ Tidak ada link yang ditemukan.")

if __name__ == "__main__":
    main()
