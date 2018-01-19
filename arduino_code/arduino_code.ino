// Arduino timer CTC interrupt example
// www.engblaze.com

// avr-libc library includes
#include <avr/io.h>
#include <avr/interrupt.h>
 
#define LEDPIN 13
#define LEDPIN2 10

// for checking elapsed time
#include <elapsedMillis.h>

unsigned long timer = 0;
String string_me = "serial ";
String a;
String mini_a;
String string_append = "";
unsigned long i = 0;
unsigned long delay1 = 9000;
unsigned long delay2 = 6000;
unsigned long on1 = 5000;
unsigned long on2 = 9000;
unsigned long time_started1 = 0;
unsigned long time_started2 = 0;

long off1 = 0;
long off2 = 3000;

boolean valve1_delay_passed = false;
boolean valve2_delay_passed = false;
boolean valve3_delay_passed = false;
boolean valve4_delay_passed = false;
boolean valve5_delay_passed = false;
boolean valve6_delay_passed = false;
boolean valve7_delay_passed = false;
boolean valve8_delay_passed = false;

boolean valve1_on_passed = false;
boolean valve2_on_passed = false;
boolean valve3_on_passed = false;
boolean valve4_on_passed = false;
boolean valve5_on_passed = false;
boolean valve6_on_passed = false;
boolean valve7_on_passed = false;
boolean valve8_on_passed = false;

boolean valve1_off_passed = false;
boolean valve2_off_passed = false;
boolean valve3_off_passed = false;
boolean valve4_off_passed = false;
boolean valve5_off_passed = false;
boolean valve6_off_passed = false;
boolean valve7_off_passed = false;
boolean valve8_off_passed = false;

//Time out vars?


boolean start = false;
elapsedMillis timeElapsed;
boolean ledState = LOW;
boolean ledState2 = LOW;
int cont_valves = 0;

void setup()
{
  Serial.begin(9600);
    pinMode(LEDPIN, OUTPUT);
 
    // initialize Timer1
    cli();          // disable global interrupts
    TCCR1A = 0;     // set entire TCCR1A register to 0
    TCCR1B = 0;     // same for TCCR1B
 
    // set compare match register to desired timer count:
    OCR1A = 15.625; //1Khz , 1
    //OCR1A = 7.8; 2Khz, 0.5
    //OCR1A = 3.9; //4KHz, 0.25
    //OCR1A = 3.125; //5KHz, 0.20 
    //OCR1A = 1.5625; //10KHz, 0.1
    // turn on CTC mode:
    TCCR1B |= (1 << WGM12);
    // Set CS10 and CS12 bits for 1024 prescaler:
    TCCR1B |= (1 << CS10);
    TCCR1B |= (1 << CS12);
    // enable timer compare interrupt:
    TIMSK1 |= (1 << OCIE1A);
    // enable global interrupts:
    sei();
}
 
void loop()
{
  while(Serial.available()) {
    a= Serial.readString();// read the incoming data as string
    Serial.println(a);
    // if KO or KO
    for (i=0; i<a.length(); i++) {
      Serial.println(a.charAt(i));
      mini_a = a.charAt(i);
      if (mini_a == (";")) {
        //digitalWrite(LEDPIN, string_append.toInt());
        Serial.println(string_append);
        string_append = "";
      }
      else {
        string_append = string_append + mini_a;
      }
      
    }
    if (cont_valves == 7){
      cont_valves = 0;  
      start = true;
      timeElapsed = 0;
    }
  }

}


ISR(TIMER1_COMPA_vect)
{
  if (start) {
    //LED1 Azul
      if (valve1_delay_passed == false) {
        if (timeElapsed > delay1) {
          delay1 = -1;
          valve1_delay_passed = true;
          Serial.println(delay2);
          ledState = !ledState;
          Serial.println(timeElapsed);
          Serial.println(ledState);
          digitalWrite(LEDPIN, ledState);
          time_started1 = long(timeElapsed);       
        }
      }
      
      //LED2 Blanco
      if (valve2_delay_passed == false) {
        if (timeElapsed > delay2) {
          delay2 = -1;
          valve2_delay_passed = true;
          Serial.println(ledState2);
          ledState2 = !ledState2;
          Serial.println(timeElapsed);
          Serial.println(ledState2);
          digitalWrite(LEDPIN2, HIGH);
          time_started2 = long(timeElapsed);
        }
      }
      //ONs to turn off led
      if (valve1_delay_passed == true) {
        long var_time1 = long(timeElapsed) - time_started1;
        if (var_time1 >= on1)
        {
          digitalWrite(LEDPIN, LOW);
          time_started1 = long(timeElapsed);
        }
      }
      

      if (valve2_delay_passed == true) {
        long var_time2 = long(timeElapsed) - time_started2;
        if (var_time2 >= on2)
        {
          digitalWrite(LEDPIN2, LOW);
          time_started2 = long(timeElapsed);
        }
      }


  }
  
}
