#Libraries
import RPi.GPIO as GPIO
import time
import serial
import board
from Adafruit_IO import Client, Feed, RequestError
import adafruit_dht

# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = 'aio_bgOy021bgmgUASD6s3yzjU4i61Uu'
# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = 'curtishallman'
# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)



def sendFeed (str, str2):
    aio.send(temperature.key, temperature_c)
    aio.send(humidity.key, humidity_value)
    
try: # if we have a 'temperature' feed
    temperature = aio.feeds('temperature')
except RequestError: # create a temperature feed
    feed = Feed(name="temperature")
    temperature = aio.create_feed(feed)
    
try: # if we have a 'humidity' feed
    humidity = aio.feeds('humidity')
except RequestError: # create a humidity feed
    feed2 = Feed(name="humidity")
    humidity = aio.create_feed(feed2)
    
try: # if we have a 'brightness' feed
    brightness = aio.feeds('brightness')
except RequestError: # create a brightness feed
    feed3 = Feed(name="brightness")
    brightness = aio.create_feed(feed3)

try: # if we have a 'moisture' feed
    moisture = aio.feeds('moisture')
except RequestError: # create a moisture feed
    feed4 = Feed(name="moisture")
    moisture = aio.create_feed(feed4)
    
#GPIO Mode (BOARD / BCM)
dht_sensor = adafruit_dht.DHT11(board.D4,use_pulseio=False)

BG_PIN =  17
GPIO.setup(BG_PIN, GPIO.IN)

ser = serial.Serial('/dev/ttyACM1', 9600)
time.sleep(1)
#send data to dashboard
while True:
    try:
        temperature_c = dht_sensor.temperature
        humidity_value = dht_sensor.humidity
    
        print("Temp={0:0.1f}C Humidity={1:0.1f}%".format(temperature_c, humidity_value))
        
        print(GPIO.input(BG_PIN))
        
        sendFeed(temperature_c, humidity_value)
    except:
        a = "Sensor failure. Check wiring.";
    
    time.sleep(5);
    
    
#ser = serial.Serial('/dev/ttyACM1', 9600)
#time.sleep(1)

while True:
    line = ser.readline();

    try:
        msg = line.decode()
        values = msg.split(":")

        brightness_value = values[0]
        moisture_value = values[1]

        print("Brightness: " + brightness_value)
        print("Moisture: " + moisture_value)
        

    except:
        pass