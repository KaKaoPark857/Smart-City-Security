#include <Wire.h>
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27, 16, 2);



void RED_ON(){

  Serial.println("RED ON");
  digitalWrite(A0, HIGH);
  digitalWrite(A1, LOW);
  digitalWrite(A2, LOW);
  digitalWrite(A3, LOW);
}

void RED_OFF(){
  Serial.println("RED OFF");
  digitalWrite(A0, LOW);
}

void YEL_ON(){

  Serial.println("YELLOW ON");
  digitalWrite(A0, LOW);
  digitalWrite(A1, HIGH);
  digitalWrite(A2, LOW);
  digitalWrite(A3, LOW);
}

void YEL_OFF(){
  Serial.println("YELLOW OFF");
  digitalWrite(A1, LOW);
}

void BLU_ON(){

  Serial.println("BLUE ON");
  digitalWrite(A0, LOW);
  digitalWrite(A1, LOW);
  digitalWrite(A2, HIGH);
  digitalWrite(A3, LOW);
}

void BLU_OFF(){
  Serial.println("YELLOW OFF");
  digitalWrite(A2, LOW);
}

void GRE_ON(){
 
  Serial.println("GREEN ON"); 
  digitalWrite(A0, LOW);
  digitalWrite(A1, LOW);
  digitalWrite(A2, LOW);
  digitalWrite(A3, HIGH);
}

void GRE_OFF(){
  Serial.println("GRE OFF");
  digitalWrite(A3, LOW);
}

void LED_OFF()
{
  Serial.println("LED OFF");
  digitalWrite(A0, LOW);
  digitalWrite(A1, LOW);
  digitalWrite(A2, LOW);
  digitalWrite(A3, LOW);
}
void setup() 
{
  
  Serial.begin(800);

  pinMode(A0, OUTPUT);
  pinMode(A1, OUTPUT);
  pinMode(A2, OUTPUT);
  pinMode(A3, OUTPUT);
  lcd.init(); 
  lcd.backlight();

}

int before =0;
int after =0;


void loop() 
{
  
  if(Serial.available()){
    char in_data;
    int change;
    in_data = Serial.read();
    
 
    
    if(in_data=='1'){ // Red on
      before=after;
      after=1;
      if(before != after){
        RED_ON();
        lcd.setCursor(0,0);
        lcd.print("People 3        ");
        lcd.setCursor(0,1);
        lcd.print("around          ");
      }
    }
    else if(in_data=='2'){ //Yellow on
      before=after;
      after=2;
      if(before != after){
        YEL_ON();
        lcd.setCursor(0,0);
        lcd.print("Car 3           ");
        lcd.setCursor(0,1);
        lcd.print("around          ");
      }
    }

    else if(in_data=='3'){ //Green on
      before=after;
      after=3;
      if(before != after){
        GRE_ON();
        lcd.setCursor(0,0);
        lcd.print("PASS            ");
        lcd.setCursor(0,1);
        lcd.print("                ");
      }
    }
    else if(in_data=='4'){ //Blue on
      before=after;
      after=4;
      if(before!=after){
        BLU_ON();
        lcd.setCursor(0,0);
        lcd.print("Motorcycle      ");
        lcd.setCursor(0,1);
        lcd.print("around          ");
      }
    }
    
    else if(in_data=='5'){ // Red off
      before=after;
      after=5;
      if(before !=after){  
      RED_OFF();}
    }
     else if(in_data=='6'){ //Yellow off
      before=after;
      after=6;
      if(before !=after){  
      YEL_OFF();}
      
    }
     else if(in_data=='7'){ //Green off
      before=after;
      after=7;
      if(before !=after){  
      GRE_OFF();}
      
    }
     else if(in_data=='8'){ //Blue off
      before=after;
      after=5;
      if(before !=after){  
      BLU_OFF();}
      
    }
    else if(in_data=='9'){
      LED_OFF();
    }

  
  }
}
