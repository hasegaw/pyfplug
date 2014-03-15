#!/bin/bash

cd `dirname $0`

FPDC_DIR=`pwd`
SSD=/sbin/start-stop-daemon

if [ -z $1 ]; then
    echo "usage: $0 [start|stop]"
    exit
fi

MODE=$1

if [ $MODE = 'stop' ]; then
    echo "stop"
    $SSD -p $FPDC_DIR/fpdc.pid --stop
    rm -rf $FPDC_DIR/fpdc.pid
elif [ $MODE = 'start' -o $MODE = 'restart' ]; then
    echo "restart"
    $SSD -p $FPDC_DIR/fpdc.pid --start --background --make-pidfile -x $FPDC_DIR/fpdc_collect.sh
fi


