import pytz
from pytz import timezone
import datetime
from datetime import datetime

import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
        #  Wait for prompt from project
        yes = socket.recv()
        yes=yes.decode('utf-8')

        if yes.lower()=='y':
            now = datetime.now()
            print("now =", now)

            currenttime = now.strftime("%Y-%m-%d %H:%M")
            print("date and time =", currenttime)	

            # send converted time back 
            print(f"Sending converted time: {currenttime}")
            socket.send_string(str(currenttime))
    
