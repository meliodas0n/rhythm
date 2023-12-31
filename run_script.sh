#!/usr/bin/bash

sudo apt-get update && sudo apt full-upgrade -y
sudo apt-get install python3-tk libportaudio2 libasound-dev ffmpeg
python3 -m venv .venv
source ./.venv/bin/activate
pip install -r requirements.txt
