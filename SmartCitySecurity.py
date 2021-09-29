from tkinter import *

#골목길 사고방지 import
import cvlib as cv
from cvlib.object_detection import draw_bbox
import cv2

#골목길 사고방지 Arduino
import serial
# arduino = serial.Serial('COM4', 9600)
# def person(diff_cnt, max_diff,cp,cc,ct,cm,cb):    
#     if cp>0 or cc>0 or ct or cm>0 or cb>0: #사람이 있을 때
#         if diff_cnt > max_diff:#움직임이 감지 되었을 때
#             m ='1'
#             m = [m.encode('utf-8')]
#             arduino.writelines(m)
#         else: #움직임이 감지 되지 않았을 때 
#             m ='2'
#             m = [m.encode('utf-8')]
#             arduino.writelines(m)
#     #위험 효소가 아무것도 없을 때
#     elif cp==0 & cc==0 &ct==0 & cm==0 & cb==0:
#         m ='3'
#         m = [m.encode('utf-8')]
#         arduino.writelines(m)

# def end_arduino():
#     m ='4'
#     m = [m.encode('utf-8')]
#     arduino.writelines(m)

#골목길 사고방지 코드
def RoadTrafficLight(): 
    thresh = 25
    max_diff = 200
    
    a, b, c = None, None, None
    url = './테스트 영상/roadtrafficlight.mp4'
    cap = cv2.VideoCapture(url)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
    
    if cap.isOpened():
        ret, a = cap.read()
        a= cv2.flip(a,1)
        
        ret, b = cap.read()
        b = cv2.flip(b,1) 

        while ret:
            if not ret:
                break

            ret, c = cap.read()
            c= cv2.flip(c,1) 
            
            # opencv를 통한 물체인식
            bbox, label, conf = cv.detect_common_objects(a, confidence=0.25, model='yolov4-tiny')
            # 검출된 물체 가장자리에 바운딩 박스 그리기
            out = draw_bbox(a, bbox, label, conf, write_conf=True)
            # 프레임을 흑백으로 바꾸어 움직이는 부분들을 흰색으로 바꾸어 비교함
            a_gray = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY)
            b_gray = cv2.cvtColor(b, cv2.COLOR_BGR2GRAY)
            c_gray = cv2.cvtColor(c, cv2.COLOR_BGR2GRAY)
    
            diff1 = cv2.absdiff(a_gray, b_gray)
            diff2 = cv2.absdiff(b_gray, c_gray)
    
            ret, diff1_t = cv2.threshold(diff1, thresh, 255, cv2.THRESH_BINARY)
            ret, diff2_t = cv2.threshold(diff2, thresh, 255, cv2.THRESH_BINARY)
    
            diff = cv2.bitwise_and(diff1_t, diff2_t)
    
            k = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
            diff = cv2.morphologyEx(diff, cv2.MORPH_OPEN, k)

            diff_cnt = cv2.countNonZero(diff)
    
            a = b
            b = c
            
            # 사람수와 탈 것의 수를 측정
            cp=label.count('person') 
            cc=label.count('car')
            ct=label.count('truck') 
            cm=label.count('motorcycle')
            cb=label.count('bicycle')
            # 아두이노에 값 전달
            #person(diff_cnt,max_diff,cp,cc,ct,cm,cb)
            
            # 판별한 물체 박스 출력 실행
            cv2.imshow("Real-time object detection",out)
            
            if cv2.waitKey(10) & 0xFF == 27 :
                # end_arduino()
                cap.release()
                cv2.destroyAllWindows() 
                break

#정찰 드론 import
import cvlib as cv #오픈Cv 라이브러리 
from cvlib.object_detection import draw_bbox # Cvlib를 사용한 객체 경계 상자
import cv2 #OpenCv 함수 사용을 하기위한 cv2 라이브러리 호출
import time #시간 모듈 사용
import os #os 모듈 사용

from cvlib.object_detection import draw_bbox # 웹캠 온

import serial  #시리얼통신 라이브러리
import sys # 시스템 특정 파라미터 및 함수 
import threading #제어 스레드
import queue # 큐모듈 , 다중 생산자 , 다중 소비자 구현

from tkinter import *
import requests
import json

WIDTH = 1280	
HEIGHT = 720 #캠사이즈 조절

#정찰 드론 코드
# ser = serial.Serial('COM5', 800, timeout=1) #아두이노 포트 할당
with open(r"./SendMessage/SD_code.json","r") as fp:
    tokens = json.load(fp)

def SecurityDrone():  #카메라 오픈시 동작 함수
    webcam = cv2.VideoCapture('./테스트 영상/Drone.mp4') #카메라 0 웹캠 1 외부 카메라 

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
        #frame = cv2.flip(frame,1) # 영상 좌우 반전 
        frame = cv2.resize(frame, (WIDTH, HEIGHT))

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
                # m ='1'
                # m = [m.encode('utf-8')]
                # ser.writelines(m) #person risk가 5일때 아두이노 시리얼 통신전달 chr 형식의 1 보냄 (유니코드 인코딩 = utf-8) LED RED ON
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
                        
            # if(car_risk ==5 or mortorcycle_risk==10):
            #     m ='5'
            #     m = [m.encode('utf-8')]
            #     ser.writelines(m) #person risk를 제외한 다른 위험수치가 증가시 chr 형식의 5 보냄 (유니코드 인코딩 = utf-8) LED RED OFF

        elif label.count('car') >=3 :
            print('감지된 차량수'+str(label.count('car')))
            print('위험')
            car_risk = 5 #차량 라벨 3대이상 감지시 car risk수를 5로 높힘
          
            if car_risk == 5:                
                # m ='2'
                # m = [m.encode('utf-8')]
                # ser.writelines(m) #car risk가 5일때 아두이노 시리얼 통신전달 chr 형식의 2 보냄 (유니코드 인코딩 = utf-8) = LED YEL ON
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
                
            # if(person_risk ==5 or mortorcycle_risk==10):
            #     m ='6'
            #     m = [m.encode('utf-8')]
            #     ser.writelines(m) #car risk를 제외한 다른 위험수치가 증가시 chr 형식의 6 보냄 (유니코드 인코딩 = utf-8) LED YEL OFF

        elif label.count('motorcycle') >= 1 :
            print('감지된 오토바이수'+str(label.count('motorcycle')))
            print('위험')
            mortorcycle_risk = 10 # 오토바이 1대이상 감지시 motorcycle risk 10으로 높힘
          
            if mortorcycle_risk == 10:
                # m ='4'
                # m = [m.encode('utf-8')]
                # ser.writelines(m) #motorcycle risk가 10일때 아두이노 시리얼 통신전달 chr 형식의 4 보냄 (유니코드 인코딩 = utf-8) = LED BLU ON
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
            
            # if(person_risk ==5 or car_risk==10):
            #     m ='8'
            #     m = [m.encode('utf-8')]
            #     ser.writelines(m) #motorcycle risk를 제외한 다른 위험수치가 증가시 chr 형식의 8 보냄 (유니코드 인코딩 = utf-8) LED BLU OFF

        elif label.count('motorcycle') ==0 and label.count('car') ==0 and label.count('person') ==0 :
            print('아무것도 없습니다.'+str( label.count('motorcycle') ==0 and label.count('car') ==0 and label.count('person') ==0))
            before=after
            after=9
            # m ='3'
            # m = [m.encode('utf-8')]
            # ser.writelines(m) #각 라벨 수 비교하여 0일시에 chr 형식의 8 보냄 (유니코드 인코딩 = utf-8)아두이노 lcd에 pass 출력 LED GRE ON
            
            if(person_risk ==5 or car_risk==10 or mortorcycle_risk):
                before=after
                after=10
                # m ='7'
                # m = [m.encode('utf-8')]
                # ser.writelines(m)  #다른 위험수치가 증가시 chr 형식의 7 보냄 (유니코드 인코딩 = utf-8) LED GRE OFF

        if cv2.waitKey(5) == 27: #esc로 코드 종료
            break
    webcam.release() #카메라 메모리 할당 종료 
    cv2.destroyAllWindows()   

#정찰 드론 속도 체크
import cv2 #OpenCv 함수 사용을 하기위한 cv2 라이브러리 호출
import dlib #dlib
import time #시간 모듈 사용
import math #math 모듈 호출
import requests
import json

carCascade = cv2.CascadeClassifier('carexample.xml') 
#차량 검출을 위한 carexample 학습 데이터를 사용하여
video = cv2.VideoCapture('./테스트 영상/Highway.mp4')
#카메라 0 웹캠 1 외부 카메라 (라즈베리파이 스트리밍 주소)

WIDTH = 1280	
HEIGHT = 720 #캠사이즈 조절

with open(r"./SendMessage/SD_code.json","r") as fp:
    tokens = json.load(fp)

def estimateSpeed(location1, location2):
	d_pixels = math.sqrt(math.pow(location2[0] - location1[0], 2) + math.pow(location2[1] - location1[1], 2))
	#처음 위치(픽셀크기) 와 두번째 자리(픽셀 크기)에 대해서 두번째 위치 - 첫번째 위치를 통해 이동 거리 계산
	ppm = 8.8
	# ppm = location2[2] / carWidht로 도로길이 m 단위단위로 입력 도로교통공사 규격 4차선 같은경우는 14m
	d_meters = d_pixels / ppm 
	#픽셀의 크기에 도로 크기를 나누어 차량의 크기 계산
	print("d_pixels=" + str(d_pixels), "d_meters=" + str(d_meters)) # 계산된 픽셀의 크기와 물체 크기 
	fps = 15
	speed = d_meters * fps * 3.6 
	#초당 1미터 = 시속 3.6km m/s에 대하여 km/h로 변환 
	return speed

def SecurityDroneSpeedCheck():
	rectangleColor = (0, 205, 0) # 박스 색 설정
	frameCounter = 0
	currentCarID = 0
	fps = 0
	
	streetmaxspeed=[25]
	carTracker = {}
	carNumbers = {}
	carLocation1 = {}
	carLocation2 = {}
	speed = [None] * 1000  
	#각 오브젝트에 대한 배열 선언
	
	before = 0
	after = 0
	out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (WIDTH,HEIGHT))
    #영상 저장을 위해 선언 cv2.VideoWriter_fourcc(*'MJPG) 로 대체가능

	while True:
		start_time = time.time()
		rc, image = video.read()
		if type(image) == type(None):
			break
		
		image = cv2.resize(image, (WIDTH, HEIGHT))
		resultImage = image.copy()
		#처리 속도를 높이기 위해 프레임 크기를 변환
		frameCounter = frameCounter + 1
		carIDtoDelete = []

		for carID in carTracker.keys():
			trackingQuality = carTracker[carID].update(image)
			
			if trackingQuality < 5: 
				carIDtoDelete.append(carID)
			#추적하는 물체에 대한 퀄리티에 대해 임계값 7 아래인 물체 삭제	

		for carID in carIDtoDelete:
			print ('Removing carID ' + str(carID) + '추적 목록제거')
			print ('Removing carID ' + str(carID) + '이전 위치제거')
			print ('Removing carID ' + str(carID) + '현재 위치제거')
			
			carTracker.pop(carID, None)
			carLocation1.pop(carID, None)
			carLocation2.pop(carID, None)
		
		if not (frameCounter % 1):
			gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			cars = carCascade.detectMultiScale(gray, 5,4,4,(2,6))
			#영상 회색으로 변환하여서 번호판() 검출된 물체에 대해서 cars로 지정
			#1.1은 이미지 크기에 대한 보정값 , 13~18은 번호판 간격에대한 최소 픽셀크기 , (24,24)는 번호판의 최소크기

			for (_x, _y, _w, _h) in cars:
				x = int(_x)
				y = int(_y)
				w = int(_w)
				h = int(_h)
			    #사각형에 대한 x,y는 이미지를 기준으로 인식 창의 왼쪽 상단 모서리 좌표 w, h는 하위 창의 너비와 높이
				x_bar = x + 0.5 * w
				y_bar = y + 0.5 * h
				#사각형 그리기
				matchCarID = None
			
				for carID in carTracker.keys():
					trackedPosition = carTracker[carID].get_position()
					
					t_x = int(trackedPosition.left())
					t_y = int(trackedPosition.top())
					t_w = int(trackedPosition.width())
					t_h = int(trackedPosition.height())
					
					t_x_bar = t_x + 0.5 * t_w
					t_y_bar = t_y + 0.5 * t_h
				
					if ((t_x <= x_bar <= (t_x + t_w)) and (t_y <= y_bar <= (t_y + t_h)) and (x <= t_x_bar <= (x + w)) and (y <= t_y_bar <= (y + h))):
						matchCarID = carID
				    #사각형을 그리는 조건과 인식한 사물의 크기가 어느정도 같으면 차량으로 판단 및 추적
				if matchCarID is None:
					print ('새로운 차량을 추적합니다' + str(currentCarID))
					
					tracker = dlib.correlation_tracker()
					tracker.start_track(image, dlib.rectangle(x, y, x + w, y + h))
					#차량이 인식시 차량의 위치가 사각형 형태로 반환되며 직사각형 표시로 차량을 식별
					carTracker[currentCarID] = tracker
					carLocation1[currentCarID] = [x, y, w, h]
					currentCarID = currentCarID + 1

		for carID in carTracker.keys():
			trackedPosition = carTracker[carID].get_position()
					
			t_x = int(trackedPosition.left())
			t_y = int(trackedPosition.top())
			t_w = int(trackedPosition.width())
			t_h = int(trackedPosition.height())
			
			cv2.rectangle(resultImage, (t_x, t_y), (t_x + t_w, t_y + t_h), rectangleColor, 4)
			
			carLocation2[carID] = [t_x, t_y, t_w, t_h]
		    #속도 측정 (시작 지점에서 떨어진 두번째 지점)
		end_time = time.time()
		
		if not (end_time == start_time):
			fps = 1.0/(end_time - start_time) 
			#인식 시간 비교하여 프레임으로 나누어 속도 계산
		
		for i in carLocation1.keys():	
			if frameCounter % 1 == 0:
				[x1, y1, w1, h1] = carLocation1[i]
				[x2, y2, w2, h2] = carLocation2[i]
						
				carLocation1[i] = [x2, y2, w2, h2]
						
				if [x1, y1, w1, h1] != [x2, y2, w2, h2]:
					if (speed[i] == None or speed[i] == 0) and y1 >= 275 and y1 <= 285:
						speed[i] = estimateSpeed([x1, y1, w1, h1], [x2, y2, w2, h2])

					#if y1 > 275 and y1 < 285:
					if speed[i] != None and y1 >= 250:
						cv2.putText(resultImage, str(int(speed[i])) + " km/h", (int(x1 + w1/2), int(y1-5)),cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
						print(before,after)
						
						if speed[i] > 25:
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
										"text":"제한 속도 25km/h 이상차량을 발견하였습니다.",
										"link":{
											"web_url":"www.naver.com"
										}
									})
								}
								response = requests.post(url, headers=headers, data=data)
								response.status_code
						else:
							before =after
							after=0							
		cv2.imshow('result', resultImage)

		if cv2.waitKey(33) == 27: #ESC 입력시 종료
			break
	cv2.destroyAllWindows()


#도로 파손 알림
import cv2
import tensorflow.keras
import numpy as np
import datetime
from tkinter import *

def preprocessing(frame,confidence=0.25, model='yolov3-tiny'):
    # 사이즈 조정
    size = (224, 224)
    frame_resized = cv2.resize(frame, size, interpolation=cv2.INTER_AREA)
    
    # 이미지 정규화
    frame_normalized = (frame_resized.astype(np.float32) / 127.0) - 1
    
    # 이미지 차원 재조정 - 예측을 위해 reshape 해줍니다.
    frame_reshaped = frame_normalized.reshape((1, 224, 224, 3))
    
    return frame_reshaped
 #학습된 데이터 경로

def SmartRoadDamagedDetect():
    model_filename = './데이터/Converted_keras/keras_model.h5'
    model = tensorflow.keras.models.load_model(model_filename)

    capture = cv2.VideoCapture("./테스트 영상/smartroaddamageddetect.mp4") #10

    width = int(capture.get(3))  # 가로

    height = int(capture.get(4))  # 세로값 가져와서

    i = 1 # 첫번째 사진부터 출력하기 위한 초기화
    count = 101 #초기 카운트값 100보다 커야하므로 설정
    while (capture.isOpened):
        ret, frame = capture.read()
        #frame = cv2.flip(frame,1) #영상 좌우반전
        if ret == False:
            break
        cv2.imshow("VideoFrame", frame) #비디오 화면 출력
        frame_fliped = cv2.flip(frame, 1)
        key = cv2.waitKey(33)  # 1) & 0xFF
        now = datetime.datetime.now().strftime("%y_%m_%d-%H-%M-%S") #현재 날짜 시간 출력
        #데이터 전처리
        preprocessed = preprocessing(frame_fliped)
        #예측
        prediction = model.predict(preprocessed)
    # 사진을 damaged가 있으면 찍고 30초 후에 존재할 경우 또 찍는다.
    #640/360
        if prediction[0,0] < prediction[0,1]:
            if count > 10:
                #for i in range(1,51):
                print("Damaged")
                cv2.IMREAD_UNCHANGED
                url = "./SRDD_HTML/screenshot/" + "SRDD (" + str(i) + ").jpg" #파일 저장 경로
                res = cv2.resize(frame,dsize=(640,360),interpolation=cv2.INTER_AREA) #저장 할 이미지 크기 변경
                cv2.putText(res,now,(0,40),cv2.FONT_HERSHEY_DUPLEX,1,(255,255,255),2,cv2.LINE_AA) #사진 읽어오기, 현재시간, 위치, 폰트, 글자크기
                cv2.imwrite(url, res) #이미지 저장
                i += 1
                count = 0
                if i >= 1000: #50개 까지 캡처
                    break
                else:
                    continue
        else: 
            print("NoDamaged")
            print(count)
            count+=1

        if count>1000:  # 데이터가 크면 오류의 위험으로 인해 count(=Nodamaged) 가 1000이 되면 다시 0으로 리셋
            count = 0

        if cv2.waitKey(10) == 27: #esc 눌렀을 때 종료
            break

    capture.release()
    exec(open("./SendMessage/send_message_main.py", encoding='UTF-8').read())

    cv2.destroyAllWindows()

#창닫기
def shutdown():
    root.destroy()

#GUI 부분
# width = 25 , height = 5, font = (25), 
root = Tk()
root.title("SmartCity Control")
root.geometry("1080x720-200+70")

label1 = Label(root, width = 25 , height = 3, font = ("Arial", 25, "bold"), text = 'SmartCity Control')  
label1.place(x=300, y=10)

btn1 = Button(root, width = 25 , height = 5, font = (10), text="Road Traffic Light", command=RoadTrafficLight)
btn1.place(x=10, y=150)

btn2 = Button(root, width = 25 , height = 5, font = (10), text="Security Drone", command=SecurityDrone)
btn2.place(x=400, y=150)

btn3 = Button(root, width = 25 , height = 5, font = (10), text="Security Drone Speed Check", command=SecurityDroneSpeedCheck)
btn3.place(x=400, y=300)

btn4 = Button(root, width = 25 , height = 5, font = (10), text="Smart Road Damaged Detect", command=SmartRoadDamagedDetect)
btn4.place(x=780, y=150)

exitButton = Button(root, width = 25 , height = 5, font = (10), text="Exit Program", command = shutdown)
exitButton.place(x=400, y=450)

root.mainloop() 