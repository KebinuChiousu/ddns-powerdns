#!/bin/bash
if [ -e ddns.pid ]
then
  echo "stopping: ddns..."
  kill `cat ddns.pid`
  rm ddns.pid
else
  echo "ddns is not running."
fi
