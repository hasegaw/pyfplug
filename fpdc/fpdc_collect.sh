#!/bin/bash

cd `dirname $0`
source fpdc_config.conf
cd ../

./fplugdaemon /var/data/fpdc/ $CURRENT_VALUES_FILE

