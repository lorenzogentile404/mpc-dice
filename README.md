# mpc-dice

A Python script implementing an mpc protocol to throw a dice over an insecure network between untrsuted parties.

## Challenge

Alice and Bob are playing an online dice game where they must roll a virtual dice representing the 6 sides of a physical dice. However, they do not trust each other and suspect that, if they can just roll dice locally on their computers, they will choose the outcome of the dice dishonestly, choosing the outcomes they need in order to win the game. In order to solve this, they want to execute a protocol among themselves to roll a dice while ensuring that they obtain an honest dice rolling outcome. Unfortunately, Alice and Bob are also using an insecure network, where they have no authenticity, confidentiality and integrity guarantees.

How can Alice and Bob play an online dice game over their insecure network when they do not trust each other?

Luckily Alice and Bob are security savvy and just had lectures on advanced cryptography and secure channels. Moreover, they have access to a Public Key Infrastructure, meaning that they know each other's public keys for a digital signature scheme. 

In order to help Alice and Bob you need to design and implement a protocol that allows Alice an Bob to throw a virtual 6 sided dice over the insecure network even though they do not trust each other.

HINT: Rolling dice is just sampling a random number from 1 to 6.

## Run the protocol

Start ```bob.py``` first, then start ```alice.py``` in order to allow Alice connecting to Bob and run the protocol.

Here is the perspective of Bob:

```console
user@host:~/mpc-dice$ python3 bob.py 
Connection from: ('127.0.0.1', 48366)
b > 010
Alice sent: com(a,r) sig = 

ffc31e9a6b7dfccd3a2cc45fbb5ae62241c0e1799148ca80fde783edf0b69c24

b'F\xfe\x95N\xefa\x1a-\xb6l\xdb\x92\xc1\x8b\x8a"\x03\xf6\x8c\\\xc8\xd4\xbb\xb9(\x85L8@V\xb0{\xb9C\xb3qQ>\xe2~\xbe\xaaV*\x83\xa6\xed\x8a\xe8\x9d\xfa\\\xa9\xec\xca5zZV\xb18Ua\xaf\xa8\x02u`\x00\x04~\x1f4\xbd\x12\xdd\x82\x96}\x05\xb8I\xda`,\xe66}\x9c4>\xee<\x12\xc4~\xb9\x96=\xcf\x8dR\xb3\xd0\xf0c\xa1>\x9d\xb9\x13cS\x9b\xf6WZMM\x0f\xe9\xea\x10`jMv\xdd\x19\x8d\x08F\x8f\xc6~\xc4\xaat\xe2\xb9h\xed\\AH\x93I\xf5\xb6\xa8\x80cq\x970\xa1\x14\xd8\xd6\xc4\xdf\x8cI5\xfer\x92\xd2\xceT\r,\x13=\xc1\x96\x0b\\\x04\xab\xb6\x19\x98\x1b\xd5\xe2"\\\x11s\xaf\xff\x96;\x10f\x8b\x031\x9aD\x12f\xeb\x9dy>t(\x9a@\xa6\xdb[\xbd\x89@\xd6c\x81|\xacxDdR\x0b\'\x01\xc94w\xe3\xbf\t\x07\xa4\x8b\x11\xce"\xa8M\xfc\xb8\x9eD\x8f\xcc\xce\x15B\x02\xa564'


Press enter to send: b sig > 
Alice sent: a r sig = 

101

81276298657019397074699303152249631992653619413355585619674935663759112327845489218177364506969854209293354504480099549202711008775317609876437004399784119500985105752223592312650708384899669656846628797913228064574859737697074155796455177234814192754798675627109158024297933243504416743806686192251051691419

b'\x0e\xb8%90\xac\x82\xc6g\nG5\xb8$\xe0-`\x834\xe7)L\xea\xd2_\xc5Y2e$\x05\x0f\xbb\xf2\xfa\xc4\xf9"\xbcG\r+Ki[\xfb\x08\xa6=\t\xae\xf4\xd51\xa2\xe0\xd9\xb8R"\x9c\xa4\xd8\xe5w\xfb\x9c\xbd>l{\x83\xb9\xc2\n\xb7~\xc6\xca\x06QG\xa0\x922\x958\xe3\x08?\xa0\xe5\x81\x18@6\x8c\x01k\x86\xfba\x85\xc1n\xb1R\xe0r\xf2\xea\xdf\x92\xb1\xc2\xca\x10]tG\xb5\x82q\r\xc9\xc3JC\xc4\xc9&\x17\xe8\xf8\xca\x81\x91\x0b\x18\x89\xc5\xba\xfa\xeb\x14\x18u\x9d\xf2I\n=\x93\x17~0{\xeeT]\xaa\x8b\x80\xb1X\xbe\\\x19\x06\xbc\xebj\xe4t\xd6=)\xa4\xcb\x98\x8c\xcb\x83\xbe\x92g\xe9W\xd1HW\xed\xa9B\xa9&\x19\xc8{\x94\x8e\x13\xf1Y;\xc8\x8e\xe6\x1dz\xec\xc15\xa7\xd9e\xe8c>\xf7\t\\\x19\xca\x0f\x8f-\xa8\x81D\x81C\xfe/pA\xb3bf\xf3p\x8cB\xa8\x83\x1eO\x90W$p\x8b\x04\xe5\xfe\xd6'



com(a,r) valid.


com(a|r) sig valid.


a r sig valid.

Compute d = (a ^ b) % 6 + 1
101 ^ 010 = 111 = 7 (base 10)
7 % 6 + 1 = 2
```
Here is the perspective of Alice:

```console
user@host:~/mpc-dice$ python3 alice.py 
a > 101
Press enter to send: com(a,r) sig > 
Bob sent: b sig = 

010

b'\x85\x88\xcc\'\x89\xb7\x9b\x8e\x85\\\x1b\xfb\xe5\xbb\xbe\xaaC_{\xa3\x9a\xc9g\x89L\x12H\x02\xc7\x822\x03\xebZ\xb5*\xccM\xfe\xbaHl\xbe\x8f\x1f\xe5\xce:~^}+\xa9a&_^\xdb\xe3\xf0\xc6\xa9~?\x0bf\xf2\x1e\xfc\xcb\x8b\xe1\x85\x8bi\xf5\xca\\\xb0h\xcb\x06\x95\xde~\xd8.\xb9n\xcfGE4\x0bT\xb6\xf0\x0f=\xe0[I3%\xec!\x97\x98\x07\xc9\xbc\\\xff\x94+)_\xf0\xea\xb7"\xf6\xf3\x17\xdb2>\x05\xe0\xa8\xcaUC\xd5\x85\x02\x13\xa6)]8\x82\x06\xd0\xd6\x8cA\x13\xce[\xea\x9f6\x97\x95\xe2\xed\xfa"\xe6\xf0w\xbc\x8c\\i\x7f\xee.\xa5\xcc(\xc1\x85e\xb8Q\x0e\xa9\xd7\xd6z$\xd6\x0f\xae6\xe9-\xd6\xaa^\x02u5\xb5\x0f-\xc8D\xdc\xef\x88\xa2\xee\xa8\xc7:o\xfdN\x9e\x10\x91Yq\xcaI+\xc0y\x90\xc6\x8au9\x0b\xea5OG\xb0\xcd\x06"\x8e)\xea\x81\xa3H\x00\xf7[\xe0\x86c\t\xb8i\x0c\x0e\xb3\x0c\xfek'


Press enter to send: a r sig > 

b sig valid.

Compute d = (a ^ b) % 6 + 1
101 ^ 010 = 111 = 7 (base 10)
7 % 6 + 1 = 2
```
