# Protocol

bytes

big-endian

| BOF   |   ID  | LEN   | DATA  | EOF   |
|:-:|:-:|:-:|:-:|:-:|
|0x5a   |0-255  |0-255  |   -   | 0x0a  |

max message length 255

---
### Messages

* 0     BASIC MESSAGE
* 1-100 client --> host
* \>100 host-->client