#!/usr/bin/env bash

# Try and install dev requirements after detecting operating system

os=$(uname)


function handle_macos() {
    which brew
    rc=$?
    if [[ ${rc} -ne 0 ]] ; then
        echo "homebrew is required for MacOS"
        exit 1
    fi
    brew update
    brew install python3 node npm sassc ||:
    brew link python3 node npm sassc ||:
}


function handle_linux() {
    which lsb_release > /dev/null
    rc=$?
    if [[ ${rc} -ne 0 ]] ; then
        echo "Ensure lsb_release is available (apt-get install lsb-release, dnf install redhat-lsb-core)"
        exit 1
    fi
    distro=$(lsb_release --short --id)
    release=$(lsb_release --short --release)
    if [[ "$distro" = "Fedora" ]] ; then
        handle_fedora "${release}"
    elif [[ "$distro" = "openSUSE" ]] ; then
        handle_opensuse "${release}"
    else
        echo "Unsupported distribution $distro."
    fi
}


function handle_fedora() {
    release=$1
    if [[ "${release}" -lt "25" ]] ; then
        echo "Fedora ${release} is untested, attempting anyways"
    fi
    dnf install python3 python3-pip nodejs npm sassc postgresql-server postgresql-contrib
}


function handle_opensuse() {
    zypper install python3 python3-pip nodejs npm sassc postgresql-server postgresql-contrib
}


if [[ "${os}" = "Darwin" ]] ; then
    handle_macos
elif [[ "${os}" = "Linux" ]] ; then
    handle_linux
elif [[ "${os}" = "FreeBSD" ]] ; then
    echo "Automatic setup does not yet support FreeBSD."
    exit 1
fi

echo "All done, run start_backend.sh and start_frontend.sh to get started."
