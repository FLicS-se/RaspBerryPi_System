import RPi.GPIO as GPIO
import time
import os
import pexpect
import getpass
import subprocess
import datetime
from multiprocessing import Pool

PIRPinIn = 18
PIRPinOut = 17
RUNTIME = 1 
TIMESLEEP = 2 
i = 0
flag = 0

def setup():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(PIRPinIn, GPIO.IN)
	GPIO.setup(PIRPinOut, GPIO.IN)

def main():
	global i
	global flag
	while True:
		if(flag==0):
			t1=time.time()
			#time=datetime.datetime.now()
			#t1=time.day
			flag=1
		elif(time.time() - t1 > 86400):
		#elif(t1 != time.day):
			flag=0
			i = 0
			#print("10")
		elif(GPIO.input(PIRPinIn)!=0):
		#elif(GPIO.input(PIRPinIn)!=0):
			starttime=time.time()
			runtime = 0
			print('********************')
			print('*    In Sensor!    *')
			print('********************')
			print('\n')
			while(runtime < RUNTIME):
				runtime = time.time() - starttime
				if(GPIO.input(PIRPinOut)!=0):
					print("=============")
					print("    Out    ")
					print("=============")
					i = i - 1
					f = open('txt.txt', 'w')
					f.write(str(i))
					f.close()
					subprocess.call(["scp -i flics-ec2.pem txt.txt ubuntu@13.114.169.85:/var/www/html/api"], shell = True)	
					time.sleep(TIMESLEEP)
					setup()
					break
			time.sleep(1)

		elif(GPIO.input(PIRPinOut)!=0):
			starttime=time.time()
			runtime = 0
			print('********************')
			print('*    Out Sensor    *')
			print('********************')
			print('\n')
			while(runtime < RUNTIME):
				runtime = time.time() - starttime
				if(GPIO.input(PIRPinIn)!=0):
					print("===============")
					print("     In     ")
					print("===============")
					i = i + 1
					f = open('txt.txt', 'w')
					f.write(str(i))
					f.close()
					subprocess.call(["scp -i flics-ec2.pem txt.txt ubuntu@13.114.169.85:/var/www/html/api"], shell = True)
					time.sleep(TIMESLEEP)
					break
			time.sleep(1)
		else:
			print('====================')
			print('=    Not alarm...  =')
			print('====================')
			print('\n')
		time.sleep(1)

if __name__ == '__main__':
	setup()
	try:
		main()
	except KeyboardInterrupt:
		destroy()
		pass
