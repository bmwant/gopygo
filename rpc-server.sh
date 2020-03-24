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

PIDFILE=/var/run/rpcserver.pid
PROG=/home/pi/workspace/gopygo/server.py

if [ -f "${PROG}" ]; then
  case "$1" in
    status)
      ;;
    stop)
      echo "Stopping a server..."
      start-stop-daemon --stop --pid $PIDFILE
      # RETVAL="$?"
	# [ "$RETVAL" = 2 ] && return 2
      ;;
    restart)
      echo "Restarting a server"
      ;;
    start)
      echo "Starting a server..."
      start-stop-daemon --start --chuid pi --background \
        --make-pidfile --pidfile $PIDFILE \
        --exec /usr/bin/python3 $PROG
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
