#!/bin/bash

check_root() {
  if [[ $EUID -ne 0 ]]; then
    echo "This script requires root privileges to install system packages."
    echo "Please run it with sudo: sudo bash $0 $*"
    exit 1
  fi
}

check_root 
echo "Starting Setup Script"
apt update
apt upgrade
apt install python3-pip python3-dev patchelf
pip install nuitka

if [[ $? -eq 0 ]]; then
  echo "Nuitka and its basic requirements are now installed."
  echo "For more advanced usage or specific features, you might need to install additional packages."
  echo "Refer to the Nuitka documentation for details: https://nuitka.net/pages/overview.html"
else
  echo "Failed To Install Nuitka!"
  exit 1
fi

echo "Compling simplestRPG now.."
mkdir build
cd build
nuitka ../src/main.py --onefile --follow-imports -o simplestRPG

if [[ $? -eq 0 ]]; then
  cd ..
  echo "Compiled simplestRPG succesfully."
else
    echo "Failed to compile simplestRPG!"
  exit 1
fi