wine /home/user2/SenselifeCamSoftware/CO2_Monitor.exe &
while [ true ]; do
	rm alarm_flag_for_telegram_bot.flag
	cat /home/user2/SenselifeCamSoftware/2018/11/*.CSV |grep "20" > all_readings.csv 
	cat /home/user2/SenselifeCamSoftware/2018/12/*.CSV |grep "20" >> all_readings.csv 
	cat /home/user2/SenselifeCamSoftware/2019/01/*.CSV |grep "20" >> all_readings.csv 
	cat /home/user2/SenselifeCamSoftware/2019/02/*.CSV |grep "20" >> all_readings.csv 
	cat /home/user2/SenselifeCamSoftware/2019/03/*.CSV |grep "20" >> all_readings.csv 
	cat /home/user2/SenselifeCamSoftware/2019/04/*.CSV |grep "20" >> all_readings.csv 
	cat /home/user2/SenselifeCamSoftware/2019/05/*.CSV |grep "20" >> all_readings.csv 
	cat /home/user2/SenselifeCamSoftware/2019/06/*.CSV |grep "20" >> all_readings.csv 
	cat /home/user2/SenselifeCamSoftware/2019/07/*.CSV |grep "20" >> all_readings.csv 
	cat /home/user2/SenselifeCamSoftware/2019/08/*.CSV |grep "20" >> all_readings.csv 
	cat /home/user2/SenselifeCamSoftware/2019/09/*.CSV |grep "20" >> all_readings.csv 
	cat /home/user2/SenselifeCamSoftware/2019/10/*.CSV |grep "20" >> all_readings.csv 
	cat /home/user2/SenselifeCamSoftware/2019/11/*.CSV |grep "20" >> all_readings.csv 
	cat /home/user2/SenselifeCamSoftware/2019/12/*.CSV |grep "20" >> all_readings.csv 
	cat /home/user2/SenselifeCamSoftware/2020/01/*.CSV |grep "20" >> all_readings.csv 
	cat /home/user2/SenselifeCamSoftware/2020/02/*.CSV |grep "20" >> all_readings.csv 
	cat /home/user2/SenselifeCamSoftware/2020/03/*.CSV |grep "20" >> all_readings.csv 
	cat /home/user2/SenselifeCamSoftware/2020/04/*.CSV |grep "20" >> all_readings.csv 
	cat /home/user2/SenselifeCamSoftware/2020/05/*.CSV |grep "20" >> all_readings.csv 
	cat /home/user2/SenselifeCamSoftware/2020/06/*.CSV |grep "20" >> all_readings.csv 
	cat /home/user2/SenselifeCamSoftware/2020/07/*.CSV |grep "20" >> all_readings.csv 
	cat /home/user2/SenselifeCamSoftware/2020/08/*.CSV |grep "20" >> all_readings.csv 
	cat /home/user2/SenselifeCamSoftware/2020/09/*.CSV |grep "20" >> all_readings.csv 
	cat /home/user2/SenselifeCamSoftware/2020/10/*.CSV |grep "20" >> all_readings.csv 
	cat /home/user2/SenselifeCamSoftware/2020/11/*.CSV |grep "20" >> all_readings.csv 
	cat /home/user2/SenselifeCamSoftware/2020/12/*.CSV |grep "20" >> all_readings.csv 
	cat /home/user2/SenselifeCamSoftware/2021/01/*.CSV |grep "20" >> all_readings.csv 
	cat /home/user2/SenselifeCamSoftware/2021/02/*.CSV |grep "20" >> all_readings.csv 
	cat /home/user2/SenselifeCamSoftware/2021/03/*.CSV |grep "20" >> all_readings.csv 
	cat /home/user2/SenselifeCamSoftware/2021/04/*.CSV |grep "20" >> all_readings.csv 
	cat /home/user2/SenselifeCamSoftware/2021/05/*.CSV |grep "20" >> all_readings.csv 
	cat /home/user2/SenselifeCamSoftware/2021/06/*.CSV |grep "20" >> all_readings.csv 
	cat /home/user2/SenselifeCamSoftware/2021/07/*.CSV |grep "20" >> all_readings.csv 
	cat /home/user2/SenselifeCamSoftware/2021/08/*.CSV |grep "20" >> all_readings.csv 
	cat /home/user2/SenselifeCamSoftware/2021/09/*.CSV |grep "20" >> all_readings.csv 
	cat /home/user2/SenselifeCamSoftware/2021/10/*.CSV |grep "20" >> all_readings.csv 
	cat /home/user2/SenselifeCamSoftware/2021/11/*.CSV |grep "20" >> all_readings.csv 
	cat /home/user2/SenselifeCamSoftware/2021/12/*.CSV |grep "20" >> all_readings.csv 
	cat /home/user2/SenselifeCamSoftware/2022/01/*.CSV |grep "20" >> all_readings.csv 
	cat /home/user2/SenselifeCamSoftware/2022/02/*.CSV |grep "20" >> all_readings.csv 
	cat /home/user2/SenselifeCamSoftware/2022/03/*.CSV |grep "20" >> all_readings.csv 
	cat /home/user2/SenselifeCamSoftware/2022/04/*.CSV |grep "20" >> all_readings.csv 
	cat /home/user2/SenselifeCamSoftware/2022/05/*.CSV |grep "20" >> all_readings.csv 
	cat /home/user2/SenselifeCamSoftware/2022/06/*.CSV |grep "20" >> all_readings.csv 
	cat /home/user2/SenselifeCamSoftware/2022/07/*.CSV |grep "20" >> all_readings.csv 
	cat /home/user2/SenselifeCamSoftware/2022/08/*.CSV |grep "20" >> all_readings.csv 
	cat /home/user2/SenselifeCamSoftware/2022/09/*.CSV |grep "20" >> all_readings.csv 
	cat /home/user2/SenselifeCamSoftware/2022/10/*.CSV |grep "20" >> all_readings.csv 
	cat /home/user2/SenselifeCamSoftware/2022/11/*.CSV |grep "20" >> all_readings.csv 
	cat /home/user2/SenselifeCamSoftware/2022/12/*.CSV |grep "20" >> all_readings.csv 
	# copy stats.json prev_stats.json
	python3 process_csv.py	#python3 because uses list2 = list.copy()
	python tweet.py
	gsutil -h "Cache-Control:public, max-age=0" -m cp outages.csv gs://uk_bn3_co2 | echo $?  
	gsutil -h "Cache-Control:public, max-age=0" -m cp todays_readings.csv gs://uk_bn3_co2 | echo $? 
	gsutil -h "Cache-Control:public, max-age=0" -m cp stats.json gs://uk_bn3_co2 | echo $?
	if [ ! -f "done_daily_copy_flag.txt" ]; then
		if [ $(date +%H) -eq '00' ]; then
		  gsutil -h "Cache-Control:public, max-age=0" cp all_historic_readings.csv gs://uk_bn3_co2 | echo $?
		  gsutil -h "Cache-Control:public, max-age=0" cp all_readings.csv gs://uk_bn3_co2 | echo $?
		  gsutil -h "Cache-Control:public, max-age=0" cp day_befores_readings.csv gs://uk_bn3_co2 | echo $?
		  gsutil -h "Cache-Control:public, max-age=0" cp last_months_readings.csv gs://uk_bn3_co2 | echo $?
		  gsutil -h "Cache-Control:public, max-age=0" cp last_weeks_readings.csv gs://uk_bn3_co2 | echo $?
		  gsutil -h "Cache-Control:public, max-age=0" cp week_before_lasts_readings.csv gs://uk_bn3_co2 | echo $?
		  gsutil -h "Cache-Control:public, max-age=0" cp yesterdays_readings.csv gs://uk_bn3_co2 | echo $?
		  copy flag.txt done_daily_copy_flag.txt
		fi
	fi
	if [ $(date +%H) -eq '01' ]; then
		rm done_daily_copy_flag.txt
		echo "flag file deleted"
	fi
	python3 monitor_sensor_connection.py
	echo $(date +%H:%M:%S)
	# Script take 70s to run on Windows laptop, test again todo
	echo "start timeout"
	sleep 530
done
