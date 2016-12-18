#!/usr/bin/env bash

set -e

function cleanup() {
	kill %1
}

pushd frontend
	echo "Updating JavaScript dependencies"
	npm install
	npm update
	./node_modules/.bin/bower install
	echo "Compiling everything together"
	npm run grunt
	npm run grunt -- watch > /dev/null 2> /dev/null &
	trap cleanup SIGINT SIGTERM
	npm install http-server
	echo "Starting development web server"
	# Don't quit if this fails, http-server is braindead and dies if a proxy request fails
	set +e
	while true ; do
		./node_modules/.bin/http-server -P http://localhost:8000 app -p 8081
	done
popd
