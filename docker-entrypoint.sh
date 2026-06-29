#!/bin/sh
set -eu

install -d -m 0755 -o appuser -g appuser /home/appuser/.tradingagents
install -d -m 0755 -o appuser -g appuser /home/appuser/app/reports
chown -R appuser:appuser /home/appuser/.tradingagents /home/appuser/app/reports

case "${1:-}" in
    -*)
        set -- tradingagents "$@"
        ;;
esac

exec runuser -u appuser -- "$@"
