// Arduino timer CTC interrupt example
// www.engblaze.com

// avr-libc library includes
#include <avr/io.h>
#include <avr/interrupt.h>
 
#define LEDPIN 2
#define LEDPIN2 3
#define LEDPIN3 4
#define LEDPIN4 5
#define LEDPIN5 6
#define LEDPIN6 7
#define LEDPIN7 8
#define LEDPIN8 9


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
unsigned long delay3 = 0;
unsigned long delay4 = 0;
unsigned long delay5 = 0;
unsigned long delay6 = 0;
unsigned long delay7 = 0;
unsigned long delay8 = 0;

unsigned long on1 = 0;
unsigned long on2 = 0;
unsigned long on3 = 0;
unsigned long on4 = 0;
unsigned long on5 = 0;
unsigned long on6 = 0;
unsigned long on7 = 0;
unsigned long on8 = 0;

unsigned long time_started1 = 0;
unsigned long time_started2 = 0;
unsigned long time_started3 = 0;
unsigned long time_started4 = 0;
unsigned long time_started5 = 0;
unsigned long time_started6 = 0;
unsigned long time_started7 = 0;
unsigned long time_started8 = 0;

long off1 = 0;
long off2 = 0;
long off3 = 0;
long off4 = 0;
long off5 = 0;
long off6 = 0;
long off7 = 0;
long off8 = 0;

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
unsigned long time_out3 = 0;
unsigned long time_out4 = 0;
unsigned long time_out5 = 0;
unsigned long time_out6 = 0;
unsigned long time_out7 = 0;
unsigned long time_out8 = 0;


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
    pinMode(LEDPIN3, OUTPUT);
    pinMode(LEDPIN4, OUTPUT);
    pinMode(LEDPIN5, OUTPUT);
    pinMode(LEDPIN6, OUTPUT);
    pinMode(LEDPIN7, OUTPUT);
    pinMode(LEDPIN8, OUTPUT);
    
 
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
        char myChar2[45];
        valve_data2.toCharArray(myChar2, valve_data2.length());
        if (sscanf(myChar2, "%lu;%lu;%lu;%lu;", &delay2, &on2, &off2, &time_out2) == 4) {
        }
        char myChar3[45];
        valve_data3.toCharArray(myChar3, valve_data3.length());
        if (sscanf(myChar3, "%lu;%lu;%lu;%lu;", &delay3, &on3, &off3, &time_out3) == 4) {
        }
        char myChar4[45];
        valve_data4.toCharArray(myChar4, valve_data4.length());
        if (sscanf(myChar4, "%lu;%lu;%lu;%lu;", &delay4, &on4, &off4, &time_out4) == 4) {
        }
        char myChar5[45];
        valve_data5.toCharArray(myChar5, valve_data5.length());
        if (sscanf(myChar5, "%lu;%lu;%lu;%lu;", &delay5, &on5, &off5, &time_out5) == 4) {
        }
        char myChar6[45];
        valve_data6.toCharArray(myChar6, valve_data6.length());
        if (sscanf(myChar6, "%lu;%lu;%lu;%lu;", &delay6, &on6, &off6, &time_out6) == 4) {
        }
        char myChar7[45];
        valve_data7.toCharArray(myChar7, valve_data7.length());
        if (sscanf(myChar7, "%lu;%lu;%lu;%lu;", &delay7, &on7, &off7, &time_out7) == 4) {
        }
        char myChar8[45];
        valve_data8.toCharArray(myChar8, valve_data8.length());
        if (sscanf(myChar8, "%lu;%lu;%lu;%lu;", &delay8, &on8, &off8, &time_out8) == 4) {
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
      start = false;
      time_out1 = 0;
      time_out2 = 0;
      time_out3 = 0;
      time_out4 = 0;
      time_out5 = 0;
      time_out6 = 0;
      time_out7 = 0;
      time_out8 = 0;
      
      cont_valves = -1;
      timeElapsed = 0;
      
      digitalWrite(LEDPIN, LOW);
      digitalWrite(LEDPIN2, LOW);
      digitalWrite(LEDPIN3, LOW);
      digitalWrite(LEDPIN4, LOW);
      digitalWrite(LEDPIN5, LOW);
      digitalWrite(LEDPIN6, LOW);
      digitalWrite(LEDPIN7, LOW);
      digitalWrite(LEDPIN8, LOW);      
      
      // delay(1);
      //LEQ
      // Serial.println(data);
      
    }
    // Still used
    else if (String("KO") == data) {
      start = false;
      time_out1 = 0;
      time_out2 = 0;
      time_out3 = 0;
      time_out4 = 0;
      time_out5 = 0;
      time_out6 = 0;
      time_out7 = 0;
      time_out8 = 0;

delay1 = 0;
delay2 = 0;
delay3 = 0;
delay4 = 0;
delay5 = 0;
delay6 = 0;
delay7 = 0;
delay8 = 0;

on1 = 0;
on2 = 0;
on3 = 0;
on4 = 0;
on5 = 0;
on6 = 0;
on7 = 0;
on8 = 0;

time_started1 = 0;
time_started2 = 0;
time_started3 = 0;
time_started4 = 0;
time_started5 = 0;
time_started6 = 0;
time_started7 = 0;
time_started8 = 0;

off1 = 0;
off2 = 0;
off3 = 0;
off4 = 0;
off5 = 0;
off6 = 0;
off7 = 0;
off8 = 0;

valve1_delay_passed = false;
valve2_delay_passed = false;
valve3_delay_passed = false;
valve4_delay_passed = false;
valve5_delay_passed = false;
valve6_delay_passed = false;
valve7_delay_passed = false;
valve8_delay_passed = false;

valve1_on_passed = false;
valve2_on_passed = false;
valve3_on_passed = false;
valve4_on_passed = false;
valve5_on_passed = false;
valve6_on_passed = false;
valve7_on_passed = false;
valve8_on_passed = false;

valve1_off_passed = false;
valve2_off_passed = false;
valve3_off_passed = false;
valve4_off_passed = false;
valve5_off_passed = false;
valve6_off_passed = false;
valve7_off_passed = false;
valve8_off_passed = false;

//Time out vars?
time_out1 = 0;
time_out2 = 0;
time_out3 = 0;
time_out4 = 0;
time_out5 = 0;
time_out6 = 0;
time_out7 = 0;
time_out8 = 0;



      
      cont_valves = -1;
      timeElapsed = 0;
      
      digitalWrite(LEDPIN, LOW);
      digitalWrite(LEDPIN2, LOW);
      digitalWrite(LEDPIN3, LOW);
      digitalWrite(LEDPIN4, LOW);
      digitalWrite(LEDPIN5, LOW);
      digitalWrite(LEDPIN6, LOW);
      digitalWrite(LEDPIN7, LOW);
      digitalWrite(LEDPIN8, LOW);      
      
      delay(1);
      Serial.println(data);
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


//3rd

    if ((time_out3 <= timeElapsed) && (time_out3 >= 0) ) {
        digitalWrite(LEDPIN3, LOW);

        off3 = 0;
        on3 = 0;
        delay3 = 0;
        valve3_on_passed = false;
        valve3_delay_passed = false;
        time_out3 = -1;
        init_3 = false;
      }

      if (time_out3 != -1) {
        //LED1 Azul
        if (valve3_delay_passed == false && init_3 == true) {
          
          if (long(timeElapsed) >= delay3) {
            valve3_delay_passed = true;
            time_started3 = long(timeElapsed);
            init_3 = false;
          }
        }
              
        //Turn ON led
        if (valve3_delay_passed == true) {
          digitalWrite(LEDPIN3, HIGH);
          long var_time3 = long(timeElapsed) - time_started3;
          if (var_time3 >= on3)
          {
            valve3_on_passed = true;
            valve3_delay_passed = false;
            time_started3 = long(timeElapsed);
          }
        }
     
        //Turn OFF Led
        if (valve3_on_passed == true) {
          digitalWrite(LEDPIN3, LOW);
          long var_time3 = long(timeElapsed) - time_started3;
          if (var_time3 >= off3)
          {
            valve3_on_passed = false;
            valve3_delay_passed = true;
            time_started3 = long(timeElapsed);
          }
        }
      }

// 4th


    if ((time_out4 <= timeElapsed) && (time_out4 >= 0) ) {
        digitalWrite(LEDPIN4, LOW);

        off4 = 0;
        on4 = 0;
        delay4 = 0;
        valve4_on_passed = false;
        valve4_delay_passed = false;
        time_out4 = -1;
        init_4 = false;
      }

      if (time_out4 != -1) {
        //LED1 Azul
        if (valve4_delay_passed == false && init_4 == true) {
          
          if (long(timeElapsed) >= delay4) {
            valve4_delay_passed = true;
            time_started4 = long(timeElapsed);
            init_4 = false;
          }
        }
              
        //Turn ON led
        if (valve4_delay_passed == true) {
          digitalWrite(LEDPIN4, HIGH);
          long var_time4 = long(timeElapsed) - time_started4;
          if (var_time4 >= on4)
          {
            valve4_on_passed = true;
            valve4_delay_passed = false;
            time_started4 = long(timeElapsed);
          }
        }
     
        //Turn OFF Led
        if (valve4_on_passed == true) {
          digitalWrite(LEDPIN4, LOW);
          long var_time4 = long(timeElapsed) - time_started4;
          if (var_time4 >= off4)
          {
            valve4_on_passed = false;
            valve4_delay_passed = true;
            time_started4 = long(timeElapsed);
          }
        }
      }

// 5th

    if ((time_out5 <= timeElapsed) && (time_out5 >= 0) ) {
        digitalWrite(LEDPIN5, LOW);

        off5 = 0;
        on5 = 0;
        delay5 = 0;
        valve5_on_passed = false;
        valve5_delay_passed = false;
        time_out5 = -1;
        init_5 = false;
      }

      if (time_out5 != -1) {
        //LED1 Azul
        if (valve5_delay_passed == false && init_5 == true) {
          
          if (long(timeElapsed) >= delay5) {
            valve5_delay_passed = true;
            time_started5 = long(timeElapsed);
            init_5 = false;
          }
        }
              
        //Turn ON led
        if (valve5_delay_passed == true) {
          digitalWrite(LEDPIN5, HIGH);
          long var_time5 = long(timeElapsed) - time_started5;
          if (var_time5 >= on5)
          {
            valve5_on_passed = true;
            valve5_delay_passed = false;
            time_started5 = long(timeElapsed);
          }
        }
     
        //Turn OFF Led
        if (valve5_on_passed == true) {
          digitalWrite(LEDPIN5, LOW);
          long var_time5 = long(timeElapsed) - time_started5;
          if (var_time5 >= off5)
          {
            valve5_on_passed = false;
            valve5_delay_passed = true;
            time_started5 = long(timeElapsed);
          }
        }
      }


// 6th

    if ((time_out6 <= timeElapsed) && (time_out6 >= 0) ) {
        digitalWrite(LEDPIN6, LOW);

        off6 = 0;
        on6 = 0;
        delay6 = 0;
        valve6_on_passed = false;
        valve6_delay_passed = false;
        time_out6 = -1;
        init_6 = false;
      }

      if (time_out6 != -1) {
        //LED1 Azul
        if (valve6_delay_passed == false && init_6 == true) {
          
          if (long(timeElapsed) >= delay6) {
            valve6_delay_passed = true;
            time_started6 = long(timeElapsed);
            init_6 = false;
          }
        }
              
        //Turn ON led
        if (valve6_delay_passed == true) {
          digitalWrite(LEDPIN6, HIGH);
          long var_time6 = long(timeElapsed) - time_started6;
          if (var_time6 >= on6)
          {
            valve6_on_passed = true;
            valve6_delay_passed = false;
            time_started6 = long(timeElapsed);
          }
        }
     
        //Turn OFF Led
        if (valve6_on_passed == true) {
          digitalWrite(LEDPIN6, LOW);
          long var_time6 = long(timeElapsed) - time_started6;
          if (var_time6 >= off6)
          {
            valve6_on_passed = false;
            valve6_delay_passed = true;
            time_started6 = long(timeElapsed);
          }
        }
      }


// 7th

    if ((time_out7 <= timeElapsed) && (time_out7 >= 0) ) {
        digitalWrite(LEDPIN7, LOW);

        off7 = 0;
        on7 = 0;
        delay7 = 0;
        valve7_on_passed = false;
        valve7_delay_passed = false;
        time_out7 = -1;
        init_7 = false;
      }

      if (time_out7 != -1) {
        //LED1 Azul
        if (valve7_delay_passed == false && init_7 == true) {
          
          if (long(timeElapsed) >= delay7) {
            valve7_delay_passed = true;
            time_started7 = long(timeElapsed);
            init_7 = false;
          }
        }
              
        //Turn ON led
        if (valve7_delay_passed == true) {
          digitalWrite(LEDPIN7, HIGH);
          long var_time7 = long(timeElapsed) - time_started7;
          if (var_time7 >= on7)
          {
            valve7_on_passed = true;
            valve7_delay_passed = false;
            time_started7 = long(timeElapsed);
          }
        }
     
        //Turn OFF Led
        if (valve7_on_passed == true) {
          digitalWrite(LEDPIN7, LOW);
          long var_time7 = long(timeElapsed) - time_started7;
          if (var_time7 >= off7)
          {
            valve7_on_passed = false;
            valve7_delay_passed = true;
            time_started7 = long(timeElapsed);
          }
        }
      }
      

// 8th

    if ((time_out8 <= timeElapsed) && (time_out8 >= 0) ) {
        digitalWrite(LEDPIN8, LOW);

        off8 = 0;
        on8 = 0;
        delay8 = 0;
        valve8_on_passed = false;
        valve8_delay_passed = false;
        time_out8 = -1;
        init_8 = false;
      }

      if (time_out8 != -1) {
        //LED1 Azul
        if (valve8_delay_passed == false && init_8 == true) {
          
          if (long(timeElapsed) >= delay8) {
            valve8_delay_passed = true;
            time_started8 = long(timeElapsed);
            init_8 = false;
          }
        }
              
        //Turn ON led
        if (valve8_delay_passed == true) {
          digitalWrite(LEDPIN8, HIGH);
          long var_time8 = long(timeElapsed) - time_started8;
          if (var_time8 >= on8)
          {
            valve8_on_passed = true;
            valve8_delay_passed = false;
            time_started8 = long(timeElapsed);
          }
        }
     
        //Turn OFF Led
        if (valve8_on_passed == true) {
          digitalWrite(LEDPIN8, LOW);
          long var_time8 = long(timeElapsed) - time_started8;
          if (var_time8 >= off8)
          {
            valve8_on_passed = false;
            valve8_delay_passed = true;
            time_started8 = long(timeElapsed);
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
