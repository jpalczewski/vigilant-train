

while true; do
    echo Starting python script...
    python vigilant-train.py mtsave -j 80 -n 400
    echo Cleaning...
    killall python
    echo Sleeping...
    sleep 3600
done
