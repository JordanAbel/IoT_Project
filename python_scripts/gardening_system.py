# Libraries
import RPi.GPIO as GPIO
import time
import serial
import board
from Adafruit_IO import Client, Feed, RequestError
import adafruit_dht
import tm1637
import threading

tm = tm1637.TM1637(clk=21, dio=20)

# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = 'aio_bgOy021bgmgUASD6s3yzjU4i61Uu'
# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = 'curtishallman'
# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)


try:  # if we have a 'temperature' feed
    temperature = aio.feeds('temperature')
except RequestError:  # create a temperature feed
    feed = Feed(name="temperature")
    temperature = aio.create_feed(feed)

try:  # if we have a 'humidity' feed
    humidity = aio.feeds('humidity')
except RequestError:  # create a humidity feed
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
    
try:  # if we have a 'temperature' feed
    toggle = aio.feeds('toggle')
except RequestError:  # create a temperature feed
    feed5 = Feed(name="toggle")
    toggle = aio.create_feed(feed5)

# GPIO Mode (BOARD / BCM)
dht_sensor = adafruit_dht.DHT11(board.D4, use_pulseio=False)

BG_PIN = 17
GPIO.setup(BG_PIN, GPIO.IN)
air_value = 57390
water_value = 31500
soil_moisture_value = 0
soil_moisture_percecntage = 0

RELAY_PIN = 26
GPIO.setup(RELAY_PIN, GPIO.OUT)

def get_connection_port():
    ser = ''
    for i in range(3):
        try:
            ser = serial.Serial(f'/dev/ttyACM{i}', 9600)
        except Exception as ex:
            pass
            
    return ser


def sendFeed(str1, str2, str3, str4):
    aio.send(temperature.key, str1)
    aio.send(humidity.key, str2)
    aio.send(brightness.key, str3)
    aio.send(moisture.key, str4)
    
def get_percentage(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def send_feed_in_time_interval():
    temperature_c = dht_sensor.temperature
    humidity_value = dht_sensor.humidity
    tm.temperature(temperature_c)
    print("Temp={0:0.1f}C Humidity={1:0.1f}%".format(temperature_c, humidity_value))

    try:
        ser = get_connection_port()
        
        if (ser):
            line = ser.readline()
            msg = line.decode()
            values = msg.split(":")

            brightness_value = values[0]
            soil_moisture_value = int(values[1])
            soil_moisture_percentage = get_percentage(
                soil_moisture_value,
                air_value,
                water_value,
                0,
                100
            )
            
            print("Soil Moisture Value", soil_moisture_value)
            print("Soil Moisture", soil_moisture_percentage)


            sendFeed(temperature_c, humidity_value, brightness_value, soil_moisture_percentage)
    except:
        print("something went wrong")
        
    time.sleep(8)
    
    threading.Thread(target=send_feed_in_time_interval).start()
    

def loop():
    water_toggle = aio.receive(toggle.key)
    
    if water_toggle.value == "ON":
        GPIO.output(RELAY_PIN, GPIO.HIGH)
    else:
        GPIO.output(RELAY_PIN, GPIO.LOW)
    
        
    
threading.Thread(target=send_feed_in_time_interval).start()

# send data to dashboard
while True:
    loop()
    
