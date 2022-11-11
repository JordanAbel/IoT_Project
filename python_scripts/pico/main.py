import machine
import utime

# Analog to Digital Converter pins
photocell_sensor = machine.ADC(26)
moisture_sensor = machine.ADC(27)

while True:
    photocell_value = photocell_sensor.read_u16() # Photocell sensor reading
    moisture_value = moisture_sensor.read_u16() # Moisture sensor reading
    
    send_value = str(photocell_value) + ":" + str(moisture_value) # Readings from sensors separated by colon symbol
     
    print(send_value) # Printed values can be read from USB
    utime.sleep(1) # Send updates every second
