import requests

# Получение URL ngrok
ngrok_url = "http://ngrok:4040/api/tunnels"  # Порт 4040 - это порт веб-интерфейса ngrok
response = requests.get(ngrok_url)
ngrok_data = response.json()
ngrok_url = ngrok_data['tunnels'][0]['public_url']

WEBHOOK_HOST = ''
WEBHOOK_PATH = ''
# WEBHOOK_URL = "https://6b7d-194-0-114-39.ngrok-free.app"
WEBHOOK_URL = f"{ngrok_url}"
# WEBHOOK_URL = ngrok_url
WEBAPP_HOST = '0.0.0.0'  # or ip
WEBAPP_PORT = 7772



