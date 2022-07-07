# audiotovideo
GUI to create video files from a folder of audio files.


## Requirements
Recommended: Pycharm Community Edition (Free): https://www.jetbrains.com/pycharm/download/

Before using, please install ffmpeg using homebrew using instruction below:

* Open Terminal
* Install Xcode: xcode-select --install
* Install Homebrew: /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
* Install ffmpeg: brew install ffmpeg
* Install Python: brew install python
* Install Python libs: pip3 install requests moviepy PyQt5 pillow

Also, you will need API access to Unsplash: https://unsplash.com/developers
* Once you have API access, create a file called user_settings.py in the same directory as the gui.py file.
* It should set a variable called unsplash_client_id = "value of your client id"
* This is not applicable if you are using a compiled version.
