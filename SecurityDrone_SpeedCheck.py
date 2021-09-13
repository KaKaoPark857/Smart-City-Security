import cv2 #OpenCv 함수 사용을 하기위한 cv2 라이브러리 호출
import dlib #dlib
import time #시간 모듈 사용
import math #math 모듈 호출
import requests
import json

carCascade = cv2.CascadeClassifier('./carexample.xml') 
#차량 검출을 위한 carexample 학습 데이터를 사용하여
video = cv2.VideoCapture('./주행6.mp4')
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

def trackMultipleObjects():
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
	out = cv2.VideoWriter('outpy.mp4',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (WIDTH,HEIGHT))
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

if __name__ == '__main__':
	trackMultipleObjects()