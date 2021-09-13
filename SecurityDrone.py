import cvlib as cv #오픈Cv 라이브러리 
from cvlib.object_detection import draw_bbox # Cvlib를 사용한 객체 경계 상자
import cv2 #OpenCv 함수 사용을 하기위한 cv2 라이브러리 호출
import time #시간 모듈 사용
import os #os 모듈 사용

from serial import Serial
from cvlib.object_detection import draw_bbox # 웹캠 온

import serial  #시리얼통신 라이브러리
import sys # 시스템 특정 파라미터 및 함수 
import threading #제어 스레드
import queue # 큐모듈 , 다중 생산자 , 다중 소비자 구현

from tkinter import *
from SecurityDrone_SpeedCheck import *
import requests
import json

window = Tk() #창 생성
window.geometry('480x360-500+220') 
ser = serial.Serial('COM5', 800, timeout=1) #아두이노 포트 할당

with open(r"./SendMessage/SD_code.json","r") as fp:
    tokens = json.load(fp)

def opencamera():  #카메라 오픈시 동작 함수
    webcam = cv2.VideoCapture('./드론1.mp4') #카메라 0 웹캠 1 외부 카메라 
    count = 0
    if not webcam.isOpened():
        print("카메라를 열 수 없습니다.")
        exit() #카메라가 연결되지 않으면 종료

    person_risk =0
    car_risk =0
    mortorcycle_risk=0 #각 상황에 따른 위험도 분류
    before =0
    after =0

    while webcam.isOpened():
        status, frame = webcam.read()
        frame = cv2.flip(frame,1) # 영상 좌우 반전 
        
        if not status:
            break
        
        bbox, label, conf = cv.detect_common_objects(frame, confidence=0.25, model='yolov4-tiny')
        #yolov4-tiny를 사용하여 bbox 구현 및 사물 라벨링 

        out = draw_bbox(frame, bbox, label, conf, write_conf=True)
        #검출된 물체 가장자리에 bbox 그리기
        
        cv2.imshow("Real-time object detection", out) #실시간 사물감지 출력 (이미지창 이름 , 파일명)
        
        if label.count('person') >=3 : # 라벨링으로 사람수 카운트
            print('감지된 사람수'+str(label.count('person')))
            print('위험')
            person_risk = 5 # person label이 3이상이거나 같을때 person risk 수를 5로  높힘
        
            if person_risk == 5:
                m ='1'
                m = [m.encode('utf-8')]
                ser.writelines(m) #person risk가 5일때 아두이노 시리얼 통신전달 chr 형식의 1 보냄 (유니코드 인코딩 = utf-8) LED RED ON
                before=after
                after=1

                if before != after:
                    url="https://kapi.kakao.com/v2/api/talk/memo/default/send"
                    headers={
                        "Authorization" : "Bearer " + tokens["access_token"]
                    }
                    data={
                        "template_object": json.dumps({
                            "object_type":"text",
                            "text":"현재 위치에 사람이3명 이상 있습니다",
                            "link":{
                                "web_url":"www.naver.com"
                            }
                        })
                    }
                    response = requests.post(url, headers=headers, data=data)
                    response.status_code
                        
            if(car_risk ==5 or mortorcycle_risk==10):
                m ='5'
                m = [m.encode('utf-8')]
                ser.writelines(m) #person risk를 제외한 다른 위험수치가 증가시 chr 형식의 5 보냄 (유니코드 인코딩 = utf-8) LED RED OFF

        elif label.count('car') >=3 :
            print('감지된 차량수'+str(label.count('car')))
            print('위험')
            car_risk = 5 #차량 라벨 3대이상 감지시 car risk수를 5로 높힘
          
            if car_risk == 5:                
                m ='2'
                m = [m.encode('utf-8')]
                ser.writelines(m) #car risk가 5일때 아두이노 시리얼 통신전달 chr 형식의 2 보냄 (유니코드 인코딩 = utf-8) = LED YEL ON
                before=after
                after=2

                if before != after:
                    url="https://kapi.kakao.com/v2/api/talk/memo/default/send"
                    headers={
                        "Authorization" : "Bearer " + tokens["access_token"]
                    }
                    data={
                        "template_object": json.dumps({
                            "object_type":"text",
                            "text":"현재 위치에 차량이3대 이상 있습니다",
                            "link":{
                                "web_url":"www.naver.com"
                            }
                        })
                    }
                    response = requests.post(url, headers=headers, data=data)
                    response.status_code
                
            if(person_risk ==5 or mortorcycle_risk==10):
                m ='6'
                m = [m.encode('utf-8')]
                ser.writelines(m) #car risk를 제외한 다른 위험수치가 증가시 chr 형식의 6 보냄 (유니코드 인코딩 = utf-8) LED YEL OFF

        elif label.count('motorcycle') >= 1 :
            print('감지된 오토바이수'+str(label.count('motorcycle')))
            print('위험')
            mortorcycle_risk = 10 # 오토바이 1대이상 감지시 motorcycle risk 10으로 높힘
          
            if mortorcycle_risk == 10:
                m ='4'
                m = [m.encode('utf-8')]
                ser.writelines(m) #motorcycle risk가 10일때 아두이노 시리얼 통신전달 chr 형식의 4 보냄 (유니코드 인코딩 = utf-8) = LED BLU ON
                before=after
                after=3

                if before != after:
                    url="https://kapi.kakao.com/v2/api/talk/memo/default/send"
                    headers={
                        "Authorization" : "Bearer " + tokens["access_token"]
                    }
                    data={
                        "template_object": json.dumps({
                            "object_type":"text",
                            "text":"현재 위치에 위험 수준이 높은 오토바이가 있습니다",
                            "link":{
                                "web_url":"www.naver.com"
                            }
                        })
                    }
                    response = requests.post(url, headers=headers, data=data)
                    response.status_code
            
            if(person_risk ==5 or car_risk==10):
                m ='8'
                m = [m.encode('utf-8')]
                ser.writelines(m) #motorcycle risk를 제외한 다른 위험수치가 증가시 chr 형식의 8 보냄 (유니코드 인코딩 = utf-8) LED BLU OFF

        elif label.count('motorcycle') ==0 and label.count('car') ==0 and label.count('person') ==0 :
            print('아무것도 없습니다.'+str( label.count('motorcycle') ==0 and label.count('car') ==0 and label.count('person') ==0))
            before=after
            after=9
            m ='3'
            m = [m.encode('utf-8')]
            ser.writelines(m) #각 라벨 수 비교하여 0일시에 chr 형식의 8 보냄 (유니코드 인코딩 = utf-8)아두이노 lcd에 pass 출력 LED GRE ON
            
            if(person_risk ==5 or car_risk==10 or mortorcycle_risk):
                before=after
                after=10
                m ='7'
                m = [m.encode('utf-8')]
                ser.writelines(m)  #다른 위험수치가 증가시 chr 형식의 7 보냄 (유니코드 인코딩 = utf-8) LED GRE OFF

        if cv2.waitKey(5) == 27: #esc로 코드 종료
            break
    webcam.release() #카메라 메모리 할당 종료 
    cv2.destroyAllWindows()   

def shutdown():
    window.destroy()

window.title("시큐리티드론")
b1 = Button(window, width = 20 , height = 5, font = (20), text='골목길영상촬영', command=opencamera)    
b2 = Button(window, width = 20 , height = 5, font = (20), text ='속도측정', command=trackMultipleObjects)
b3 = Button(window, width = 20 , height = 5, font = (20), text='종료', command=shutdown)

b1.pack(side=TOP ,expand=100, padx= 30)
b2.pack(side=TOP ,expand=100, padx= 30)
b3.pack(side=BOTTOM ,expand=100, padx= 30)

window.mainloop()


