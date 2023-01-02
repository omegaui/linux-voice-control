#!/bin/bash

cd lvc_gui_flutter || exit
flutter build linux

cd ..

cd gui || mkdir gui || exit

rm -rf *

cd ..

echo "Copying the release bundle to repo/gui ..."
cp -r lvc_gui_flutter/build/linux/x64/release/bundle/* gui/

echo "Done!"
