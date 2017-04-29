# BLE-UART-Reader
Simple python script to read BLE values.

Usage: python primo_ble_readuart.py E8:EC:B8:30:AB:B4
Where E8:EC:B8:30:AB:B4 is the BLE address of your device. Use the commando sudo hcitool lescan to read values from the Arduino Primo. 
Use the example File-Example-BLE-serial<br>
and the funcion spam()<br>
(Uncomment it at the row 44)<br>
  //forward();<br>
  // loopback();<br>
   spam();<br>

You will see:<br>
angelo@angelo-X550LD:~/Dropbox/Primo/ArduinoTestBenchPrimo$ python primo_ble_readuart.py E8:EC:B8:30:AB:B4<br>
Ret:7451178 tick-tacks!<br>
Ret:7452192 tick-tacks!<br>
Ret:7453206 tick-tacks!<br>
Ret:7454220 tick-tacks!<br>
Ret:7455234 tick-tacks!<br>
Ret:7456248 tick-tacks!<br>
Ret:7457262 tick-tacks!<br>
Ret:7458276 tick-tacks!<br>
Ret:7459290 tick-tacks!<br>
Ret:7460304 tick-tacks!<br>
Ret:7461318 tick-tacks!<br>
Ret:7462332 tick-tacks!<br>
<br>
