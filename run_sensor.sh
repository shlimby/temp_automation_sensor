# Change directory to script dir
path=$( realpath "$0"  ) 
dir=$(dirname "$path")'/'
cd $dir

if test -f "./venv"; then
    venv/bin/python3 run_sensor.py
else 
    python3 run_sensor.py
fi
