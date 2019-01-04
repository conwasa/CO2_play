# -*- coding: utf-8 -*-
import json
import csv
import re
import sys
import time
import datetime
from datetime import timedelta

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
def prStrikethrough(skk): 			print(u"\033[09m {}\033[00m" .format(skk)), 
def prBoldStrikethrough(skk): 		print(u"\033[1m\033[09m {}\033[00m" .format(skk)), 
def prBoldUnderline(skk): 			print(u"\033[1m\033[04m {}\033[00m" .format(skk)), 
def prInverseStrikethrough(skk):	print(u"\033[7m\033[09m {}\033[00m" .format(skk)), 
def prInverseUnderline(skk): 		print(u"\033[7m\033[04m {}\033[00m" .format(skk)), 



def read_csv_file():
#	with open(filename, mode="r", encoding="utf-8") as json_data:
	with open('all_readings.csv', 'rt') as all_data_file:
		try:
			levels_reader1 = csv.reader(all_data_file, delimiter=',')
			csv_data_list = list(levels_reader1)

		except ValueError:
			prRed('process_csv.py error reading file 1')
			
	return(csv_data_list)

def get_subset(list, start_date, end_date, y_value):
	returned_list = []
	for i in range (0, len(list), 1):
		row = []
		if start_date <= list[i][0] <= end_date:
			if y_value == 'day_of_week':
				row.append(datetime.date.fromisoformat(list[i][0]).strftime("%a"))
			elif y_value == 'day_of_month':
				row.append(datetime.date.fromisoformat(list[i][0]).strftime("%d"))
			elif y_value == 'month':
				row.append(datetime.date.fromisoformat(list[i][0]).strftime("%b"))
			else:
				row.append(list[i][y_value])  # time 
			row.append(list[i][2])  # time 
			returned_list.append(row)	
	return(returned_list)

def write_subset(list, filename, header):
	with open(filename, mode='w',newline='') as output_file:    # newline = '' for Windows as otherwise it outputs an extra CR
		output_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		output_writer.writerow(header)
		for i in range (0, len(list), 1):
			output_writer.writerow(list[i])

def write_outage_csv(list1):
	last_record_datetime = datetime.datetime.fromisoformat('1970-01-01 00:00')
	good_delta = datetime.datetime.fromisoformat('1970-01-01 00:20') - datetime.datetime.fromisoformat('1970-01-01 00:00')
	with open('outages.csv', mode='w',newline='') as output_file:    # newline = '' for Windows as otherwise it outputs an extra CR
		output_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		output_writer.writerow(['outages > 10m','duration [hh:mm]'])

		flag = False
		last_outage_text = ''
		for i in range (len(list1)-1, 0, -1):
			record_datetime = datetime.datetime.fromisoformat(list1[i][0] + ' ' + list1[i][1])
			delta = last_record_datetime - record_datetime  
			if delta > good_delta:
				outage = delta 
				if len(str(outage)) == 7:
					outage_str = '0' + str(outage)[:-3]
				else:
					outage_str = str(outage)[:-3]
				output_writer.writerow([str(record_datetime), outage_str])
				if flag == False:
					last_outage_text = 'last outage: ' + str(record_datetime) + ' for ' + outage_str + ' [hh:mm]' 
					flag = True
#				print (str(i) + ' ' + str(record_datetime) + ' ' + str(delta))
#				print ('len=' + str(len(str(outage))))
			last_record_datetime = record_datetime
		return(last_outage_text)
			
def write_stats(list1, last_outage_text):
	lowest_reading 	= '999'
	latest_reading 	= '000'
	highest_reading = '000'
	last_record_datetime = datetime.datetime.fromisoformat('1970-01-01 00:00')
	
	for i in range (0, len(list1), 1):
		if  list1[i][2] < lowest_reading:   # these are strings not numbers
			lowest_reading = list1[i][2]
			lowest_reading_datetime_str = list1[i][0]
		if  list1[i][2] > highest_reading:   # these are strings not numbers
			highest_reading = list1[i][2]
			highest_reading_datetime_str = list1[i][0]


	headers_list = []
	text = {}
	text = { text: 'latest reading: ' + list1[-1][2] + 'ppm at ' + list1[-1][0]}
	headers_list.append(text)
	
	text = { text: 'lowest reading: ' + lowest_reading + 'ppm at ' + lowest_reading_datetime_str}  
	headers_list.append(text)

	text = { text: 'highest reading: ' + highest_reading + 'ppm at ' + highest_reading_datetime_str}  
	headers_list.append(text)
	
	header_dict = {header_lines: headers_list} 
		
	print (header_dict)
	with open('stats.json', 'w') as write_file:
		json.dump(header_dict, write_file, indent=2) 

def	pad_rest_of_day_with_zeros(list1):
	
	list2 = list1.copy()
	
	last_record_datetime = datetime.datetime.fromisoformat(list1[-1][0] + ' ' + list1[-1][1])
	end_of_day = last_record_datetime.replace(hour=23).replace(minute=59)
	
	next_ts = last_record_datetime + timedelta(minutes=10)
	while next_ts < end_of_day:
		list2.append([str(next_ts.date()), str(next_ts.time())[:-3], 420])
		next_ts = next_ts +   timedelta(minutes=10) 
	return(list2)	
		
# MAIN SECTION

list1=read_csv_file()
#sort into date and time
list1.sort(key=lambda x: x[0:1])
#list1=sorted(list1)

list2=pad_rest_of_day_with_zeros(list1)

todays_date=datetime.date.isoformat(datetime.date.today())
todays_readings=get_subset(list2, todays_date, todays_date, 1)
write_subset(todays_readings, 'todays_readings.csv', ['time','co2_ppm'])

yesterdays_date=datetime.date.isoformat(datetime.date.today() - timedelta(days=1))
yesterdays_readings=get_subset(list1, yesterdays_date, yesterdays_date, 1)
write_subset(yesterdays_readings, 'yesterdays_readings.csv', ['time','co2_ppm'])

day_befores_date=datetime.date.isoformat(datetime.date.today() - timedelta(days=2))
day_befores_readings=get_subset(list1, day_befores_date, day_befores_date, 1)
write_subset(day_befores_readings, 'day_befores_readings.csv', ['time','co2_ppm'])

num_days_since_monday=((datetime.date.today().weekday()))
num_days_to_sunday = 6 - num_days_since_monday
last_monday_week=datetime.date.isoformat(datetime.date.today() - timedelta(weeks=1) - timedelta(days=num_days_since_monday))
last_sunday=datetime.date.isoformat(datetime.date.today() - timedelta(weeks=1) + timedelta(days=num_days_to_sunday))
last_weeks_readings=get_subset(list1, last_monday_week, last_sunday, 'day_of_week')
write_subset(last_weeks_readings, 'last_weeks_readings.csv', ['day','co2_ppm'])

day_of_month=((datetime.date.today().weekday()))
num_days_to_sunday = 6 - num_days_since_monday
last_monday_week=datetime.date.isoformat(datetime.date.today() - timedelta(weeks=1) - timedelta(days=num_days_since_monday))
last_sunday=datetime.date.isoformat(datetime.date.today() - timedelta(weeks=1) + timedelta(days=num_days_to_sunday))
last_weeks_readings=get_subset(list1, last_monday_week, last_sunday, 'day_of_week')
write_subset(last_weeks_readings, 'last_weeks_readings.csv', ['day','co2_ppm'])

end_of_last_month=datetime.date.today().replace(day=1) - datetime.timedelta (days = 1)
start_of_last_month=end_of_last_month.replace(day=1)
last_months_readings=get_subset(list1, str(start_of_last_month), str(end_of_last_month), 0)
#last_months_readings=get_subset(list1, str(start_of_last_month), str(end_of_last_month), 'day_of_month')
write_subset(last_months_readings, 'last_months_readings.csv', ['day','co2_ppm'])

all_historic_readings=get_subset(list1, '2018-11-15', '2999-12-31', 'month')
write_subset(all_historic_readings, 'all_historic_readings.csv', ['month','co2_ppm'])

outage_text=write_outage_csv(list1)
write_stats(list1, outage_text)




print ("Current year: ", datetime.date.today().strftime("%Y"))
print ("Month of year: ", datetime.date.today().strftime("%m"))
print ("Week number of the year: ", datetime.date.today().strftime("%W"))
print ("Weekday of the week: ", datetime.date.today().strftime("%w"))
print ("Day of year: ", datetime.date.today().strftime("%j"))
print ("Day of the month : ", datetime.date.today().strftime("%d"))
print ("Day of week: ", datetime.date.today().strftime("%A"))
print ("Day of week: ", datetime.date.today().strftime("%a"))
print ("ISO: ",datetime.date.isoformat(datetime.date.today())) 