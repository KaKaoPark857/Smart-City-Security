import serial
arduino = serial.Serial('COM4', 9600)

def person(diff_cnt, max_diff,cp,cc,ct,cm,cb):    
    if cp>0 or cc>0 or ct or cm>0 or cb>0: #사람이 있을 때
        if diff_cnt > max_diff:#움직임이 감지 되었을 때
            m ='1'
            m = [m.encode('utf-8')]
            arduino.writelines(m)
        else: #움직임이 감지 되지 않았을 때 
            m ='2'
            m = [m.encode('utf-8')]
            arduino.writelines(m)
    #위험 효소가 아무것도 없을 때
    elif cp==0 & cc==0 &ct==0 & cm==0 & cb==0:
        m ='3'
        m = [m.encode('utf-8')]
        arduino.writelines(m)
        
def end_arduino():
    m ='4'
    m = [m.encode('utf-8')]
    arduino.writelines(m)

