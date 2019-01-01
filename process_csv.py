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


			
def write_json(time_offset, station_jingles_list, ix_2_start_point, length_of_audio):
	""" outputs:
	"""
	timing_data_dict = {	'time_offset'				: time_offset,
							'station_jingles_list'		: station_jingles_list,
							'debug_ix_2_start_point' 	: ix_2_start_point,
							'length_of_audio'			: length_of_audio
							}
#	print dict
#	print publishable_transcript_dict
#	print ('>>>>>>>>>' + public_json_output_url + '/timing_data_'  + stream_name + '_' + filename_timestamp + '.json')
	with open(public_json_output_url + '/timing_data_'  + stream_name + '_' + filename_timestamp + '.json', 'w') as write_file:
		json.dump(timing_data_dict, write_file, indent=2) 

# MAIN SECTION

list1=read_csv_file()
#sort into date and time
list1.sort(key=lambda x: x[0:1])

todays_date=datetime.date.isoformat(datetime.date.today())
todays_readings=get_subset(list1, todays_date, todays_date, 1)
write_subset(todays_readings, 'todays_readings.csv', ['time','co2_ppm'])

yesterdays_date=datetime.date.isoformat(datetime.date.today() - timedelta(days=1))
yesterdays_readings=get_subset(list1, yesterdays_date, yesterdays_date, 1)
write_subset(yesterdays_readings, 'yesterdays_readings.csv', ['time','co2_ppm'])

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
last_months_readings=get_subset(list1, str(start_of_last_month), str(end_of_last_month), 'day_of_month')
write_subset(last_months_readings, 'last_months_readings.csv', ['day','co2_ppm'])

all_historic_readings=get_subset(list1, '2018-11-15', '2999-12-31', 0)
write_subset(all_historic_readings, 'all_historic_readings.csv', ['date','co2_ppm'])


# classmethod date.fromisoformat(date_string)¶

#for i in range (0, len(last_weeks_readings), 1):
#	print (last_weeks_readings[i])

	
print ('last_monday_week=' + last_monday_week)

	
print ("Current year: ", datetime.date.today().strftime("%Y"))
print ("Month of year: ", datetime.date.today().strftime("%m"))
print ("Week number of the year: ", datetime.date.today().strftime("%W"))
print ("Weekday of the week: ", datetime.date.today().strftime("%w"))
print ("Day of year: ", datetime.date.today().strftime("%j"))
print ("Day of the month : ", datetime.date.today().strftime("%d"))
print ("Day of week: ", datetime.date.today().strftime("%A"))
print ("Day of week: ", datetime.date.today().strftime("%a"))
print ("ISO: ",datetime.date.isoformat(datetime.date.today())) 