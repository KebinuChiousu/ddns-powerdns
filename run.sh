#!/bin/bash
gunicorn ddns:app > ddns.log 2>&1 & disown
ps -ef | grep "gunicorn ddns:app" | grep -v grep | awk '{print $2}' > ddns.pid
