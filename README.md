
<div align="center" style="margin: 20px;">
    <a href="https://codeclimate.com/github/omegaui/linux-voice-control/maintainability"><img src="https://api.codeclimate.com/v1/badges/6619e8fe493be62c377e/maintainability" /></a>
    <img src="https://img.shields.io/github/license/omegaui/linux-voice-control" />
    <br>
    <a href="https://www.youtube.com/watch?v=oTfOO_Gz1_s"><strong>Watch the CLI version in action on youtube</strong></a>
</div>

<div align="center">
    <img src="images/lvc-icon.png">
    <h2>Linux Voice Control</h2>
</div>


<div align="center"><h3><strong>See it in action</strong></h3></div>

[Latest Preview (No-Audio)](https://user-images.githubusercontent.com/73544069/215714637-5138a941-99e4-4bba-8d90-27cf2da86b71.webm)

<div align="center">
    <img src="https://img.icons8.com/external-flaticons-flat-flat-icons/64/000000/external-lights-lighting-flaticons-flat-flat-icons-6.png">
    <img src="https://img.icons8.com/emoji/64/000000/film-projector-emoji.png">
    <img src="https://img.icons8.com/external-flaticons-flat-flat-icons/64/000000/external-action-gaming-ecommerce-flaticons-flat-flat-icons-2.png">
</div>
<div align="center" style="padding: 30px;">
  <div align="center" style="background: rgb(120, 20, 10, 0.1); border-radius: 60px; width: 150px; height: 100px;">
    <a href="https://youtu.be/oTfOO_Gz1_s">
      <img src="https://img.icons8.com/fluency/96/null/youtube-play.png"/>
    </a>
    <p><strong>See YouTube Video</strong></p>
  </div>
</div>

# ![](https://img.icons8.com/color/48/null/metallic-paint.png) Features
- [x] [**ChatGPT Mode**](https://github.com/omegaui/linux-voice-control/issues/8) (just say **activate chat mode**)
- [x] GUI Mode (using Flutter)
- [x] Master Control Mode (yeah, it's your Jarvis Now)
- [x] Voice Feedback 
- [x] Desktop Notifications
- [x] Simplest Command Execution Logic (use your own words and map them to a command in **lvc-commands.json**)
- [x] Accurate Master Voice Matching using **[speechbrain](https://speechbrain.github.io/#)**
- [x] Automated Setup!
- [x] Customization
  - [x] Change Your Control System Name
  - [x] Voice Feedback Speech Control
  - [x] Voice Feedback Speed Control
  - [x] Total Execution Control through configuration
- [ ] **[Live Mode](https://github.com/omegaui/linux-voice-control/issues/3)** (under development, until, the system listens every **x seconds**, where **x** is the **record-duration** property in **lvc-config.json**)
- [ ] **[Dynamic Mode](https://github.com/omegaui/linux-voice-control/issues/5)**

**Pro-Tip**: _Say '**See you later**' to it turn off._

**Pro-Tip**: _Say '**Activate master control mode**' to turn on master control mode without manual config._

**Pro-Tip**: _Say '**Deactivate master control mode**' to turn off master control mode without manual config._

**_Yes, these are the built-in actions!_**

<div align="center">
  <img src="https://img.icons8.com/external-flaticons-flat-flat-icons/320/null/external-master-martial-arts-flaticons-flat-flat-icons.png"/>
  <h1>Master Control Mode</h1>
</div>

Ok! ;) 

Let's just see how to set up master control mode:

After installing,
run the **master_control_mode_setup.py** script
```shell
python3 master_control_mode_setup.py
```

You will be asked to speak three times given only 3 seconds each time.
Speak as much as you can but in your normal tone!
After Saving the training-data, this program exists **without** actually enabling master control mode.

For enabling master control mode, you need to set this property in **lvc-config.json** to **true**
OR
Even you can just say **activate master control mode** during the runtime to enable it dynamically for that session only 😉!
```json
{
  "master-mode": true
}
```

# ![](https://img.icons8.com/external-icongeek26-flat-icongeek26/32/000000/external-Sage-Leaves-recipes-and-ingredients-icongeek26-flat-icongeek26.png) Usage / Install

Lets quick finish the setup
```shell
git clone https://github.com/omegaui/linux-voice-control
cd linux-voice-control
./install.sh
```

The `install.sh` script will set up your installation of linux-voice-control by installing some dependencies with pip.

The above process will finish off writing `lvc-config.json` and `lvc-commands.json` file to your root (~) and also the sources to `~/lvc-bin`.
That's how your `lvc-config.json` look initially ...
```json
{
  "name": "alex",
  "greeting": "Greetings!",
  "record-duration": 3,
  "channels": 2,
  "rate": 44100,
  "chunk-size": 1024,
  "notifications-enabled": false,
  "show-commands-on-startup": true,
  "logs": true,
  "speech-threshold": 2500,
  "live-mode": false,
  "use-hot-word-in-basic-mode": false,
  "hot-words": [
    "hey alex",
    "here alex",
    "listen alex"
  ],
  "master-mode": false,
  "master-mode-barrier-speech-enabled": true,
  "master-mode-barrier-speech": "Unauthorized",
  "voice-pitch": 1.0,
  "voice-feedback-enabled": true,
  "voice-transcription-feedback-enabled": false,
  "voice-feedback-speed": 1.35,
  "voice-cache-enabled": true,
  "voice-feedback-default-speeches": [],
  "voice-feedback-transcription-capable-speeches": [
    "transcribing...",
    "getting it..."
  ],
  "voice-feedback-turning-off": "Turning off linux voice control!"
}
```
<div align="center"><strong>lvc-config.json</strong></div>

Let's take a look at the game controller ... `lvc-commands.json`
here, blocking property means that whether the feedback must go on simultaneously with command execution (if set to false) 
or it should first complete the voice feedback then execute the command (if set to true).

```json
{
  "open firefox": {
    "exec": "firefox",
    "feedback": "starting firefox",
    "blocking": true
  },
  "open editor": {
    "exec": "gedit",
    "feedback": "launching editor",
    "blocking": true
  },
  "lock the screen": {
    "exec": "xdg-screensaver lock",
    "feedback": "locked",
    "blocking": false
  },
  "open whatsapp": {
    "exec": "firefox https://web.whatsapp.com",
    "feedback": "opening whatsapp",
    "blocking": true
  },
  "open instagram": {
    "exec": "firefox https://instagram.com",
    "feedback": "opening instagram",
    "blocking": true
  },
  "write an email": {
    "exec": "firefox https://mail.google.com/mail/u/0/#inbox",
    "feedback": "opening G Mail",
    "blocking": true
  }
}
```
<div align="center"><strong>lvc-commands.json</strong></div> 

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

**Life Saver Tip: _Add `linux-voice-control-gui` to your startup scripts_**

**Future Ideas**: Adding Dynamic Voice Control like _hey alex ... call Spider-Man_ (you already know things like that) and most important things [discussions](https://github.com/omegaui/linux-voice-control/discussions)

# ![](https://img.icons8.com/fluency/32/000000/sourcetree.png) Build from source

Super simple things you know ...
```shell
git clone https://github.com/omegaui/linux-voice-control
cd linux-voice-control
pip install -r requirements.txt
python3 main.py
```

If you are unable to build pyaudio,
see this [post](https://medium.com/@niveditha.itengineer/learn-how-to-setup-portaudio-and-pyaudio-in-ubuntu-to-play-with-speech-recognition-8d2fff660e94).

If you are encountering errors with MPV:
- this means `libmpv` is not installed on your system, for ubuntu you can do that with **sudo apt-get install libmpv-dev**
- For other distros, search online for corresponding package.

If you are encountering warnings with ALSA saying **unable to open slave** or **Unknown {device}**:
- Open up `/usr/share/alsa/alsa.conf`
- Comment out all the lines with cards.pcm.{device}
- Also, Comment out all the lines with pcm.surround{X} things.
Example:
```shell
# redirect to load-on-demand extended pcm definitions
pcm.cards cards.pcm

pcm.default cards.pcm.default
pcm.sysdefault cards.pcm.default
pcm.front cards.pcm.front
# pcm.rear cards.pcm.rear
# pcm.center_lfe cards.pcm.center_lfe
# pcm.side cards.pcm.side
# pcm.surround21 cards.pcm.surround21
# pcm.surround40 cards.pcm.surround40
# pcm.surround41 cards.pcm.surround41
# pcm.surround50 cards.pcm.surround50
# pcm.surround51 cards.pcm.surround51
# pcm.surround71 cards.pcm.surround71
pcm.iec958 cards.pcm.iec958
pcm.spdif iec958
pcm.hdmi cards.pcm.hdmi
pcm.dmix cards.pcm.dmix
pcm.dsnoop cards.pcm.dsnoop
pcm.modem cards.pcm.modem
pcm.phoneline cards.pcm.phoneline
```

Then, everything would work fine.

# ![](https://img.icons8.com/color/32/000000/approval--v1.png) Ok Tested!
![img.png](images/img.png)
<div align="center">
    <em>
        The project is finely tested on <strong>fedora 36 Workstation & Ubuntu 22.04</strong>
    </em>
</div>

# ![](https://img.icons8.com/external-flat-geotatah/32/000000/external-expand-startups-flat-flat-geotatah.png) Extending Usage


The values in `lvc-commands.json` seem just like single commands running when matching key is triggered.

But wait ... it doesn't ends here.

You can even do more with this, i.e. you can write a shell script or any other program, that can be used to
perform some other complex task.

### Example
```json
{
  "its time to rock": {
    "exec": "/usr/bin/setup-spotify-chill-mode"
  }
}
```
<div align="center">A new entry in <strong>lvc-commands.json</strong></div> 


```bash
#!/bin/bash
echo "Listen I don't know actually how to do this ... but I think you got what I mean ..."
# some code here that launches spotify and starts playing that playlist
```
<div align="center"><strong>setup-spotify-chill-mode.sh</strong></div>
<div align="center">
  <img src="https://img.icons8.com/color/240/null/two-hearts.png"/>
  <a href="https://github.com/omegaui"><h1>🐧 Happy Hacking 🐧</h1></a>
</div>
