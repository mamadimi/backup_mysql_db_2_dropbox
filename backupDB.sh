#bin/bash

DATABASE=''
USER=''
PASSWORD=''

#Back up janitor db
BACK_UP_NAME=$(date "+%d-%m-%Y_%H:%M")_$DATABASE_dbBackup.sql

mysqldump -u $USER -p$PASSWORD $DATABASE > $BACK_UP_NAME

python upload2Dropbox.py $BACK_UP_NAME
