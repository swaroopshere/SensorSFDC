import os
import glob
import time
import random
from simple_salesforce import Salesforce

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

sensor1_serial = '28-000005978b86'
sensor2_serial = '28-00000605f87f'
base_dir = '/sys/bus/w1/devices/'
#device_file = device_folder + '/w1_slave'
config_file = '/home/pi/Dreamforce/timeinterval'
def read_config():
    f = open(config_file, 'r')
    interval = f.readline()
    return interval

def read_temp_raw(sensor_serial_number):
    device_folder = glob.glob(base_dir + sensor_serial_number)[0]
    device_file = device_folder + '/w1_slave'
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp(sensor_serial_number):
    lines = read_temp_raw(sensor_serial_number)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

#def get_Room_Name():
#    room=['LivingRoom','Kitchen','Bedroom1','MasterBed','Garage']
#    return random.choice(room)

def send_Data_SFDC(sensor1_serial,temp_c, temp_f):
    print(sensor1_serial,temp_c, temp_f)
    sf=Salesforce(username='sensor@tempsensor.org',password='Raspberry20',security_token='FNfOKLMAr6USzUNYJ7SclHnt');
#    roomName = get_Room_Name()
    sf.Temperature__c.create({'Name':sensor1_serial,'Celcius__c':temp_c,'Farenheit__c':temp_f})

#def close():
#    print "Disconnect"
#    GPIO.cleanup()
	
while True:
	temp_c, temp_f = read_temp(sensor1_serial)
        send_Data_SFDC(sensor1_serial,temp_c,temp_f)
	temp_c, temp_f = read_temp(sensor2_serial)
	send_Data_SFDC(sensor2_serial,temp_c, temp_f)
	sleepTime=read_config()
	print(sleepTime)
	time.sleep(int(sleepTime))

#except (KeyboardInterrupt):
#    print "Interrupt received"
#    close()
