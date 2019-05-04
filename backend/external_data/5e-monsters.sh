#!/bin/bash

if [ ! -d "5e-bestiary" ]; then
    git clone https://github.com/chisaipete/bestiary 5e-bestiary
else
    pushd 5e-bestiary
    git pull
    popd
fi

../../.venv/bin/python ../pact/manage.py import_5e_bestiary 5e-bestiary/_creatures
