#!/usr/bin/env bash

sum_cmd=$(which md5)
if [ $? -eq 0 ]  ; then
    md5 -q $1
else
    md5sum $1 | awk '{print $1}'
fi