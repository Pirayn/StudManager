APP_DIR="/usr/bin"
APP_BIN="server.py"
APP_ARGS="-250f /var/log/StudManager/error.log"
start-stop-daemon --start --exec "$APP_DIR/$APP_BIN" -- $APP_ARGS