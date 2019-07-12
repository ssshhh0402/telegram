from flask import Flask, request
from decouple import config
import requests
import random
import pprint

app = Flask(__name__)
token = config('TELEGRAM_TOKEN')
url = f'https://api.telegram.org/bot{token}'
naver_client_id  = config("NAVER_CLIENT_ID")
naver_client_secret = config("NAVER_CLIENT_SECRET")
naver_url = 'https://openapi.naver.com/v1/papago/n2mt'

@app.route('/')
def telegram():
    return 'OK'


@app.route(f'/{token}', methods = ['POST'])
def telegram2 ():
    response = request.get_json()
    text = response.get('message').get('text')
    chat_id = response.get('message').get('chat').get('id')
    headers = {'X-Naver-Client-Id' : naver_client_id, 'X-Naver-Client-Secret': naver_client_secret}
    if response.get('message').get('photo'):
        file_id = response.get('message').get('photo')[-1].get('file_id')
        file_response = requests.get(f'{url}/getFile?file_id={file_id}').json()
        file_path = file_response.get('result').get('file_path')
        file_url = f'https://api.telegram.org/file/bot{token}/{file_path}'
        image = requests.get(file_url, stream=True).raw.read()

        
        naver_url = 'https://openapi.naver.com/v1/vision/celebrity'
        response = requests.post(naver_url, headers = headers, files = {'image': image}).json()
        if response.get('faces'):
            best = response.get('faces')[0].get('celebrity')
            confidence = best.get('confidence')
            value = best.get('value')
            text = f'{confidence}만큼 {value}를 닮으셨습니다.'
        else:
            text = '사람 아니네'
               
        api_url = f'{url}/sendMessage?chat_id={chat_id}&text= {text}'
        requests.get(api_url)

    elif response.get('message').get('text'):
    
        if '/번역 '== text[0:4] in text :
            data = {'source' : 'ko', 'target': 'en', 'text':text[4:] }
            response = requests.post(naver_url, headers = headers, data= data).json()
            pprint.pprint(response.get('message').get('result').get('translatedText'))
            text = response.get('message').get('result').get('translatedText')
        # 인사말이 오면, 나만의 인사해주기
        elif '안녕' in text or 'hi' in text:
            text = '안녕 나는 봇'

        elif '로또' in text:
            text = sorted(random.sample(range(1,46)),6)

        # 마지막~ url 만들어서 메시지 보내기
        api_url = f'{url}/sendMessage?chat_id={chat_id}&text= {text}'
        requests.get(api_url)
    return 'OK',200



if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug = True)