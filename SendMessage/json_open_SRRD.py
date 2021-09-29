import json 
# #1.
with open(r"./SendMessage/SRRD_Code.json","r") as fp: #앞에 세이브에서 저장한 코드값을 찾아옴
    ts = json.load(fp)
print(ts)
print(ts["access_token"])

