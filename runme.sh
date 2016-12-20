

while true; do
    echo Starting python script...
    python vigilant-train.py mtsave -j 80 -n 400
    python vigilant-train.py stats 
    echo Cleaning...
    killall python
    echo Sleeping...
    sleep 3600
done
