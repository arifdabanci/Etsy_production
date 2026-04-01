import hashlib
import secrets
import base64
import requests
from requests_oauthlib import OAuth2Session

# Etsy'den aldığın bilgiler
client_id = "7p0thcerzgmj3q98t4ckyj6j" # Keystring
redirect_uri = "https://localhost" # Kayıt ederken yazdığın URL

# Güvenlik için kod üretimi (PKCE)
code_verifier = secrets.token_urlsafe(80)
code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode('utf-8')).digest()).decode('utf-8').replace('=', '')

# 1. İzin Alma Linki Oluştur
scope = ['listings_r', 'listings_w', 'shops_r']
etsy = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
authorization_url, state = etsy.authorization_url("https://www.etsy.com/oauth/connect", 
                                                  code_challenge=code_challenge, 
                                                  code_challenge_method="S256")

print(f"Şu linke tıkla ve izin ver:\n{authorization_url}")
# Tarayıcı seni redirect_uri'ye atacak, oradaki URL'nin sonundaki ?code=... kısmını kopyala.
