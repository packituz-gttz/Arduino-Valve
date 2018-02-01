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

String data = "";

String valve_data1 = "";
String valve_data2 = "";
String valve_data3 = "";
String valve_data4 = "";
String valve_data5 = "";
String valve_data6 = "";
String valve_data7 = "";
String valve_data8 = "";

int cont_valves = 0;
int number_valves = 7;
long i = 0;

unsigned long delay1 = 0;
unsigned long delay2 = 0;
unsigned long delay3 = 9000;
unsigned long delay4 = 6000;
unsigned long delay5 = 9000;
unsigned long delay6 = 6000;
unsigned long delay7 = 9000;
unsigned long delay8 = 6000;

unsigned long on1 = 0;
unsigned long on2 = 0;
unsigned long on3 = 5000;
unsigned long on4 = 9000;
unsigned long on5 = 5000;
unsigned long on6 = 9000;
unsigned long on7 = 5000;
unsigned long on8 = 9000;

unsigned long time_started1 = 0;
unsigned long time_started2 = 0;
unsigned long time_started3 = 0;
unsigned long time_started4 = 0;
unsigned long time_started5 = 0;
unsigned long time_started6 = 0;
unsigned long time_started7 = 0;
unsigned long time_started8 = 0;

long off1 = 0;
long off2 = 3000;
long off3 = 0;
long off4 = 3000;
long off5 = 0;
long off6 = 3000;
long off7 = 0;
long off8 = 3000;

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
unsigned long time_out1 = 0;
unsigned long time_out2 = 0;


boolean start = false;
boolean init_1 = true;
boolean init_2 = true;
boolean init_3 = true;
boolean init_4 = true;
boolean init_5 = true;
boolean init_6 = true;
boolean init_7 = true;
boolean init_8 = true;

elapsedMillis timeElapsed;
boolean ledState = LOW;
boolean ledState2 = LOW;

void setup()
{
  Serial.begin(9600);
    pinMode(LEDPIN, OUTPUT);
    pinMode(LEDPIN2, OUTPUT);
 
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

    data = Serial.readString();// read the incoming data as string
    if (String("OK") == data) {
      if (cont_valves == 7) {

        char myChar[45];
        valve_data1.toCharArray(myChar, valve_data1.length());
        if (sscanf(myChar, "%lu;%lu;%lu;%lu;", &delay1, &on1, &off1, &time_out1) == 4) {
        }
        Serial.println(valve_data2);
        char myChar2[45];
        valve_data2.toCharArray(myChar2, valve_data2.length());
        if (sscanf(myChar2, "%lu;%lu;%lu;%lu;", &delay2, &on2, &off2, &time_out2) == 4) {
        }
        cont_valves = 0;
        timeElapsed = 0;
        start = true;
        
      }
      else {
        cont_valves++;
      }
      
      
    }
    else if (String("KILL") == data) {
      time_out1 = 0;
      time_out2 = 0;
      
    }
    else if (String("KO") == data) {
      cont_valves=0;
    }
    else {
      if (cont_valves == 0){
        valve_data1 = data;// read the incoming data as string
        delay(1);
      }
      else if(cont_valves == 1) {
        valve_data2 = data;// read the incoming data as string
        delay(1);
      }
      else if(cont_valves == 2) {
        valve_data3 = data;// read the incoming data as string
        delay(1);
      }
      else if(cont_valves == 3) {
        valve_data4 = data;// read the incoming data as string
        delay(1);
      }
      else if(cont_valves == 4) {
        valve_data5 = data;// read the incoming data as string
        delay(1);
      }
      else if(cont_valves == 5) {
        valve_data6 = data;// read the incoming data as string
        delay(1);
      }
      else if(cont_valves == 6) {
        valve_data7 = data;// read the incoming data as string
        delay(1);
      }
      else if(cont_valves == 7) {
        valve_data8 = data;// read the incoming data as string
        delay(1);
        }
        Serial.println(data);
      }
      
    }
  }



ISR(TIMER1_COMPA_vect)
{
  if (start) {


      if ((time_out1 <= timeElapsed) && (time_out1 >= 0) ) {
        digitalWrite(LEDPIN, LOW);

        off1 = 0;
        on1 = 0;
        delay1 = 0;
        valve1_on_passed = false;
        valve1_delay_passed = false;
        time_out1 = -1;
        init_1 = false;
      }

      if (time_out1 != -1) {
        //LED1 Azul
        if (valve1_delay_passed == false && init_1 == true) {
          
          if (long(timeElapsed) >= delay1) { 
            valve1_delay_passed = true;
            time_started1 = long(timeElapsed);
            init_1 = false;
          }
        }
              
        //Turn ON led
        if (valve1_delay_passed == true) {
          digitalWrite(LEDPIN, HIGH);
          long var_time1 = long(timeElapsed) - time_started1;
          if (var_time1 >= on1)
          {
            valve1_on_passed = true;
            valve1_delay_passed = false;
            time_started1 = long(timeElapsed);
          }
        }
     
        //Turn OFF Led
        if (valve1_on_passed == true) {
          digitalWrite(LEDPIN, LOW);
          long var_time1 = long(timeElapsed) - time_started1;
          if (var_time1 >= off1)
          {
            valve1_on_passed = false;
            valve1_delay_passed = true;
            time_started1 = long(timeElapsed);
          }
        }
      }
    
/////////////////////////////////////


    if ((time_out2 <= timeElapsed) && (time_out2 >= 0) ) {
        digitalWrite(LEDPIN2, LOW);

        off2 = 0;
        on2 = 0;
        delay2 = 0;
        valve2_on_passed = false;
        valve2_delay_passed = false;
        time_out2 = -1;
        init_2 = false;
      }

      if (time_out2 != -1) {
        //LED1 Azul
        if (valve2_delay_passed == false && init_2 == true) {
          
          if (long(timeElapsed) >= delay2) {
            valve2_delay_passed = true;
            time_started2 = long(timeElapsed);
            init_2 = false;
          }
        }
              
        //Turn ON led
        if (valve2_delay_passed == true) {
          digitalWrite(LEDPIN2, HIGH);
          long var_time2 = long(timeElapsed) - time_started2;
          if (var_time2 >= on2)
          {
            valve2_on_passed = true;
            valve2_delay_passed = false;
            time_started2 = long(timeElapsed);
          }
        }
     
        //Turn OFF Led
        if (valve2_on_passed == true) {
          digitalWrite(LEDPIN2, LOW);
          long var_time2 = long(timeElapsed) - time_started2;
          if (var_time2 >= off2)
          {
            valve2_on_passed = false;
            valve2_delay_passed = true;
            time_started2 = long(timeElapsed);
          }
        }
      }


//2nd
      //LED2 Blanco
//      if (valve2_delay_passed == false && init_2 == true) {
//        if (timeElapsed >= delay2) {
//          delay2 = -1;
//          valve2_delay_passed = true;
//          
//          ledState2 = !ledState2;
//          time_started2 = long(timeElapsed);
//          init_2 = false;
//        }
//      }
//
//      if (valve2_delay_passed == true) {
//        digitalWrite(LEDPIN2, HIGH);
//        
//        long var_time2 = long(timeElapsed) - time_started2;
//        if (var_time2 >= on2)
//        {
//          valve2_on_passed = true;
//          valve2_delay_passed = false;
//          time_started2 = long(timeElapsed);
//        }
//      }
//      
//      if (valve2_on_passed == true) {
//        digitalWrite(LEDPIN2, LOW);
//        long var_time2 = long(timeElapsed) - time_started2;
//        if (var_time2 >= off2)
//        {
//          valve2_off_passed = true;
//          valve2_on_passed = false;
//          time_started2 = long(timeElapsed);
//        }
//      }
//
//      if (time_out2 <= timeElapsed and time_out2 >= 0 ) {
//        digitalWrite(LEDPIN2, LOW);
//        off2 = 0;
//        on2 = 0;
//        delay2 = 0;
//        time_out2 = -1;
//      }

  }
  
}
