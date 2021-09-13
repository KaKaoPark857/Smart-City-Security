import cvlib as cv
from cvlib.object_detection import draw_bbox
import cv2
from RoadTrafficLight_aduino import * # arduino_c문 import
from tkinter import *

def open_CV(): 
    thresh = 25
    max_diff = 200
    
    a, b, c = None, None, None
    
    cap = cv2.VideoCapture(0)
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
            person(diff_cnt,max_diff,cp,cc,ct,cm,cb)
            
            # 판별한 물체 박스 출력 실행
            cv2.imshow("Real-time object detection",out)
            
            if cv2.waitKey(10) & 0xFF == 27 :
                end_arduino()
                cap.release()
                cv2.destroyAllWindows() 
                break
    
def shutdown():
    window.destroy()
        
window = Tk()
window.title("TrafficLight")
window.geometry("480x250-500+220")
    
btn1 = Button(window, text='실행', height = 5, width = 25,font = (40),command=open_CV) # 버튼을 올릴 장소, 버튼에 들어갈 내용
btn2 = Button(window, text='종료',height = 5, width = 25,font = (40), command=shutdown)
    
btn1.pack() # auto 위치 지정
btn2.pack()
    
window.mainloop()