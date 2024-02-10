#!/bin/sh

echo "pip installing requirements.txt ..."
pip install -r requirements.txt
pip install playwright
playwright install
echo "You need to login into ChatGPT to use chat mode, to do so run <chatgpt install>."
echo "Settings up Linux-Voice-Control (lvc) ..."
mkdir ~/lvc-bin
mkdir ~/lvc-bin/misc
mkdir ~/lvc-bin/gui
echo "Copying sources and icon to ~/lvc-bin ..."
cp main.py ~/lvc-bin
cp command_manager.py ~/lvc-bin
cp config_manager.py ~/lvc-bin
cp __init__.py ~/lvc-bin
cp notifier.py ~/lvc-bin
cp voice_feedback.py ~/lvc-bin
cp utils.py ~/lvc-bin
cp chatgpt_port.py ~/lvc-bin
cp basic_mode_manager.py ~/lvc-bin
cp live_mode_manager.py ~/lvc-bin
cp live_mode_setup.py ~/lvc-bin
cp master_mode_manager.py ~/lvc-bin
cp master_control_mode_setup.py ~/lvc-bin
cp images/lvc-icon.png ~/lvc-bin
cp misc/greeting.mp3 ~/lvc-bin/misc
cp misc/internal-voice-feedback-error.mp3 ~/lvc-bin/misc
cp misc/network-error.mp3 ~/lvc-bin/misc
cp misc/exiting-feedback.mp3 ~/lvc-bin/misc
cp -r gui/* ~/lvc-bin/gui
echo "Copying all launchers to /usr/bin (requires root access) ..."
sudo cp linux-voice-control /usr/bin
sudo cp linux-voice-control-gui /usr/bin
sudo chmod 0755 /usr/bin/linux-voice-control /usr/bin/linux-voice-control-gui ~/lvc-bin/gui/lvc_gui_flutter
echo "Copying default commands and config to ~ ..."
cp lvc-commands.json ~/lvc-bin
cp lvc-config.json ~/lvc-bin
echo "All Set"
echo "That's how your lvc-config.json looks right now ..."
cat ~/lvc-bin/lvc-config.json
echo
echo "And these are some raw commands ..."
cat ~/lvc-bin/lvc-commands.json
echo
echo "Attach linux-voice-control-gui script to your startup for an always ready assist."
echo
echo "Execute linux-voice-control or linux-voice-control-gui now to start it here!"

