#!/bin/sh

echo "pip installing requirements.txt ..."
pip install -r requirements.txt
echo "Settings up Linux-Voice-Control (lvc) ..."
mkdir ~/lvc-bin
echo "Copying sources and icon to ~/lvc-bin ..."
cp main.py ~/lvc-bin
cp command_manager.py ~/lvc-bin
cp config_manager.py ~/lvc-bin
cp __init__.py ~/lvc-bin
cp notifier.py ~/lvc-bin
cp voice_feedback.py ~/lvc-bin
cp utils.py ~/lvc-bin
cp live_mode_manager.py ~/lvc-bin
cp live_mode_setup.py ~/lvc-bin
cp master_mode_manager.py ~/lvc-bin
cp master_control_mode_setup.py ~/lvc-bin
cp images/lvc-icon.png ~/lvc-bin
echo "Copying launcher(linux-voice-control) to /usr/bin (requires root access) ..."
sudo cp linux-voice-control /usr/bin
sudo chmod 777 /usr/bin/linux-voice-control
echo "Copying default commands and config to ~ ..."
cp lvc-commands.json ~
cp lvc-config.json ~
echo "All Set"
echo "That's how your lvc-config.json looks right now ..."
cat ~/lvc-config.json
echo
echo "And these are some raw commands ..."
cat ~/lvc-commands.json
echo
echo "Attach the program to your startup for an always ready assist."
echo
echo "Execute linux-voice-control now to start it here!"

