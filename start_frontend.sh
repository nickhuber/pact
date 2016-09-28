#!/usr/bin/env bash

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
	./node_modules/.bin/http-server -P http://localhost:8000 app
popd
