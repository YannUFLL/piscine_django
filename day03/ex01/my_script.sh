#!/bin/bash

pip --version

rm -rf local_lib
mkdir -p local_lib


echo "Installing path.py..."
pip install --target=./local_lib git+https://github.com/jaraco/path.git > install.log 2>&1

if [ $? -eq 0 ]; then
    echo "Installation successful. Running program..."
    PYTHONPATH=./local_lib python3 ./my_program.py
else 
    echo "Installation failed. Check install.log."
fi
