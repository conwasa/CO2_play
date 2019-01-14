:start
type C:\user\SenselifeCamSoftware\2018\11\*.csv |find "20" > all_readings.csv |find "20"
type C:\user\SenselifeCamSoftware\2018\12\*.csv |find "20" >> all_readings.csv |find "20"
type C:\user\SenselifeCamSoftware\2019\01\*.csv |find "20" >> all_readings.csv |find "20"
type C:\user\SenselifeCamSoftware\2019\02\*.csv |find "20" >> all_readings.csv |find "20"
type C:\user\SenselifeCamSoftware\2019\03\*.csv |find "20" >> all_readings.csv |find "20"
type C:\user\SenselifeCamSoftware\2019\04\*.csv |find "20" >> all_readings.csv |find "20"
type C:\user\SenselifeCamSoftware\2019\05\*.csv |find "20" >> all_readings.csv |find "20"
type C:\user\SenselifeCamSoftware\2019\06\*.csv |find "20" >> all_readings.csv |find "20"
type C:\user\SenselifeCamSoftware\2019\07\*.csv |find "20" >> all_readings.csv |find "20"
type C:\user\SenselifeCamSoftware\2019\08\*.csv |find "20" >> all_readings.csv |find "20"
type C:\user\SenselifeCamSoftware\2019\09\*.csv |find "20" >> all_readings.csv |find "20"
type C:\user\SenselifeCamSoftware\2019\10\*.csv |find "20" >> all_readings.csv |find "20"
type C:\user\SenselifeCamSoftware\2019\11\*.csv |find "20" >> all_readings.csv |find "20"
type C:\user\SenselifeCamSoftware\2019\12\*.csv |find "20" >> all_readings.csv |find "20"

copy stats.json prev_stats.json
python process_csv.py
python tweet.py

gsutil -m cp outages.csv gs://uk_bn3_co2 | echo Exit Code is %errorlevel%
gsutil -m cp todays_readings.csv gs://uk_bn3_co2 | echo Exit Code is %errorlevel%
gsutil -m cp stats.json gs://uk_bn3_co2 | echo Exit Code is %errorlevel%

set hour=%time:~0,2%

IF NOT EXIST done_daily_copy_flag.txt (
IF "%hour%" == "00" (
echo "copy all files"
gsutil cp all_historic_readings.csv gs://uk_bn3_co2 | echo Exit Code is %errorlevel%
gsutil cp all_readings.csv gs://uk_bn3_co2 | echo Exit Code is %errorlevel%
gsutil cp day_befores_readings.csv gs://uk_bn3_co2 | echo Exit Code is %errorlevel%
gsutil cp last_months_readings.csv gs://uk_bn3_co2 | echo Exit Code is %errorlevel%
gsutil cp last_weeks_readings.csv gs://uk_bn3_co2 | echo Exit Code is %errorlevel%
gsutil cp week_before_lasts_readings.csv gs://uk_bn3_co2 | echo Exit Code is %errorlevel%
gsutil cp yesterdays_readings.csv gs://uk_bn3_co2 | echo Exit Code is %errorlevel%
copy flag.txt done_daily_copy_flag.txt
))

IF "%hour%" == "01" (
del done_daily_copy_flag.txt
echo "flag file deleted"
)
echo %time%
rem Script take 70s to run
echo "start timeout"
timeout 530
goto start