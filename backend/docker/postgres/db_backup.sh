#!/bin/bash

source /var/www/db_backup.config

if [ -z "$SSH_USER" ] || [ -z "$SSH_PORT" ] || [ -z "$SSH_HOST" ] || [ -z "$DB_NAME" ] || [ -z "$DB_USER" ] || [ -z "$DB_PASS" ] || [ -z "$SSH_FILES_PATH" ] || [ -z "$SSH_KEY" ]; then
    echo "Insufficient parameters";
    exit 0;
fi

view_help()
{
cat << _EOF_
____________________________________

-b, --backup  :make backup now
-r, --run-sched  :run backup scheduler
-s, --stop-sched  :stop backup scheduler
____________________________________
_EOF_
}

make_backup()
{
    DUMP_FILENAME=dump_$DB_NAME_`date +%d-%m-%Y"_"%H_%M_%S`.sql.gz

    PGPASSWORD="$DB_PASS" pg_dump --exclude-table-data=alembic_version --column-inserts --data-only --dbname=postgresql://$DB_USER@postgres:5432/$DB_NAME > /tmp/flask/$DUMP_FILENAME

#    rsync -p -t -r -e "ssh -p $SSH_PORT -i $SSH_KEY" --log-file=$LOGS_PATH/rsync.log /tmp/$DUMP_FILENAME $SSH_USER@$SSH_HOST:$SSH_FILES_PATH/sqls/

#    rm /tmp/$DUMP_FILENAME
}

run_scheduler()
{
    crontab /etc/cron_schedule
    service cron start
}

stop_scheduler()
{
    service cron stop
}

case $1 in
    -b | --backup ) 	make_backup
		                ;;
    -r | --run-sched )  run_scheduler
                        ;;
    -s | --stop-sched ) stop_scheduler
                        ;;
    * )                 view_help
esac
