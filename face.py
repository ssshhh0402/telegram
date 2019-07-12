import requests 
import pprint
from decouple import config
img_url = "https://api.telegram.org/file/bot815471355:AAEXs3TbfrpoVRbYTUFHlTFzzddYjSAz_44/photos/file_2.jpg"

image = requests.get(img_url)
response = requests.get(img_url, stream = True)
image = response.raw.read()
naver_client_id = config('NAVER_CLIENT_ID')
naver_client_secret = config('NAVER_CLIENT_SECRET')
naver_url = 'https://openapi.naver.com/v1/vision/celebrity'

headers = {
    'X-Naver-Client-Id': naver_client_id,
    'X-Naver-Client-Secret' : naver_client_secret
}

response = requests.post(naver_url, headers = headers, files = {'image': image}).json()
pprint.pprint(response)
best = response.get('faces')[0].get('celebrity')
confidence = best.get('confidence')
value = best.get('value')
text = f'{confidence}만큼 {value}를 닮으셨습니다.'

print(text)
