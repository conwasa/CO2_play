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
#import subprocess
from sys     import stderr

#print '<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'  
#print 'parms passed to find_pips_v3.py:'
#print '$1=', sys.argv[1] 
#print '$2=', sys.argv[2]
#print '$3=', sys.argv[3]
#print '$4=', sys.argv[4]
#print '<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'  

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


#    underline='\033[04m'
#    reverse='\033[07m'
#    strikethrough='\033[09m'

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
			line1 			= data['line1']
			line2 			= data['line2']
			line3 			= data['line3']
			site_location	= data['site_location']
			last_reading	= data['last_reading']
			lowest_reading	= data['lowest_reading']
			highest_reading	= data['highest_reading']
  
except IOError:
	prYellow('stats.py: cannot read twitter_keys.json')
	sys.exit()

print (line1)
print (line2)
print (line3)

try:
	with open('apikeys/twitter_keys.json') as json_data2:
		data = json.load(json_data2)
		if bool(data) == False: # empty dictionary
			prYellow('tweet.py: twitter_keys.json is empty')
			sys.exit()
		else:
			consumer_key 		= data['consumer_key']
			consumer_secret 	= data['consumer_secret']
			access_token_key 	= data['access_token_key']
			access_token_secret	= data['access_token_secret']
except IOError:
	prYellow('tweet.py: cannot read twitter_keys.json')
	sys.exit()

print (consumer_key)
print (consumer_secret)
print (access_token_key)
print (access_token_secret)

api = twitter.Api(consumer_key=consumer_key,
					consumer_secret = consumer_secret,
					access_token_key = access_token_key,
					access_token_secret = access_token_secret)
					
print (api.VerifyCredentials())
#message = "Hello World! Lets try some ways to get a subscript '2': unicode:" + u"\u2082" + " and the html entity: 	&#8322;" 
#post_update = api.PostUpdates(status=message)

line1_clean = line1.replace('&nbsp;','').replace(':',': ')

message = "Outdoor CO" + u"\u2082" + " at " + str(site_location) + ", " + line1_clean + ". Graphs and info at https://conwasa.github.io/CO2_play/ #CO2"
post_update = api.PostUpdates(status=message)
print (message)
			
	
