#!/bin/bash

while /bin/true; do
	./scrolling_text.py YELLOW fonts/HARNGTON.TTF 'Seasons Greetings'
	./scrolling_text.py RED fonts/OLDENGL.TTF 'Merry Christmas'
	./scrolling_text.py BLUE fonts/yataghan.ttf 'Feliz Navidad'
	./scrolling_text.py GREEN fonts/COOPBL.TTF 'Joyeux Noel'
#	./scrolling_text.py PURPLE fonts/RAVIE.TTF 'Wesolych Swiat'
done
