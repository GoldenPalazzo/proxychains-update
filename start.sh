#!/bin/sh
set -ue
echo "Running main.py..."
./main.py
echo "Modifying proxychains config"
sudo mv *.conf /etc/proxychains4.conf
echo "All done. Enjoy your anonymity."
