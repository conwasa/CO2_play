wine /home/user2/SenselifeCamSoftware/CO2_Monitor.exe &
while [ true ]; do
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
	# copy stats.json prev_stats.json
	python3 process_csv.py	#python3 because uses list2 = list.copy()
	python tweet.py
	gsutil -m cp outages.csv gs://uk_bn3_co2 | echo $?  
	gsutil -m cp todays_readings.csv gs://uk_bn3_co2 | echo $? 
	gsutil -m cp stats.json gs://uk_bn3_co2 | echo $?
	if [ ! -f "done_daily_copy_flag.txt" ]; then
		if [ $(date +%H) -eq '00' ]; then
		  gsutil cp all_historic_readings.csv gs://uk_bn3_co2 | echo $?
		  gsutil cp all_readings.csv gs://uk_bn3_co2 | echo $?
		  gsutil cp day_befores_readings.csv gs://uk_bn3_co2 | echo $?
		  gsutil cp last_months_readings.csv gs://uk_bn3_co2 | echo $?
		  gsutil cp last_weeks_readings.csv gs://uk_bn3_co2 | echo $?
		  gsutil cp week_before_lasts_readings.csv gs://uk_bn3_co2 | echo $?
		  gsutil cp yesterdays_readings.csv gs://uk_bn3_co2 | echo $?
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
