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
python process_csv.py
gsutil cp *.csv gs://uk_bn3_co2
gsutil cp *.json gs://uk_bn3_co2
timeout 5

