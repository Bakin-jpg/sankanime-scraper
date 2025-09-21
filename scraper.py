from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    url = "https://sankanime.com/watch/nine-rulers-crown-19741"
    
    page.goto(url)
    print("🚀 Halaman terbuka, menunggu player muncul...")
    
    # Tunggu player video muncul
    page.wait_for_selector('.art-video-player', timeout=20000)
    print("✅ Player ditemukan!")
    
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
    
    # Ambil semua opsi resolusi
    qualities = page.query_selector_all('.art-setting-item')
    for q in qualities:
        text = q.inner_text().strip()
        if any(res in text for res in ['360p', '480p', '720p', '1080p']):
            print(f"Ditemukan: {text}")
    
    browser.close()
