import RPi.GPIO as GPIO
import gspread
import time

# Setup creds and login to spreadsheet to update data
credentials = {
  "type": "service_account",
  "project_id": "pcount-331110",
  "private_key_id": "1220a0317507a27a5b07a02e3b24af2fccbb47e5",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDja5b+x70tkUq3\nmzg2nGckZvfcI6efXHdWvW2nk4+Du1FjnX8xSsqm55JY66SnY0Tf5G2WNH/vZ30L\nlTn8B4Fj6bJCgkVgx/AWntFPDkI0eoBvJ9LtrIPfq/K8D6Gc3tV+lwQnoO/CRsc/\nTH5Ii0Q4asJLhP6j87bunky9/iLTn3/dZ3tgDEIS3deyZVzntMNqpAFzjAl5H3bG\n13r6XueHBnNkeQMxPXC9JsXytxFJ4Xw3Hmxm4GZojO9YvcC6lvCfqK4zgHf6fA2S\nHSfQgyHoFOaff8WGSaKfrBBMfgyrmTbkPoWHa6HCx4cUW6r7+ozdN6r0Umnj0Dmw\n+C9/mzntAgMBAAECggEAPR9Xj9aDI9Ie8MYJD7RtjD0YdNQoYw5pDKkQ5a8lLVSV\nBV75JnhhiwZGMRv0PwDRLBOq2Gn30JJR62EKGpCx1/ahcHquxto1zv6UZtkANjaO\nelGLwVFSiDUgoibZWt4RJ1rTRQteJSr8tiiK8Fht13PqEH4IKmyASBXHrnC1T4bW\n45FhhIDWsEmp+kEVIC92eFwalwMUGVumMnxEpLDIS7l8X2JZyb2d0ETUv+XYJzrF\nR+TEqHD9tIjfb2zWJwcBzE+1lBRPYfEyxGBZkkEz1fm0d03KAPYQ9y515wy18I+C\ngeZmWSCCLJbmUyJjnkZyuRijvm8ZDZdo73ijri43iQKBgQD+4dmsuFbcDu3Sb7DJ\n+nenKT+1xZyyzXzl/YdYbnWMx1+Hf2oJzDc6eCesSP/4RqFLwCkMLe0UzEYOKZiQ\n+0C/nTYpQDQdofWLB5k5xSS2HKZLRUvqBU1pOAfYEdxuraznqI9AVQhzD75qlGx+\n4rRt058AM7BRzg9fLa1Ed2PrQwKBgQDkauig2JD9AZP1gcvO4AiL2WhwQnJye2La\n/pZnih4gk54VXKIC1x+9b7d90ehHl76gdAWd4wCK4YIIc04mL6NEaF28yuy6S36f\nS5ivXY+wjUqzo2uteof7tHJpKEBmbMQ9Ewjh914MLhBdb8qQonGfB5Ikw3DGBD9v\npZlME9g7DwKBgQC7xnPxVVVYhf8bm4FpLAdetXrkVZOd/tlXLzK5KZecgX2Ve38J\nfNPrVX4U5Sr/JDnMbuNOv778JYovAOIPXatT/2RZe51pf1pAdPajouPq7qxso77L\nx+BB9i+BNZdqSrUpbfsrb/nrmtuz9WkBCc/XYaKwKWRqwB5/Bk2yNSr9tQKBgCay\nkgzGA/JJNSbvwXaf7/K5d38lUrxgeQP/A74w4R/Fwo997RisF32BksWnLUILzEjk\nvxrbnXjp8Zy65C+F/JQXVmIowuhg5+fW59w17qULmu9KLXDrhGQ5UvTL0/VGUgzC\nz8twnCdWGoGp8diFHNjDcJf34IA7sf+ZP5pq9kQzAoGAdnTE6KfZemxYPB5zvrJj\n7+7bZxQ3LijMhNyzEu4tXpGLlj4Eqh94cU+QtGpDZWhAjPPNJDoTXabvBMMJQMEk\nA84X7jNovATsg7eAcoi+L+LnU4i0Wmhniu5ztZ8gNXCwTmHqp78cMFoU5tKFJqwV\nh40RfrEoOhSYj48PyUHEzIw=\n-----END PRIVATE KEY-----\n",
  "client_email": "pcount@pcount-331110.iam.gserviceaccount.com",
  "client_id": "113280603793667533962",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/pcount%40pcount-331110.iam.gserviceaccount.com"
}
gc = gspread.service_account_from_dict(credentials)
sh = gc.open("Scout")
worksheet = sh.worksheet("Pub List")
worksheet.update('K2', 0)

# Setup GPIO ports on Raspberry Pi and
# add rising edge detection on both channels
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)
GPIO.setup(18, GPIO.IN)
GPIO.add_event_detect(17, GPIO.RISING)  
GPIO.add_event_detect(18, GPIO.RISING)  
headcount = 0

# If one sensor is triggered wait for the other to trigger for movement direction + sensor error
def a_triggered():
    global headcount
    global worksheet
    # wait for up to 5 seconds for a rising edge (timeout is in milliseconds)
    channel = GPIO.wait_for_edge(18, GPIO.RISING, timeout=1000)
    if channel is None:
        print('Timeout occurred')
    else:
        headcount = headcount + 1
        print("Person entered")
        print("The headcount is currently: " + str(headcount))
        worksheet.update('K2', headcount)

def b_triggered():
    global headcount
    global worksheet
    # wait for up to 5 seconds for a rising edge (timeout is in milliseconds)
    channel = GPIO.wait_for_edge(17, GPIO.RISING, timeout=1000)
    if channel is None:
        print('Timeout occurred')
    else:
        headcount = headcount - 1
        print("Person left")
        print("The headcount is currently: " + str(headcount))
        worksheet.update('K2', headcount)

# Infinite loop to detect the initial trigger sensor
while True:
    if GPIO.event_detected(17):
        print('A_Triggered')
        a_triggered()
        
    if GPIO.event_detected(18):
        print('B_Triggered')
        b_triggered()
        
        
GPIO.cleanup()


    
    
