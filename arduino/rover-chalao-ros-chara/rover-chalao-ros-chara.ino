/* software ---->
 A -> left
 B -> right

 A1 -> front
 A2 -> back

 B1 -> front
 B2 -> back

 

*/

int x, z,fr,fl,br,bl;



// left
#define ARPWM 6
#define ALPWM 9
#define A1ENRF 7
#define A2ENBL 12

// right
#define BRPWM 3
#define BLPWM 5
#define B1ENLF 10
#define B2ENBR 2

#define speed 200


void adjust_speed(float spd_x, float spd_z) 
{

  spd_x = 200*spd_x;
  spd_z = 40*spd_z;
  //depending on sign of x ,either forward-right or backward-right
  if(spd_z>0)  // increase speed of right motors , decrease speed of left motors for right rotation 
  {
   fr=spd_x+spd_z;   // need multiply with constants (fr=param1*spd_x+param2*spd_z), change it later
   br=spd_x+spd_z;
   fl=spd_x-spd_z;
   bl=spd_x-spd_z;   
  }
  //depending on sign of x, either forward-left or backward-left
  if(spd_z<0)  // increase speed of left motors , decrease speed of right motors for left rotation
  {
   fr=spd_x-abs(spd_z);
   br=spd_x-abs(spd_z);
   fl=spd_x+abs(spd_z);
   bl=spd_x+abs(spd_z);   
  }
}

void drive_rover_forward(int spd_left, int spd_right)
{
  analogWrite(A1ENRF, 255);
  analogWrite(A2ENBL, 255);
  analogWrite(B1ENLF, 255);
  analogWrite(B2ENBR, 255);

  digitalWrite(ALPWM, LOW);
  analogWrite(ARPWM,spd_left);
  digitalWrite(BLPWM, LOW);
  analogWrite(BRPWM,spd_right); 
}

void drive_rover_backward(int spd_left, int spd_right)
{
  analogWrite(A1ENRF, 255);
  analogWrite(A2ENBL, 255);
  analogWrite(B1ENLF, 255);
  analogWrite(B2ENBR, 255);

  digitalWrite(ARPWM, LOW);
  analogWrite(ALPWM,spd_left);
  digitalWrite(BRPWM, LOW);
  analogWrite(BLPWM,spd_right); 
}





void velCallback(){

  float x = 0.8;
  float z = 0.0;

  if (x>0) //checking if forward
  {
      adjust_speed(x,z); // adjust the speed for forward-right and forward-left movement
      drive_rover_forward(fl,fr);
  }

  else if (x<0) //checking if backward
  {
      
    adjust_speed(abs(x),z); // the sign only indicates directtion
    drive_rover_backward(fl,fr);
  }
   
  }


void setup() {
  Serial.begin(9600);
  // Set motor connections as outputs
  pinMode(ARPWM, OUTPUT);
  pinMode(ALPWM, OUTPUT);
  pinMode(BRPWM, OUTPUT);
  pinMode(BLPWM, OUTPUT);
  pinMode(A1ENRF, OUTPUT);
  pinMode(A2ENBL, OUTPUT);
  pinMode(B1ENLF, OUTPUT);
  pinMode(B2ENBR, OUTPUT);

  pinMode(LED_BUILTIN, OUTPUT);

}

void loop() {
  if(Serial.available()>0){
    
    velCallback();
    digitalWrite(LED_BUILTIN, HIGH);
    delay(5000);
    digitalWrite(LED_BUILTIN, LOW);

  }
}