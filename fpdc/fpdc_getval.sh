#!/bin/bash

cd `dirname $0`
source fpdc_config.conf

if [ -z $1 ]; then
    echo "$0 - Get current stored value of FPDC"
    echo "Usage: $0 [TMP|ILL|HUM|PWR]"
    exit
fi

if [ ! -e "$CURRENT_VALUES_FILE" ]; then
    exit 1
fi




source "$CURRENT_VALUES_FILE"
echo ${!1}
exit 0

