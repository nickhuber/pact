#!/usr/bin/env bash

hash md5 2> /dev/null
if [ $? -eq 0 ]  ; then
    md5 -q $1
else
    md5sum $1 | awk '{print $1}'
fi