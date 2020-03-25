#!/bin/sh
### BEGIN INIT INFO
# Provides:          rpc-server
# Required-Start:    mountkernfs
# Required-Stop:
# X-Start-Before:    checkroot
# Default-Start:     S
# Default-Stop:
# X-Interactive:     true
# Short-Description: rpc
# Description:       Onlye
### END INIT INFO

# 0         program is running or service is OK
# 1         program is dead and /var/run pid file exists
# 2         program is dead and /var/lock lock file exists
# 3         program is not running
# 4         program or service status is unknown

USER=pi
PIDFILE=/var/run/rpcserver.pid
EXEC=/usr/bin/python3
SCRIPT=/home/pi/workspace/gopygo/server.py
LOGS=/var/log/rpcserver.log

if [ -f "${SCRIPT}" ]; then
  case "$1" in
    status)
      if [ -f "${PIDFILE}" ]; then
        PID=`cat $PIDFILE`
        if ps -p $PID > /dev/null; then
          TIME=$(ps -o etime= -p $PID)
          echo "Running for $TIME"
        else
          echo "Server is not running, check logs at $LOGS"
        fi
      else
        echo "Start server first to check the status"
      fi
      ;;
    stop)
      echo "Stopping a server..."
      start-stop-daemon --stop --pidfile $PIDFILE --remove-pidfile
      # RETVAL="$?"
      # [ "$RETVAL" = 2 ] && return 2
      ;;
    restart)
      echo "Restarting a server"
      ;;
    start)
      echo "Starting a server..."
      start-stop-daemon --start --chuid $USER --background \
        --make-pidfile --pidfile $PIDFILE \
        --startas /bin/bash -- -c "exec $EXEC $SCRIPT > $LOGS 2>&1"
      ;;
    *)
      echo 'Usage: /etc/init.d/rpc-server {start|restart|stop|status}'
      exit 3
      ;;
  esac
else
  echo 'Install gopygo application first' >&2
  exit 3
fi
