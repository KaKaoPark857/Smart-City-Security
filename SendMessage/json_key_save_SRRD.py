# 사용자 토큰받아서 json파일에 저장하기
import requests

url = 'https://kauth.kakao.com/oauth/token'

#https://kauth.kakao.com/oauth/authorize?client_id=5ee51d1a6a55ed4b66bfceca898b94ac&redirect_uri=https://textsendkakaotalklink.netlify.app&response_type=code
rest_api_key = '5ee51d1a6a55ed4b66bfceca898b94ac' #REST API키 도로파손
redirect_uri = 'https://textsendkakaotalklink.netlify.app'
authorize_code = 'qKgzB65WduUsnyVrVj6WN6qfbOhns7cj1YazgUeI9G-L-rsFKtJ3TrKTBcUXAqJB9A5Y1go9dBEAAAF8LyW_Cw'



data = {
    'grant_type':'authorization_code',
    'client_id':rest_api_key,
    'redirect_uri':redirect_uri,
    'code': authorize_code,
    }

response = requests.post(url, data=data)
tokens = response.json()
print(tokens)

# # json 저장
import json
# #1.
with open(r"./SendMessage/SRRD_Code.json","w") as fp: #저장시킬 프로그램의 경로 지정
    json.dump(tokens, fp)
    #도로파손

