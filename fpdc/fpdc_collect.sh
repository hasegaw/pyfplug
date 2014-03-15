#!/bin/bash

# Usage example:
# crontab:
#   * * * * *   /path/to/fpdc/fpdc_collect.sh

cd `dirname $0`
source fpdc_config.conf

function get_current_values {

    CURFN="$CURRENT_VALUES_FILE"

    IFS=" "
    VALUES="`$FCTL get tmp ill hum pwr`"
    set -- $VALUES
    echo "
TMP=$1
ILL=$2
HUM=$3
PWR=$4
" > "$CURFN"
}


function get_acc_values {
    LOGFN_DATE=`date "+%Y-%m"`
    LOGFN="${LOG_FILE/<MONTH>/$LOGFN_DATE}"
    LOGDATE=`date +%d,%H,%H:%M:%S`
    
    DATA=`$FCTL get acc`
    DATA="${DATA// /,}"
    LINE="$LOGDATE,$DATA"
    echo "$LINE" >> "$LOGFN"
}


CUR_HOUR="n"

while true; do
    NOW_HOUR=`date +%Y%m%d%H`
    if [ x$NOW_HOUR != x$CUR_HOUR ]; then
        CUR_HOUR=$NOW_HOUR
        if [ s$LOG_ENABLED != "s0" ]; then
            get_acc_values
        fi
    fi
    get_current_values
    sleep 4
done


