#!/usr/bin/env bash

# Try and install dev requirements after detecting operating system

os=$(uname)


function handle_macos() {
    which brew
    rc=$?
    if [ $rc -ne 0 ] ; then
        echo "homebrew is required for MacOS"
        exit 1
    fi
    brew update
    brew install python3 node npm ||:
}


function handle_linux() {
    which lsb_release
    rc=$?
    if [ $rc -ne 0 ] ; then
        echo "Ensure lsb_release is available (apt-get install lsb-release, dnf install redhat-lsb-core)"
        exit 1
    fi
    distro=$(lsb_release --short --id)
    release=$(lsb_release --short --release)
    if [ "$distro" = "Ubuntu" ] ; then
        handle_ubuntu $release
    else
        echo "Unsupported distribution $distro."
    fi
}


function handle_ubuntu() {
    release=$1
    if [[ "$release" < "14.03" ]] ; then
        echo "Ubuntu $release too old, 14.04 is the minimum supported version, but 16.04 or newer is recommended"
    elif [[ "$release" < "16.04" ]] ; then
        apt-get update
        apt-get install python3 python3-pip nodejs npm
    else
        apt-get update
        apt-get install python3 python3-venv python3-pip nodejs npm
    fi
}


if [ "$os" = "Darwin" ] ; then
    handle_macos
elif [ "$os" = "Linux" ] ; then
    handle_linux
elif [ "$os" = "FreeBSD" ] ; then
    echo "Automatic setup does not yet support FreeBSD."
    exit 1
fi

echo "All done, run start_backend.sh and start_frontend.sh to get started."
