#!/usr/bin/env bash

set -e

pushd frontend
    echo "Updating JavaScript dependencies"
    npm install
    echo "Starting development web server"
    npm run serve
popd
