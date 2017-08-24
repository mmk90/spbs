#include <stdio.h>


#include <mega16a.h>
// I2C Bus functions
#include <i2c.h>
// DS1307 Real Time Clock functions
#include <ds1307.h>
// Alphanumeric LCD functions
#include <alcd.h>
#include <delay.h>
#include <stdio.h>

void main(void(
{
int a=0,i=200,b=0;
int hh=0,mm=0,ss=0,ww=0,moo=0,yy=0,dd=0;
unsigned char stt[16];
char buffer[]={0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},h=0,m=0,s=0,y=0,mo=0,d=0,w=0;
//><><><><><><><><><><><><><><><><><><><><><><\\
DDRB=(0<<DDB7) | (0<<DDB6) | (0<<DDB5) | (0<<DDB4) | (0<<DDB3) | (0<<DDB2) | (0<<DDB1) | (0<<DDB0);
PORTB=(0<<PORTB7) | (0<<PORTB6) | (1<<PORTB5) | (1<<PORTB4) | (1<<PORTB3) | (1<<PORTB2) | (1<<PORTB1) | (1<<PORTB0);
//><><><><><><><><><><><><><><><><><><><><><><\\
// Bit-Banged I2C Bus initialization
// I2C Port: PORTC
// I2C SDA bit: 1
// I2C SCL bit: 0
// Bit Rate: 100 kHz
// Note: I2C settings are specified in the
// Project|Configure|C Compiler|Libraries|I2C menu.
i2c_init();
//><><><><><><><><><><><><><><><><><><><><><><\\
// DS1307 Real Time Clock initialization
// Square wave output on pin SQW/OUT: Off
// SQW/OUT pin state: 0
rtc_init(0,0,0);
//><><><><><><><><><><><><><><><><><><><><><><\\
lcd_init(16);
//><><><><><><><><><><><><><><><><><><><><><><\\

 lcd_clear();
        lcd_gotoxy(0,0);
        lcd_puts("*SPBS IOT GROUP*");
        lcd_gotoxy(1,1);
        lcd_puts("Smart DoorBell");
        delay_ms(1000);

        while (1)
        {
          rtc_get_time(&h,&m,&s);
          rtc_get_date(&w,&d,&mo,&y);
          if(PINB.3==0){
          delay_ms(100);
          a=!a;
          }

            switch(a){
            case 0:
            lcd_clear();
            lcd_gotoxy(4,1);
            sprintf(buffer,"%d:%d:%d",h,m,s);
            lcd_puts(buffer);
            lcd_gotoxy(3,0);
            sprintf(buffer,"20%d:%d:%d",y,mo,d);
            lcd_puts(buffer);
            delay_ms(100);
            break;

            case 1:
            lcd_clear();
              if(PINB.4==0){
              delay_ms(100);
              b++;
              if(b>6) b=0;
              }

              if(PINB.5==0){
              delay_ms(100);
              b--;
              if(b<0) b=6;
              }
             switch (b){

             case 0:

             lcd_clear();
             lcd_gotoxy(0,0);
             sprintf(stt,">>Sec:%d",s);
             lcd_puts(stt);
             lcd_gotoxy(0,1);
             sprintf(stt,"Min:%d",m);
             lcd_puts(stt);
              if(PINB.0==0)
               {
               delay_ms(200);
               ss++;
               if( ss > 60 ) ss=0;
               rtc_set_time(hh,mm,ss);
                }
                if(PINB.1==0)
               {
               delay_ms(200);
               ss--;
               if( ss < 0 ) ss=60;
               rtc_set_time(hh,mm,ss);
                }
              break;

             case 1:
             lcd_clear();
             lcd_gotoxy(0,0);
             sprintf(stt,"Sec:%d",s);
             lcd_puts(stt);
             lcd_gotoxy(0,1);
             sprintf(stt,">>Min:%d",m);
             lcd_puts(stt);
             if(PINB.0==0)
               {
               delay_ms(200);
               mm++;
               if( mm > 60 ) mm=0;
               rtc_set_time(hh,mm,ss);
                }
                if(PINB.1==0)
               {
               delay_ms(200);
               mm--;
               if( mm < 0 ) mm=60;
               rtc_set_time(hh,mm,ss);
                }
             break;


             case 2:
             lcd_clear();
             lcd_gotoxy(0,0);
             sprintf(stt,">>Hour:%d",h);
             lcd_puts(stt);
             lcd_gotoxy(0,1);
             sprintf(stt,"DAY:%d",d);
             lcd_puts(stt);
             if(PINB.0==0)
               {
               delay_ms(200);
               hh++;
               if( hh > 24 ) hh=0;
               rtc_set_time(hh,mm,ss);
                }
                if(PINB.1==0)
               {
               delay_ms(200);
               hh--;
               if( hh < 0 ) hh=24;
               rtc_set_time(hh,mm,ss);
                }
             break;

             case 3:
             lcd_clear();
             lcd_gotoxy(0,0);
             sprintf(stt,"Hour:%d",h);
             lcd_puts(stt);
             lcd_gotoxy(0,1);
             sprintf(stt,">>Day:%d",d);
             lcd_puts(stt);
             if(PINB.0==0)
               {
               delay_ms(i);
               if(dd==5)i=10;
               dd++;
               if( dd > 31 ) dd=0;
               rtc_set_date(ww,dd,moo,yy);
                }
                if(PINB.1==0)
               {
               delay_ms(i);
               if(dd==20)i=10;
               dd--;
               if( dd < 0 ) dd=31;
               rtc_set_date(ww,dd,moo,yy);
                }

             break;

             case 4:
             lcd_clear();
             lcd_gotoxy(0,0);
             sprintf(stt,">>Mounth:%d",mo);
             lcd_puts(stt);
             lcd_gotoxy(0,1);
             sprintf(stt,"Year:%d",y);
             lcd_puts(stt);
             if(PINB.0==0)
               {
               delay_ms(i);
               if(dd==5)i=10;
               moo++;
               if( moo > 12 ) moo=0;
               rtc_set_date(ww,dd,moo,yy);
                }
                  if(PINB.1==0)
               {
               delay_ms(i);
               if(moo==8)i=10;
               moo--;
               if( dd < 0 ) dd=12;
               rtc_set_date(ww,dd,moo,yy);
                }
             break;

                 case 5:
             lcd_clear();
             lcd_gotoxy(0,0);
             sprintf(stt,"Mounth:%d",mo);
             lcd_puts(stt);
             lcd_gotoxy(0,1);
             sprintf(stt,">>Year:%d",y);
             lcd_puts(stt);
             if(PINB.0==0)
               {
               delay_ms(i);
               if(yy==5)i=5;
               yy++;
               if( yy > 30 ) yy=0;
               rtc_set_date(ww,dd,moo,yy);
                }
                  if(PINB.1==0)
               {
               delay_ms(i);
               if(yy==20)i=10;
               yy--;
               if( yy < 0 ) yy=30;
               rtc_set_date(ww,dd,moo,yy);
                }
             break;

              case 6:
             lcd_clear();
             lcd_gotoxy(0,0);
             sprintf(stt,">>About");
             lcd_puts(stt);
             if(PINB.0==0)
               {
               delay_ms(i);
               lcd_clear();
               lcd_gotoxy(0,0);
               lcd_puts("Kazemi-Mazdarani");
               lcd_gotoxy(4,1);
               lcd_puts("Kalantari");
               delay_ms(1000);
                }
                  if(PINB.1==0)
               {
               delay_ms(i);
               lcd_clear();
               lcd_gotoxy(4,0);
               lcd_puts("SPBS GROUP");
               lcd_gotoxy(3,1);
               lcd_puts("IOT ACADEMY");
               delay_ms(1000);
                }
             break;
              }

            break;

            }
            delay_ms(200);
        }

