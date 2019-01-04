#!/usr/bin/env bash

if [[ "$(id -u)" != "0" ]]; then
   echo "Make sure to run this with sudo or as root, or it won't work!"
   exit 1
fi

hash python3 2>/dev/null

if [[ $? -ne 0 ]]; then
    echo "Make sure python 3 is installed and set to python3!"
    exit 1
fi

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

python3 -m pip install -r ${DIR}/requirements.txt
cp $DIR/nbt2json.py /usr/bin/nbt2json
chmod +x /usr/bin/nbt2json

echo "----------------------"
echo
echo "NBT2JSON installed, use /usr/bin/nbt2json to run."
