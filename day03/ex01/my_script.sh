#!/bin/bash

pip --version
mkdir -p local_lib
if [ -d "./local_lib/path" ]; then
    echo "Removing existing path"
    rm -rf ./local_lib/path
fi


echo "Installing path.py..."
git clone https://github.com/jaraco/path.git ./local_lib/path > install.log 2>&1

if [ $? -eq 0 ]; then
    echo "Installation successful."
    PYTHONPATH=./local_lib/path python3 ./my_program.py
else 
    echo "Installation failed. Check install.log."
fi
