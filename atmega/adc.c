#include <avr/io.h>
#include <stdint.h>
#include <stdlib.h>                 // needed for uint8_t
#include <util/delay.h>
#include <string.h>

#define FOSC 1000000                       // Clock Speed
#define BAUD 4800
#define MYUBRR (FOSC/16/BAUD -1)

uint16_t adc_read(uint8_t adcx);
char getChar(void);
void sendChar(char tosend);

int main(void)
{
    /*Set baud rate */
    UBRR0H = (MYUBRR >> 8);
    UBRR0L = MYUBRR;

    UCSR0B = (1 << TXEN0)| (1 << TXCIE0) | (1 << RXEN0) | (1 << RXCIE0); ;      // Enable receiver and transmitter
    UCSR0C = (1 << UCSZ01) | (1 << UCSZ00);    // Set frame: 8data, 1 stp

    DDRD = 0b01000000;   //set all of port D as inputs except for TX
    DDRB = 0xFF;
    PORTB = 0x00;
    
    DDRC = 0x00;

	ADCSRA |= _BV(ADEN);
	
	uint16_t value;
	uint8_t i, high_byte, low_byte;
    while(1)
    {
		for(i = 0; i < 6; i++)
		{
			value = adc_read(i);		
			high_byte = value >> 8;
			low_byte = value & 0x00FF;
			sendChar(i);
			sendChar(high_byte);
			sendChar(low_byte);
			sendChar('\n');
		}		
    }
    return 0;
}

void sendChar(char tosend)
{
	while (( UCSR0A & (1<<UDRE0))  == 0){};
	UDR0 = tosend;
}

char getChar(void)
{
	while (!(UCSR0A & _BV(RXC0)));
	return (char) UDR0;
}

uint16_t adc_read(uint8_t adcx)
{
	ADMUX	&=	0xf0;
	ADMUX	|=	adcx;

	ADCSRA |= _BV(ADSC);

	while ( (ADCSRA & _BV(ADSC)) );
	
	return (uint16_t) ADC;
}
