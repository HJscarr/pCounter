import RPi.GPIO as GPIO
import gspread
import time

# Measures the distance with a sensor (output via trig and recieve in echo divide by time taken)
def measureDistance(TRIG,ECHO):
    GPIO.output(TRIG, False)
    time.sleep(0.002)
    GPIO.output(TRIG, True)
    time.sleep(0.01)
    GPIO.output(TRIG, False)
    while GPIO.input(ECHO)==0:
        pulse_start = time.time()
    while GPIO.input(ECHO)==1: 
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    distance = round((pulse_duration * 17165),1)
    #print(f'For Sensor {TRIG} Distance: {distance} cm') 
    return(distance)   

# Set the mode of the sensors and setup the sensors and get initial values (without person)
# Set constants like sensitivity of detection and headcount and counters
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
SensorA = [27,17]
SensorB = [24,23]
GPIO.setup(SensorA[0],GPIO.OUT)
GPIO.setup(SensorA[1],GPIO.IN)
GPIO.setup(SensorB[0],GPIO.OUT)
GPIO.setup(SensorB[1],GPIO.IN)
time.sleep(2)
SensorAInitial = measureDistance(SensorA[0],SensorA[1])
SensorBInitial = measureDistance(SensorB[0],SensorB[1])
headcount = 0
sequence = ""
timeoutCounter = 0
sensitivity = 50

while True:
  # Read ultrasonic sensors
  SensorAVal = measureDistance(SensorA[0],SensorA[1])
  SensorBVal = measureDistance(SensorB[0],SensorB[1])
  
  # If sensor is trigged append a value to string to represent a sensor firing
  # the order in which they are appended signifies the direction of movement 
  # (A fires then B fires then the string will read 12 rather than 21)
  if (sequence == ""):
    if (SensorAVal < SensorAInitial - sensitivity):
      print("Sensor A Triggered")
      sequence += "1"
    elif (SensorBVal < SensorBInitial - sensitivity):
      print("Sensor B Triggered")
      sequence += "2"
  
  if (sequence != ""):
    if ((SensorAVal < SensorAInitial - sensitivity) and (sequence[0] != '1')):
      print("Sensor A Triggered")
      sequence += "1"
    elif ((SensorBVal < SensorBInitial - sensitivity) and (sequence[0] != '2')):
      print("Sensor B Triggered")
      sequence += "2"
  
  # Determine the direction of movement by the string as described above
  if (sequence == "12"):
    headcount += 1
    print(f"Someone entered the room! Headcount is now: {headcount}")
    sequence=""
    time.sleep(2)
  elif (sequence == "21") and (headcount > 0):
    headcount -=  1 
    print(f"Someone left the room! Headcount is now: {headcount}")
    sequence=""
    time.sleep(2)
  
  #Resets the sequence if it is invalid or a timeout occurs
  if(len(sequence) > 2) or (sequence == "11") or (sequence == "22") or (timeoutCounter > 20):
    print("Timeout Occured")
    sequence=""  

  # Increment timeoutCounter to prevent misfires changing the output
  if (len(sequence) == 1):
    timeoutCounter += 1
  else:
    timeoutCounter=0

GPIO.cleanup() 