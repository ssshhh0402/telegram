import requests, pprint
from decouple import config #파이썬에서 환경변수 관리하는 패키지

#1. 토큰 및 기본 URL 설정
token = config('TELEGRAM_TOKEN')
url = f'https://api.telegram.org/bot{token}/'

response = requests.get(url+'GETUPDATES').json()

chat_id = response.get('result')[0].get('message').get('from').get('id')
pprint.pprint(chat_id)

#4. CHAT_ID에 메시지 보내기
    #4-1 요청 보낼 URL 만들기
text = "a;lsdkfj;alksdjf"
api_url = f'{url}sendMessage?chat_id={chat_id}&text={text}'
requests.get(api_url)
    #4-2 REQUESTS 로 보내기