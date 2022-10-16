
<div align="center">
    <img src="images/lvc-icon.png">
    <h2>Linux Voice Control</h2>
</div>

# ![](https://img.icons8.com/external-icongeek26-flat-icongeek26/32/000000/external-Sage-Leaves-recipes-and-ingredients-icongeek26-flat-icongeek26.png) Usage

Well, this voice control system is currently in the basic mode ...

Lets quick finish the setup and tell you how
```shell
git clone https://github.com/omegaui/linux-voice-control
cd linux-voice-control
./install.sh
```

The `install.sh` script will set up your installation of linux-voice-control by installing some dependencies with pip.

The above process will finish off writing `lvc-config.json` and `lvc-commands.json` file to your root (~) and also the sources to `~/lvc-bin`.
That's how the first two lines of `lvc-config.json` look initially ...
```
{
  "name": "alex", # name of your control system
  "record-duration": 3, # duration in which you will speak your command ... simultaneously keeps on listening for every 3s
...
```

Let's take a look at the game controller ... `lvc-commands.json`
```json
{
  "open firefox": "firefox",
  "open editor": "gedit",
  "lock the screen": "xdg-screensaver lock",
  "open whatsapp": "firefox https://web.whatsapp.com",
  "open instagram": "firefox https://instagram.com",
  "write an email": "firefox https://mail.google.com/mail/u/0/#inbox"
}
```

You must be able to infer from above by now, that the keys are your speeches actually and their values are the corresponding commands that are to be executed each time you name those keys.

But wait ... understand how it's actually working in the background.

Let's take an example how it accurately recognizes your commands and your actual speeches.

First if you're really feeling happy to know about this project, then, you must thank [openai's whisper](https://github.com/openai/whisper)
it's actually the root and the stem of this project being a reality.
Want to know why? Just click on the link above.

After getting the audio transcription, a fuzzy match is applied against the keys in the `lvc-commands.json`.

Just like you search something on Google and getting the correct results even after typing the wrong spelling.

Your installation is all set for usage (for forking too 😉).
Just hit `linux-voice-control` in the terminal.

**Life Saver Tip: Add `linux-voice-control` to your startup scripts** 

**Future Ideas**: Adding Dynamic Voice Control like _hey alex ... call spiderman_ (you already know things like that) and most important things [discussions](https://github.com/omegaui/linux-voice-control/discussions)

# ![](https://img.icons8.com/fluency/32/000000/sourcetree.png) Build from source

Super simple things you know ... 
```shell
git clone https://github.com/omegaui/linux-voice-control
cd linux-voice-control
pip install -r requirements.txt
python3 main.py
```

# ![](https://img.icons8.com/color/32/000000/approval--v1.png) Ok Tested!
The project is finely tested on fedora 36 Workstation ...
Here's the neofetch ...
![img.png](images/img.png)
