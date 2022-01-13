# get this directory
path=$( realpath "$0"  ) 
dir=$(dirname "$path")'/'

#write out current crontab
crontab -l > mycron
#echo new cron into cron file
echo "# added by temp automation sensor" >> mycron
echo "* * * * * "$dir"run_sensor.sh" >> mycron
#install new cron file
crontab mycron
rm mycron
