//String dicid;
int input_port=4;
int output_port1_relay = 11;
int output_port2_led2 = 12;
//int face=0;
int output_port3_led1 =10;

void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);
pinMode(input_port,INPUT);
pinMode(A2,INPUT);
//digitalWrite(input_port,LOW);
pinMode(output_port1_relay,OUTPUT);
digitalWrite(output_port1_relay,HIGH);
pinMode(output_port2_led2,OUTPUT);
pinMode(output_port3_led1,OUTPUT);
//digitalWrite(relay_pin,LOW);
}

void loop() {
  // put your main code here, to run repeatedly:
  //int flag = digitalRead(input_port);
if(analogRead(A2)>700){
  //digitalWrite(output_port,HIGH);

  check();
  //break;
}
//delay(10000);
// digitalWrite(output_port,LOW);

}

void check() { 
  char data = 0;

 
 if(Serial.available())
 {
  data =Serial.read();
 
 Serial.println(data);
 char face=data;
 //int face = data;
 if(face == '1') {

 digitalWrite(output_port1_relay,HIGH);
 digitalWrite(output_port3_led1,HIGH);
 digitalWrite(output_port2_led2,LOW);
 delay(10000);
 digitalWrite(output_port1_relay,LOW); //condition to stop relay after sometime
 digitalWrite(output_port3_led1,LOW);
 digitalWrite(output_port2_led2,HIGH);
 face='2'; //condition to stop relay after sometime, disable both statements to switch relay forever

 Serial.println("Unlocked");
 }
 else {
 digitalWrite(output_port1_relay,LOW);
 digitalWrite(output_port3_led1,LOW);
 digitalWrite(output_port2_led2,HIGH);
 Serial.println("Wrong");
}
Serial.end();
 }
 return;
}
