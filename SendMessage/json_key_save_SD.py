# 사용자 토큰받아서 json파일에 저장하기
import requests

url = 'https://kauth.kakao.com/oauth/token'

#https://kauth.kakao.com/oauth/authorize?client_id=7cdbc1360d5a7d19a7db149dc32f9994&redirect_uri=https://example.com/oauth&response_type=code
rest_api_key = '7cdbc1360d5a7d19a7db149dc32f9994' #REST API키 정찰드론
redirect_uri = 'https://example.com/oauth'
authorize_code = 'kYs_OSW25CruhcTJWLjCT0o8wOZYajyEa6HB-pyi-xd6Ae-0xEMMnGYDasi9bEyC6Lk0qwo9dZwAAAF8LyZ6pA'



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
with open(r"./SendMessage/SD_code.json","w") as fp: #저장시킬 프로그램의 경로 지정
    json.dump(tokens, fp)
    #정찰드론