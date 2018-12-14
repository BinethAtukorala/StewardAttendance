import time
import RPi.GPIO as GPIO
import SimpleMFRC522
from firebase import firebase
import datetime

from os import system

GPIO.setwarnings(False)
GPIO.cleanup()

SECRET = 'pK9jJOi2UBz7x6JmdDhg4HmY3T8IpBcT5Ns0Mpq0'
EMAIL = 'bineth.mandiv@gmail.com'
authentication = firebase.FirebaseAuthentication(SECRET,EMAIL, True, True)

fb = firebase.FirebaseApplication('https://stewardattendence.firebaseio.com/', authentication)

reader = SimpleMFRC522.SimpleMFRC522()

MAX_NO = fb.get('/', 'No')

w, h = MAX_NO+1, 4
usrs = [[0 for x in range(h)] for y in range(w)] 

for x in range(MAX_NO):
    usrs[x][0] = fb.get('/stewards/'+str(x)+'/', 'UID')
    usrs[x][1] = fb.get('/stewards/'+str(x)+'/', 'StewardNo')
    usrs[x][2] = fb.get('/stewards/'+str(x)+'/', 'Name')

def findID(_id):

    for x in range(MAX_NO):
        if(_id == usrs[x][0]):
            return x
    return MAX_NO

now = datetime.datetime.now()
date = str(now.year)+'-'+str(now.month)+'-'+str(now.day)

for x in range(MAX_NO):
    result = fb.patch('/'+date+'/'+str(x)+'/', {'Presence':'0', 'time':'-'})


try:    
        system("clear")
        print("System Initiated\n\n")

        
        while(1):
            id = reader.read()
            print("Card found : "+str(id))
            usrNo = findID(id)
            if(usrNo != MAX_NO):
                currentPresence = fb.get('/'+date+'/'+str(usrNo)+'/', 'Presence')
                if(currentPresence == '0'):
                    print(usrs[usrNo][2]+" attendance recorded")
                    now = datetime.datetime.now()
                    time_now = str(now.hour)+'.'+str(now.minute)+'.'+str(now.second)
                    fb.patch('/'+date+'/'+str(usrNo)+'/', {'Presence':'1', 'time': time_now})
            else:
                print("NOT FOUND")
	    print("\n")
	    time.sleep(1)


finally:
        GPIO.cleanup()
