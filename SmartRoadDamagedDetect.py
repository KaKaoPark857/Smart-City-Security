# 동영상 프로세싱
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
    model_filename = './converted_keras/keras_model.h5'
    model = tensorflow.keras.models.load_model(model_filename)

    capture = cv2.VideoCapture("./테스트 영상/testRoadvideo.mp4") #10

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

def shutdown():
    window.destroy()

window = Tk()
window.title("TrafficLight")
window.geometry("480x250-500+220")
    
btn1 = Button(window, text='실행', height = 5, width = 25,font = (40),command=SmartRoadDamagedDetect) # 버튼을 올릴 장소, 버튼에 들어갈 내용
btn2 = Button(window, text='종료',height = 5, width = 25,font = (40), command=shutdown)
    
btn1.pack() # auto 위치 지정
btn2.pack()
    
window.mainloop()