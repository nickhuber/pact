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
    if [[ "$distro" = "Ubuntu" ]] ; then
        handle_ubuntu "${release}"
    elif [[ "$distro" = "Fedora" ]] ; then
        handle_fedora "${release}"
    elif [[ "$distro" = "openSUSE project" ]] ; then
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
    dnf install python3 python3-pip nodejs npm sassc
}


function handle_opensuse() {
    release=$1
    zypper addrepo "https://download.opensuse.org/repositories/devel:/libraries:/c_c++/openSUSE_Leap_${release}/devel:libraries:c_c++.repo"
    zypper install python3 python3-pip nodejs npm sassc
}


function handle_ubuntu() {
    release=$1
    if [[ $(bc <<< "${release} < 14.04") -eq 1 ]] ; then
        echo "Ubuntu ${release} too old, 14.04 is the minimum supported version, but 16.04 or newer is recommended"
    elif [[ $(bc <<< "${release} < 16.04") -eq 1 ]] ; then
        apt-get update
        apt-get install python3 python3-pip nodejs npm sassc
    else
        apt-get update
        apt-get install python3 python3-venv python3-pip nodejs npm sassc
    fi
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
