import requests
from decouple import config
import pprint

naver_client_id  = config("NAVER_CLINT_ID")
naver_client_secret = config("NAVER_CLIENT_SECRET")
naver_url = 'https://openapi.naver.com/v1/papago/n2mt'
headers = {'X-Naver-Client-Id' : naver_client_id,
'X-Naver-Client-Secret': naver_client_secret}

data = {
    'source' : 'ko',
    'target': 'en',
    'text': '띵작'

}
response = requests.post(naver_url, headers = headers, data= data).json()
pprint.pprint(response.get('message').get('result').get('translatedText'))
