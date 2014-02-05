#!/bin/bash

cd `dirname $0`
source fpdc_config.conf


CURFN="$CURRENT_VALUES_FILE"
echo > "$CURFN"

IFS=" "
VALUES="`$FCTL get tmp ill hum pwr`"
set -- $VALUES
echo "
TMP=$1
ILL=$2
HUM=$3
PWR=$4
" > "$CURFN"

if [ -z $LOG_ENABLED ]; then
    exit
fi

if [ $LOG_ENABLED = 0 ]; then
    exit
fi

MONTH=`date +%M`
if [ $MONTH != 00 ]; then
    exit
fi

LOGFN_DATE=`date "+%Y-%m"`
LOGFN="${LOG_FILE/<MONTH>/$LOGFN_DATE}"
LOGDATE=`date +%d,%H,%H:%M:%S`
DATA=`$FCTL get acc 0`
LINE="$LOGDATE,$DATA"

echo "$LINE" >> "$LOGFN"

# for test
DATA=`$FCTL get acc`
LINE="$LOGDATE,$DATA"
echo "$LINE" >> ${LOGFN}.test

