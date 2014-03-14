#!/bin/bash

cd `dirname $0`

PIDFILE=fpdc.pid

if [ -e $PIDFILE ]; then
    kill `cat $PIDFILE`
    rm -rf $PIDFILE
    sleep 5
fi

./fpdc_collect.sh &
PID=$!

echo "$PID" > $PIDFILE



