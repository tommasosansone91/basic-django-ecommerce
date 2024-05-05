# Start the app manually in background via gunicorn (and gracefully exit the machine)

> [!NOTE]
> This is just a temporary command and should be launched only to check that guincorn can run the app successfully.
> The starting, stopping and starting-at-boot of the app should be managed via systemd and the systemctl syntax, which should be implemented as last step of the app installation rpocess.

    current_dir=$pwd

Lancia manualmente copiando lo script e incollandolo nella shell comando per comando, o non funziona.

    cd /var/www/piste_ciclabili_fantastiche/
    source venv/bin/activate

    sudo nohup env PYTHONPATH=`pwd`/.. venv/bin/gunicorn piste_ciclabili_fantastiche.wsgi:application --bind localhost:8001 > /home/pi/piste_ciclabili_fantastiche.log 2>&1 &


    cd $current_dir

### check that the app is up and running

    echo "Grepping the app name from ps aux"
    echo "$(ps aux | grep 'piste_ciclabili_fantastiche')"

### exit gracefully

    ctrl + D

> [!IMPORTANT]
> Do not use the X button of the UI of the terminal.


