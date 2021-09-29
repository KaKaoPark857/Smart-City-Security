void RED_ON(){
  Serial.println("RED ON");
  digitalWrite(A0, HIGH);
  digitalWrite(A1, LOW);
  digitalWrite(A2, LOW);
  
}



void GRE_ON(){
  Serial.println("GREEN ON"); 
  digitalWrite(A0, LOW);
  digitalWrite(A2, HIGH);
  digitalWrite(A1, LOW);
  
}



void YEL_ON(){
  Serial.println("YELLOW ON");
  digitalWrite(A0, LOW);
  digitalWrite(A2, LOW);
  digitalWrite(A1, HIGH);
 
}



void LED_OFF(){
  Serial.println("LED OFF");
  digitalWrite(A0, LOW);
  digitalWrite(A2, LOW);
  digitalWrite(A1, LOW);
}



void setup() {
  Serial.begin(9600);
  pinMode(A0, OUTPUT);
  pinMode(A1, OUTPUT);
  pinMode(A2, OUTPUT);
}

int before = 0;
int after =0;
  
void loop() {
  if(Serial.available()){
    char in_data;
    in_data = Serial.read();

    if(in_data=='1'){ //빨강불on
      before=after;
      after=1;
      if (before !=after){
        RED_ON();
      }   
    }
    else if(in_data=='2'){ //노란불on
      before=after;
      after=2; 
      if (before !=after){
        YEL_ON();
      } 
    }
    else if(in_data=='3'){ //초록불 on
      before=after;
      after=3;
      if (before !=after){
        GRE_ON();
      }
    
    }
    else if(in_data=='4'){
      LED_OFF();
      
    }
  }
}
