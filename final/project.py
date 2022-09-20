import pytz
import datetime
from datetime import datetime
from pytz import timezone
from tzlocal import get_localzone
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim

import zmq

while True:
    """
    Function to get time zone for input location.
    """
    def get_timezone(location):
        geolocator = Nominatim(user_agent="geoapiExercises")
        # getting Latitude and Longitude
        latlong = geolocator.geocode(location)
        if latlong is None:
            # return None
            return None
        else:
            # pass the Latitude and Longitude into a timezone_at and return timezone
            obj = TimezoneFinder()
            return obj.timezone_at(lng=latlong.longitude, lat=latlong.latitude)

    """
    Ask user if they want to convert current time.
    """
    currentlocal = input("Convert current local time (Y/N)? ")

    while currentlocal.lower() != 'y' and currentlocal.lower() != 'n':
        currentlocal = input("Enter valid answer (Y/N): ")
        
    if currentlocal.lower() == 'y':
        input_timezone = get_localzone()
        input_timezone = str(input_timezone)
        file = open("input-timezone.txt", "w")
        file.write(input_timezone)
        file.close()

        context = zmq.Context()

        #  Socket to talk to server
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:5555")

        #  Send input time, wait for a response
        socket.send_string(currentlocal)

        time2convert = socket.recv()
        time2convert=time2convert.decode('utf-8')

    elif currentlocal.lower() == 'n':
        #Get input location's timezone.
        inputLocation = input("Enter input location:  ")
        input_timezone = get_timezone(inputLocation)

        while input_timezone is None:
            inputLocation = input("Please enter a valid time zone: ")
            input_timezone = get_timezone(inputLocation)

        file = open("input-timezone.txt", "w")
        file.write(input_timezone)
        file.close()

        #Get time to convert.
        time2convert = str(input('Enter date and time (yyyy-mm-dd hh:mm): '))

    #Get output location's timezone.
    outputLocation = input("Enter output location:  ")
    output_timezone = get_timezone(outputLocation)

    while output_timezone is None:
        outputLocation = input("Please enter a valid time zone: ")
        output_timezone = get_timezone(outputLocation)

    file = open("output-timezone.txt", "w")
    file.write(output_timezone)
    file.close()


    """
    Convert time.
    """
    datetime = datetime.strptime(time2convert, "%Y-%m-%d %H:%M")
    inputtime = timezone(input_timezone).localize(datetime) 
    outputtime = inputtime.astimezone(timezone(output_timezone))


    """
    Output message.
    """
    print("\n")
    print(f"Time in {input_timezone}: {time2convert}") 
    print(f"Time in {output_timezone}: {outputtime}") 
    print("\n") 