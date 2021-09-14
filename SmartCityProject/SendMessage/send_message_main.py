import requests
import json
#1.

with open(r"./SendMessage/SRRD_code.json","r") as fp: #발급받은 코드값을 불러와서 인증함
    tokens = json.load(fp)
url="https://kapi.kakao.com/v2/api/talk/memo/default/send" #로그인한 카카오톡 아이디로 자기한테 메세지보냄
headers={
    "Authorization" : "Bearer " + tokens["access_token"]
}
data={
    "template_object": json.dumps({
        "object_type":"text",
        "text":"도로 파손으로 인한 보수 요청",
        "link":{
            "web_url":"www.naver.com"
        }
    })
}

response = requests.post(url, headers=headers, data=data)
response.status_code