#! /bin/bash
PATH=/bin:/usr/bin:/sbin:/usr/sbin
VIRTUALENV=/root/.local/share/virtualenvs/Server-WjXv57Cf/bin/activate
GUNICORN=/root/.local/share/virtualenvs/Server-WjXv57Cf/bin/gunicorn
APPMODULE=wsgi:application
DAEMON=gunicornDEBUG
BIND="127.0.0.1:3000"
PIDFILE=/var/run/gunicorn.pid
LOGFILE=/home/nicola/Documenti/Lavoro/UnionService/Server/log/$DAEMON.log
WORKERS=1

        CWD=$PWD
        cd /home/nicola/Documenti/Lavoro/UnionService/Server
        . $VIRTUALENV
        export SECRET_KEY=d23huh2ws
        export PASS_DB=blablableshi
        COMMAND="$GUNICORN --bind=$BIND -k eventlet --workers=$WORKERS --log-level debug --pid=$PIDFILE  Server:application"
        $COMMAND
