#!/usr/bin/env bash

set -e

running="true"

function cleanup() {
    running="false"
    kill %1
}

pushd frontend
    echo "Updating JavaScript dependencies"
    npm install
    npm update
    echo "Compiling everything together"
    make
    echo "Watching for changes, will recompile if necessary"
    fswatch \
        --one-per-batch \
        --event=Updated \
        --recursive \
        src | xargs --max-args=1 -I{} make &
    echo "Setting up cleanup handler"
    trap cleanup SIGINT SIGTERM
    echo "Installing dev http server"
    npm install http-server
    echo "Starting development web server"
    # Don't quit if this fails, http-server is braindead and dies if a proxy request fails
    set +e
    while true ; do
        ./node_modules/.bin/http-server -P http://localhost:8000 dist -p 8081
        if [ "$running" = "false" ] ; then
            break
        fi
    done
popd
