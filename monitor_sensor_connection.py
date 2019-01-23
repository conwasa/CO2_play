# -*- coding: utf-8 -*-
import json
import csv
import re
import sys
import time
import datetime
from datetime import timedelta
import twitter

import io   # for utf-8 encoding
import subprocess
from sys     import stderr


# Python program to print from https://www.geeksforgeeks.org/print-colors-python-terminal/ 
# colored text and background 
def prRed(skk): 		print(u"\033[91m {}\033[00m" .format(skk)), 
def prGreen(skk): 		print(u"\033[92m {}\033[00m" .format(skk)), 
def prYellow(skk): 		print(u"\033[93m {}\033[00m" .format(skk)), 
def prLightPurple(skk): print(u"\033[94m {}\033[00m" .format(skk)), 
def prPurple(skk): 		print(u"\033[95m {}\033[00m" .format(skk)), 
def prCyan(skk): 		print(u"\033[96m {}\033[00m" .format(skk)), 
def prLightGray(skk): 	print(u"\033[97m {}\033[00m" .format(skk)), 
def prBlack(skk): 		print(u"\033[98m {}\033[00m" .format(skk)), 

def prInverse(skk): 	print(u"\033[7m {}\033[00m" .format(skk)), 
def prBold(skk): 		print(u"\033[1m {}\033[00m" .format(skk)), 



def prUnderline(skk): 				print(u"\033[04m {}\033[00m" .format(skk)), 
def prStrikethrough(skk): 			print(u"\033[09m {}\033[00Access_token_secretm" .format(skk)), 
def prBoldStrikethrough(skk): 		print(u"\033[1m\033[09m {}\033[00m" .format(skk)), 
def prBoldUnderline(skk): 			print(u"\033[1m\033[04m {}\033[00m" .format(skk)), 
def prInverseStrikethrough(skk):	print(u"\033[7m\033[09m {}\033[00m" .format(skk)), 
def prInverseUnderline(skk): 		print(u"\033[7m\033[04m {}\033[00m" .format(skk)), 

		
# MAIN SECTION

try:
	with open('stats.json') as json_data2:
		data = json.load(json_data2)
		if bool(data) == False: # empty dictionary
			prYellow('tweet.py: stats.json is empty')
			sys.exit()
		else:
			print ("lookin g in")
			print (str(data))
			last_reading_datetime = data['last_reading_datetime']
  
except IOError:
	prYellow('stats.py: cannot read twitter_keys.json')
	sys.exit()

last_reading_datetime_dt = datetime.datetime.fromisoformat(last_reading_datetime)
a15_minutes_ago = datetime.datetime.now() - timedelta(minutes=15)
print ('last_reading_datetime=' + str(last_reading_datetime))
print ('12 minutes ago=       ' + str(a15_minutes_ago))

if last_reading_datetime_dt < a15_minutes_ago:
	shell_string = '"C:\Program Files\VideoLAN\VLC\vlc.exe" --loop morse_CO2.mp3'
	shell_string = 'alarm.bat'

	subprocess.call([shell_string], shell = True)	
