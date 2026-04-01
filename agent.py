import os
import json
import google.generativeai as genai
import requests

# --- AYARLAR (GitHub Secrets'tan alınır) ---
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
ETSY_KEY = os.getenv("ETSY_KEYSTRING")
ETSY_SECRET = os.getenv("ETSY_SHARED_SECRET")
SHOP_ID = os.getenv("ETSY_SHOP_ID")

genai.configure(api_key=GEMINI_KEY)

def analyze_folder_with_gemini(folder_path):
    """Klasördeki tüm görsellere bakıp ortak bir ilan içeriği üretir."""
    model = genai.GenerativeModel('gemini-1.5-flash')
    files_to_upload = []
    
    # Klasördeki tüm resimleri analiz için hazırla
    images = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
    
    for img_name in images:
        path = os.path.join(folder_path, img_name)
        files_to_upload.append(genai.upload_file(path))
    
    prompt = """
    Bu klasördeki tüm fotoğraflar AYNI ÜRÜNE aittir. 
    Lütfen tüm açılara bakarak Etsy için:
    1. 140 karakterlik SEO uyumlu bir Title.
    2. El yapımı vurgulu, emoji içermeyen bir Description.
    3. Virgülle ayrılmış 13 adet Tags (max 20 karakter).
    Format: Sadece şu JSON yapısını döndür: {"title": "", "description": "", "tags": ""}
    """
    
    response = model.generate_content([prompt] + files_to_upload)
    return json.loads(response.text)

def create_etsy_listing(data):
    """Etsy'de ana taslağı oluşturur ve listing_id döndürür."""
    # OAuth 2.0 Token işlemleri burada devreye girer (Daha önce konuştuğumuz token_alici.py ile alınan token kullanılmalı)
    # Şimdilik yapıyı kuruyoruz:
    url = f"https://openapi.etsy.com/v3/application/shops/{SHOP_ID}/listings"
    headers = {"x-api-key": ETSY_KEY} # V3 için Authorization: Bearer {token} gerekecek
    
    payload = {
        "quantity": 1,
        "title": data['title'],
        "description": data['description'],
        "price": "45.00", # Dinamik hale getirilebilir
        "who_made": "i_did",
        "is_supply": False,
        "when_made": "made_to_order",
        "state": "draft",
        "taxonomy_id": 1234, # Bu numara 'Tablecloth' veya 'Slippers' için değişir
        "tags": data['tags']
    }
    # r = requests.post(url, json=payload, headers=headers)
    # return r.json()['listing_id']
    print(f"Taslak oluşturuldu: {data['title']}")
    return "MOCK_LISTING_ID"

def upload_media_to_listing(listing_id, folder_path):
    """Klasördeki tüm fotoğraf ve videoları ilana yükler."""
    for file in os.listdir(folder_path):
        full_path = os.path.join(folder_path, file)
        
        if file.lower().endswith(('.jpg', '.jpeg', '.png')):
            print(f"Fotoğraf yükleniyor: {file}")
            # Etsy Image Upload API çağrısı buraya gelecek
            
        elif file.lower().endswith(('.mp4', '.mov')):
            print(f"Video yükleniyor: {file}")
            # Etsy Video Upload API çağrısı buraya gelecek

if __name__ == "__main__":
    # Örnek: images içindeki ilk alt klasörü bul
    base_dir = "images"
    subfolders = [f.path for f in os.scandir(base_dir) if f.is_dir()]
    
    if subfolders:
        target_folder = subfolders[0] # Şimdilik ilk klasörü işle
        print(f"İşleniyor: {target_folder}")
        
        content = analyze_folder_with_gemini(target_folder)
        l_id = create_etsy_listing(content)
        upload_media_to_listing(l_id, target_folder)
