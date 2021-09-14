# 사용자 토큰받아서 json파일에 저장하기
import requests

url = 'https://kauth.kakao.com/oauth/token'

#https://kauth.kakao.com/oauth/authorize?client_id=5ee51d1a6a55ed4b66bfceca898b94ac&redirect_uri=https://textsendkakaotalklink.netlify.app&response_type=code
# rest_api_key = '5ee51d1a6a55ed4b66bfceca898b94ac' #REST API키 도로파손
# redirect_uri = 'https://textsendkakaotalklink.netlify.app'
# authorize_code = 'RKCJ5uZMXKBo5Lc3XzKnMEkqqHiQtLTdlfqqLS9xcrgv9boc6kfoZi1uMc-lyQzYKZm1Vwo9dJcAAAF7v1-m8g'

#https://kauth.kakao.com/oauth/authorize?client_id=7cdbc1360d5a7d19a7db149dc32f9994&redirect_uri=https://example.com/oauth&response_type=code
rest_api_key = '7cdbc1360d5a7d19a7db149dc32f9994' #REST API키 정찰드론
redirect_uri = 'https://example.com/oauth'
authorize_code = 'fAUt3v7HomFTgLOfF8R-9a24FEKocffH3BCkc-3KjaiFxk3lr36dA7q52VjzFbSD1aJqSAo9c5sAAAF7v2Ipyw'



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
# with open(r"./SendMessage/SRRD_Code.json","w") as fp: #저장시킬 프로그램의 경로 지정
#     json.dump(tokens, fp)
    #도로파손

with open(r"./SendMessage/SD_code.json","w") as fp: #저장시킬 프로그램의 경로 지정
    json.dump(tokens, fp)
    #정찰드론