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


if [ s$LOG_ENABLED != "s0" ]; then
    MIN=`date +%M`
    if [ $MIN == 00 ]; then
        get_acc_values
    fi
fi

while true; do
    get_current_values
    sleep 4
done


