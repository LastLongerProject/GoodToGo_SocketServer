#!/bin/bash
until python3 server.py; do
	echo "'server.py' crashed with exit code $?. Restarting..." >&2
	sleep 1
done
