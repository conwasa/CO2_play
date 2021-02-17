# -*- coding: utf-8 -*-
import os
import json
import csv
import re
import sys
import time
import datetime
from datetime import timedelta
import io   # for utf-8 encoding
from sys     import stderr
# python-telegram-bot.org specific imports
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
#enable logging
logging.basicConfig(
	format='%asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def get_latest_stats():

	try:
		with open('stats.json') as json_data2:
			data = json.load(json_data2)
			if bool(data) == False: # empty dictionary
				prYellow('telegram_bot.py: stats.json is empty')
				sys.exit()
			else:
				line1 			= data['line1']
				line2 			= data['line2']
				line3 			= data['line3']
				site_location	= data['site_location']
				last_reading	= data['last_reading']
				lowest_reading	= data['lowest_reading']
				highest_reading	= data['highest_reading']
				weekly_trend	= data['weekly_trend']
				monthly_trend	= data['monthly_trend']
				annual_trend	= data['annual_trend']

	except IOError:
		print ('stats.py: cannot read stats.json')
		sys.exit()

	line1_clean = line1.replace('&nbsp;','').replace('reading:','reading: ')

	if last_reading	== lowest_reading:
		message = "Record low outdoor CO" + u"\u2082" + " at " + str(site_location) + line1_clean[12:] + ". This is the lowest value recorded since 15th November 2018. Graphs and info at https://conwasa.github.io/CO2_play/ #CO2"
		print (message)

	elif last_reading	== highest_reading:
		message = "Record high outdoor CO" + u"\u2082" + " at " + str(site_location) + line1_clean[12:] + ". This is the highest value recorded since 15th November 2018. Graphs and info at https://conwasa.github.io/CO2_play/ #CO2"
	else:
		message = "Outdoor CO" + u"\u2082" + " at " + str(site_location) + ", " + line1_clean + ". Graphs and info at https://conwasa.github.io/CO2_play/ \n#CO2"

	if int(last_reading) > 1000:
		co2_gt_1000_value = int(last_reading)
	else:
		co2_gt_1000_value = 0
		
	return ([message, site_location, co2_gt_1000_value, weekly_trend, monthly_trend, annual_trend])
	
def get_spoken_time_since_last_char(time_since_last_chat):
	mins_since_last_chat = int(time.strftime("%M", time.localtime(time_since_last_chat)))
	hours_since_last_chat = int(time.strftime("%H", time.localtime(time_since_last_chat)))
	days_since_last_chat = int(time.strftime("%j", time.localtime(time_since_last_chat))) - 1
	years_since_last_chat = int(time.strftime("%Y", time.localtime(time_since_last_chat))) - 1970
	if years_since_last_chat != 0:
		days_since_last_chat = days_since_last_chat + years_since_last_chat * 365
	if days_since_last_chat == 1:
		hours_since_last_chat = hours_since_last_chat + 24
		days_since_last_chat = 0
	if hours_since_last_chat == 1:
		mins_since_last_chat = mins_since_last_chat + 60
		hours_since_last_chat = 0
	spoken_time_since_last_chat = str(mins_since_last_chat) + " minutes"
	if hours_since_last_chat != 0:
		spoken_time_since_last_chat = str(hours_since_last_chat) + " hours and " + spoken_time_since_last_chat 
	if days_since_last_chat != 0:
		spoken_time_since_last_chat = str(days_since_last_chat) + " days, " + spoken_time_since_last_chat 
	return (spoken_time_since_last_chat)
	

def load_subscriptions_dict():
# I didn't know about the pickle library at the time of writing. 
# search 'python pickle dictionary' for more information.
	subscriptions_dict = {}
	 
	try:
		with open('subscriptions.json') as json_data:
			subscriptions_dict = json.load(json_data)
			if bool(subscriptions_dict) == False: # empty dictionary
				prYellow('telegram_bot.py: subscription dictionary empty')
				sys.exit()
	except (ValueError, IOError):
		# first run, create empty topic lists
		subscriptions_dict = {  'new records' : [],
								'all readings' : [], 
								'service msgs' : [], 
								'dev news' : [],
								'weekly trend' : [],
								'monthly trend' : [],
								'annual trend' : []
		}
		with open('subscriptions.json', 'w') as write_file:
			json.dump(subscriptions_dict, write_file, indent=2) 
		
	return subscriptions_dict

def add_subscription(subscriptions_dict, chat_id, topic, context):
	chat_id_list = subscriptions_dict[topic]
	if chat_id not in chat_id_list: 
		chat_id_list.append(chat_id)
		subscriptions_dict[topic] = chat_id_list
		with open('subscriptions.json', 'w') as write_file:
			json.dump(subscriptions_dict, write_file, indent=2) 
		context.bot.send_message(chat_id=chat_id, text="you are subscribed to " + topic)
	else:
		context.bot.send_message(chat_id=chat_id, text="you are already subscribed to " + topic)
	return subscriptions_dict

def remove_subscription(subscriptions_dict, chat_id, topic, context):
	chat_id_list = subscriptions_dict[topic]
	if chat_id in chat_id_list: 
		chat_id_list.remove(chat_id)
		subscriptions_dict[topic] = chat_id_list
		with open('subscriptions.json', 'w') as write_file:
			json.dump(subscriptions_dict, write_file, indent=2) 
		context.bot.send_message(chat_id=chat_id, text="you are unsubscribed from " + topic)
	else:
		context.bot.send_message(chat_id=chat_id, text="you are already unsubscribed from " + topic)
	return subscriptions_dict

def	notify_subscribers(subscriptions_dict, topic, message):
	chat_id_list = subscriptions_dict[topic]
	for chat_id in chat_id_list:
		updater.bot.send_message(chat_id=chat_id, text=message)

def send_start_and_reply_msg(update, context):
	print ("telegram chatbot event chat_id=" + str(update.effective_chat.id) + " received message=" + update.message.text)
	epoch_time_now = int(time.time())
	time_since_last_chat = epoch_time_now - last_spoken_to_epoch_time
	if time_since_last_chat > 6000:  # 6000 seconds is 10 minutes
		spoken_time_since_last_chat = get_spoken_time_since_last_char(time_since_last_chat)
		context.bot.send_message(chat_id=update.effective_chat.id, text="Thank you, no-one has spoken to me for " + spoken_time_since_last_chat + ".")
		
	stats_list = get_latest_stats()
	co2_message = stats_list[0]
	context.bot.send_message(chat_id=update.effective_chat.id, text=co2_message)
	context.bot.send_message(chat_id=update.effective_chat.id, text="I measure local outdoor CO" + u"\u2082" + " levels and send messages about readings and trends.\n\nType or tap '/help' for commands.")

def format_service_message(update, context, activity_name):
	chat_id = str(update.message.chat_id)
	first_name = update.message.chat.first_name
	last_name = update.message.chat.last_name
	username = update.message.chat.username
	print("chat_id : {} and firstname : {} lastname : {}  username {}". format(chat_id, first_name, last_name , username))
	message = first_name + " " + activity_name  # chat_id removed as anyone can subscribe to 'service msgs' and it could be spammed
	return message

def	join_and_print(chat_id, cmd, list):
	chat_id = str(chat_id)
	parm = ' '.join(list)
	print (chat_id + " command=/" + cmd + " " + parm)
	return (parm)
	
# MAIN SECTION

subscriptions_dict = load_subscriptions_dict()

try:
	with open('apikeys/telegram_keys.json') as json_data2:
		data = json.load(json_data2)
		if bool(data) == False: # empty dictionary
			prYellow('telegram_bot.py: telegram_keys.json is empty')
			sys.exit()
		else:
			telegram_co2_bot_token	= data['telegram_co2_bot_token']
except IOError:
	prYellow('telegram_bot.py: cannot read telegram_keys.json')
	sys.exit()

last_spoken_to_epoch_time = int(time.time())

stats_list = get_latest_stats()
co2_message = stats_list[0]
site_location = stats_list[1]

from telegram.ext import Updater
updater = Updater(token=telegram_co2_bot_token, use_context=True)

dispatcher = updater.dispatcher

def start(update, context):
	send_start_and_reply_msg(update, context)
	message = format_service_message(update, context, 'has started this bot.')
	notify_subscribers(subscriptions_dict, 'service msgs', message)
	
	from telegram.ext import CommandHandler
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def reply(update, context):
	send_start_and_reply_msg(update, context)
	message = format_service_message(update, context, 'is chatting: ' + update.message.text)
	notify_subscribers(subscriptions_dict, 'service msgs', message)
	
from telegram.ext import MessageHandler, Filters
reply_handler = MessageHandler(Filters.text & (~Filters.command), reply)
dispatcher.add_handler(reply_handler)

def help(update, context):
	message = """Commands:
	/sub <topic> - subscribe to a topic
	/unsub <topic> - unsubscribe
	/info  <topic> - details of a topic
	/show <data> - interactive console
	/help - this message
	
	Topics are:
	weekly trend - end of week summary of trend
	monthly trend - end of month summary of trend
	annual trend - end of year summary of trend
	all trends - weekly, monthly and annual trends
	
	new records - record high or low values
	all readings - a message every 10 minutes
	
	service msgs - mainly for the robot's owner
	dev news - my software and maker stuff
	
	all - all of the above
	
	Data:
	subs - list your subscriptions
	trends - list the last trend records
	last reading - shows the last reading

	example:
	/sub monthly trend\n"""
	
	context.bot.send_message(chat_id=update.effective_chat.id, text=message)
	message = format_service_message(update, context, '/help ')
	notify_subscribers(subscriptions_dict, 'service msgs', message)
#	/about - how school teachers can use this\n

help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)

# topic descriptions for the /info command
new_records_info = """Info: 'new records' topic. Messages look like this:\n
	Record low outdoor CO""" + u"\u2082" + """ at """ + str(site_location) + """: 381ppm at 12:57 on Wednesday 24 Apr 2019. This is the lowest value recorded since 15th November 2018. Graphs and info at https://conwasa.github.io/CO2_play/ #CO2\n
	Record high outdoor CO""" + u"\u2082" + """ at """ + str(site_location) + """: 625ppm at 09:24 on Thursday 05 Dec 2019. This is the highest value recorded since 15th November 2018. Graphs and info at https://conwasa.github.io/CO2_play/ #CO2"\n
	Expect one message or so a year."""

all_readings_info = "Info: 'all readings' topic. A message wen a new reading is taken. Messages look like this:\n\n" + co2_message + "\n\nExpect a message every 10 minutes."

service_msgs_info = """Info: 'service msgs' topic. Messages for this Bot's owner. They look like this:\n
	Alex has started this bot.
	Bob is chatting: hello
	Bob /info dev news
	The CO2 sensor is offline.
	High CO2 1500ppm. Possible fire.\n
	Expect a few messages a week."""
	
dev_news_info = """Info: 'dev news' topic.\nNews of updates to this robot and others. \n
	Expect one message every month or so."""
		
weekly_trend_info = "Info: 'weekly trend' topic. Sent at 9am (" + site_location + """) Mondays, giving the trend based the average of previous Monday's and Sunday's readings. Messages look like tis:
	
	Weekly CO2 trend: up 3.0 percent from 492 to 502 ppm 

	Expect one message a week."""

monthly_trend_info = "Info: 'monthly trend' topic. Sent at 9am (" + site_location + """) on the first of each month, giving the trend based the average reading of the first and last days of the previous month. Messages look like tis:
	
	Monthly CO2 trend: up 1.6 percent from 490 to 492 ppm 

	Expect one message a month."""

annual_trend_info = "Info: 'annual trend' topic. Sent at 9am (" + site_location + """) on the first day of year, giving the trend based the average reading of the first and last days of the previous year. Messages look like tis:
	
	Annual CO2 trend: down 2.6 percent from 492 to 486 ppm 

	Expect one message a year."""

all_trends_info = """Info: 'all trends' topic. All three trend topics. Messages look like this:
	
	Weekly CO2 trend: up 3.0 percent from 492 to 502 ppm 
	Monthly CO2 trend: up 1.6 percent from 490 to 492 ppm 
	Annual CO2 trend: down 2.6 percent from 492 to 486 ppm 

	Expect one or so message a week."""

all_info = """Info: 'all' topic. All messages from this Bot.\n
	Expect one message every 10 minutes plus a few more a day."""

show_subs_info = """Info: 'show subs' topic. Lists your subscribed topics .\n
	On demand."""
	
def info(update, context):
	parm = join_and_print(update.effective_chat.id, 'info', context.args)
#	parm = ' '.join(context.args)
	if parm == 'new records':
		message = new_records_info
	elif parm == 'all readings':
		message = all_readings_info
	elif parm == 'service msgs':
		message = service_msgs_info
	elif parm == 'dev news':
		message = dev_news_info
	elif parm == 'weekly trend':
		message = weekly_trend_info
	elif parm == 'monthly trend':
		message = monthly_trend_info
	elif parm == 'annual trend':
		message = annual_trend_info
	elif parm == 'all trends':
		message = all_trends_info
	elif parm == 'all':
		message = new_records_info + "\n\n" + all_readings_info + "\n\n" + service_msgs_info + "\n\n" + dev_news_info + "\n\n" + weekly_trend_info + "\n\n" + monthly_trend_info + "\n\n" + annual_trend_info + "\n\n" + all_trends_info + "\n\n" + all_info
	elif parm == 'show_subs':
		message = show_subs_info
	elif parm == '':
		context.bot.send_message(chat_id=update.effective_chat.id, text='you must specify one of tese topics:\n\nnew records\nall readings\nservice msgs\ndev news\nall')
	else:
		message = parm + " not found, see /help"
	context.bot.send_message(chat_id=update.effective_chat.id, text=message)
	message = format_service_message(update, context, '/info ' + parm)
	notify_subscribers(subscriptions_dict, 'service msgs', message)

info_handler = CommandHandler('info', info)
dispatcher.add_handler(info_handler)

def sub(update, context):
	parm = join_and_print(update.effective_chat.id, 'sub', context.args)
	if parm in ['new records', 'all readings', 'service msgs', 'dev news', 'weekly trend', 'monthly trend', 'annual trend' ]:
		add_subscription(subscriptions_dict, str(update.effective_chat.id), parm, context)
	elif parm == 'all trends':
		add_subscription(subscriptions_dict, str(update.effective_chat.id), 'weekly trend', context)
		add_subscription(subscriptions_dict, str(update.effective_chat.id), 'monthly trend', context)
		add_subscription(subscriptions_dict, str(update.effective_chat.id), 'annual trend', context)
	elif parm == 'all':
		add_subscription(subscriptions_dict, str(update.effective_chat.id), 'new records', context)
		add_subscription(subscriptions_dict, str(update.effective_chat.id), 'all readings', context)
		add_subscription(subscriptions_dict, str(update.effective_chat.id), 'service msgs', context)
		add_subscription(subscriptions_dict, str(update.effective_chat.id), 'dev news', context)
		add_subscription(subscriptions_dict, str(update.effective_chat.id), 'weekly trend', context)
		add_subscription(subscriptions_dict, str(update.effective_chat.id), 'monthly trend', context)
		add_subscription(subscriptions_dict, str(update.effective_chat.id), 'annual trend', context)
	elif parm == '':
		context.bot.send_message(chat_id=update.effective_chat.id, text='you must specify one of tese topics:\n\nnew records\nall readings\nservice msgs\ndev news\nall')
	else:
		message = parm + " is not a valid topic, see /help"
		context.bot.send_message(chat_id=update.effective_chat.id, text=message)
	message = format_service_message(update, context, '/sub ' + parm)
	notify_subscribers(subscriptions_dict, 'service msgs', message)

sub_handler = CommandHandler('sub', sub)
dispatcher.add_handler(sub_handler)

def unsub(update, context):
	parm = join_and_print(update.effective_chat.id, 'sub', context.args)
	if parm in ['new records', 'all readings', 'service msgs', 'dev news', 'weekly trend', 'monthly trend', 'annual trend' ]:
		remove_subscription(subscriptions_dict, str(update.effective_chat.id), parm, context)
	elif parm == 'all trends':
		remove_subscription(subscriptions_dict, str(update.effective_chat.id), 'weekly trend', context)
		remove_subscription(subscriptions_dict, str(update.effective_chat.id), 'monthly trend', context)
		remove_subscription(subscriptions_dict, str(update.effective_chat.id), 'annual trend', context)
	elif parm == 'all':
		remove_subscription(subscriptions_dict, str(update.effective_chat.id), 'new records', context)
		remove_subscription(subscriptions_dict, str(update.effective_chat.id), 'all readings', context)
		remove_subscription(subscriptions_dict, str(update.effective_chat.id), 'service msgs', context)
		remove_subscription(subscriptions_dict, str(update.effective_chat.id), 'dev news', context)
		remove_subscription(subscriptions_dict, str(update.effective_chat.id), 'weekly trend', context)
		remove_subscription(subscriptions_dict, str(update.effective_chat.id), 'monthly trend', context)
		remove_subscription(subscriptions_dict, str(update.effective_chat.id), 'annual trend', context)
	elif parm == '':
		context.bot.send_message(chat_id=update.effective_chat.id, text='you must specify one of tese topics:\n\nnew records\nall readings\nservice msgs\ndev news\nall')
	else:
		message = parm + " is not a valid topic, see /help"
		context.bot.send_message(chat_id=update.effective_chat.id, text=message)
	message = format_service_message(update, context, '/unsub ' + parm)
	notify_subscribers(subscriptions_dict, 'service msgs', message)
	
unsub_handler = CommandHandler('unsub', unsub)
dispatcher.add_handler(unsub_handler)

def show_sub(subscriptions_dict, topic, update, context):
	chat_id = update.message.chat_id
	chat_id_list = subscriptions_dict[topic]
	
	if str(chat_id) in chat_id_list:
		context.bot.send_message(chat_id=chat_id, text="you are subscribed to " + topic)
		return True
	else:
		return False
		
def show(update, context):
	parm = join_and_print(update.effective_chat.id, 'show', context.args)
	if parm == 'subs':
		has_subs = False
		for topic in ['new records', 'all readings', 'service msgs', 'dev news', 'weekly trend', 'monthly trend', 'annual trend' ]:
			subbed = show_sub(subscriptions_dict, topic, update, context)
			if subbed == True:
				has_subs = True
		if has_subs == False:
			context.bot.send_message(chat_id=update.effective_chat.id, text='you have no subscriptions')
	elif parm == 'trends':
		context.bot.send_message(chat_id=update.effective_chat.id, text=weekly_trend)
		context.bot.send_message(chat_id=update.effective_chat.id, text=monthly_trend)
		context.bot.send_message(chat_id=update.effective_chat.id, text=annual_trend)
	elif parm == 'last reading':
		context.bot.send_message(chat_id=update.effective_chat.id, text=co2_message)
	elif parm == '':
		context.bot.send_message(chat_id=update.effective_chat.id, text='you must specify one of tese topics:\n\nnew records\nall readings\nservice msgs\ndev news\nall')
	else:
		message = parm + " is not a valid data set, see /help"
		context.bot.send_message(chat_id=update.effective_chat.id, text=message)
	
show_handler = CommandHandler('show', show)
dispatcher.add_handler(show_handler)

# timer section
job_queue = updater.job_queue

def send_weekly_message(context):
	notify_subscribers(subscriptions_dict, 'weekly trend', weekly_trend)
job_queue.run_daily(send_weekly_message, datetime.time(9, 00, 00, 000000),days=[0])

def send_monthly_message(context):
	notify_subscribers(subscriptions_dict, 'monthly trend', monthly_trend)
job_queue.run_monthly(send_monthly_message, datetime.time(9, 00, 00, 000000), 1)

now = datetime.datetime.now()
next_year = now.year + 1
annual_msg_datetime = datetime.datetime(next_year, 1, 1, 9, 00)
def send_annual_message(context):
	notify_subscribers(subscriptions_dict, 'annual trend', annual_trend)
	next_year = now.year + 1
	job_queue.run_once(send_annual_message, annual_msg_datetime)
job_queue.run_once(send_annual_message, annual_msg_datetime)

#this must be last
def unknown(update, context):
	context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")
unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

updater.start_polling()

old_co2_message = ''
while True:
	stats_list = get_latest_stats()
	co2_message = stats_list[0]
	co2_gt_1000_value = stats_list[2]
	weekly_trend = stats_list[3]
	monthly_trend = stats_list[4]
	annual_trend = stats_list[5]
	if co2_message != old_co2_message:
		now = datetime.datetime.now()
		print (str(now.strftime("%Y-%m-%d %H:%M:%S")) + " " + co2_message)
		old_co2_message = co2_message
		notify_subscribers(subscriptions_dict, 'all readings', co2_message)
		if 'Record' in co2_message:
			notify_subscribers(subscriptions_dict, 'new records', co2_message)
	
	try:
		f = open("alarm_flag_for_telegram_bot.flag")
		notify_subscribers(subscriptions_dict, 'service msgs', 'The CO2 sensor is offline')
		f.close()
		os.remove("alarm_flag_for_telegram_bot.flag")
	except IOError:
		pass
	
	if co2_gt_1000_value > 0:
		notify_subscribers(subscriptions_dict, 'service msgs', 'High CO2 ' + str(co2_gt_1000_value) + 'ppm. Possible fire.')

	time.sleep (10)