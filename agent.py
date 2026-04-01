import os
import json
from google import genai
from google.genai import types

# --- AYARLAR ---
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_KEY)

def analyze_folder_with_gemini(folder_path):
    """Yeni SDK ile klasördeki görselleri analiz eder."""
    print(f"Klasör analiz ediliyor: {folder_path}")
    
    # Resimleri bul
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
    contents = []
    
    # Resimleri yükle ve içerik listesine ekle
    for img_name in image_files:
        path = os.path.join(folder_path, img_name)
        with open(path, "rb") as f:
            image_data = f.read()
            contents.append(types.Part.from_bytes(data=image_data, mime_type="image/jpeg"))

    prompt = """
    Bu görseller aynı ürüne aittir. Etsy için şunları hazırla:
    1. 140 karakterlik SEO uyumlu Title.
    2. El yapımı vurgulu, emoji içermeyen Description.
    3. Virgülle ayrılmış 13 adet Tags (max 20 karakter).
    Format: Sadece JSON döndür. Örn: {"title": "...", "description": "...", "tags": "..."}
    """
    
    # Yeni SDK çağrısı
    response = client.models.generate_content(
        model='gemini-1.5-flash',
        contents=[prompt] + contents,
        config=types.GenerateContentConfig(
            response_mime_type='application/json' # Otomatik JSON formatı zorlar
        )
    )
    
    return json.loads(response.text)

# ... create_etsy_listing ve diğer fonksiyonlar aynı kalabilir ...
