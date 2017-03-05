This application converts light incident to an LDR to Morse code dits and dahs before translating them.
The LDR is connected directly to a RasPi with a 2uF cap in between. A similar circuit can be found here: https://pimylifeup.com/raspberry-pi-light-sensor/

Usage: 
For a dit, shine the light (or laser) towards the LDR for less than half a second.
For a dah, shine the light for half a second.
Once a character has been constructed, shade the LDR for half a second to signal the beginning of a new character.
Kill the program (ctrl+c) and you should see what your Morse Code translates to.

