# audiotovideo
GUI to create video files from a folder of audio files.

## Finding Most Searched Pronunciations
* https://trends.google.com/trends/explore?q=how%20to%20pronounce&geo=US

## Requirements
Recommended: Pycharm Community Edition (Free): https://www.jetbrains.com/pycharm/download/

Before using, install ffmpeg using homebrew via below instructions:

* Open Terminal
* Install Xcode: xcode-select --install
* Install Homebrew: /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
* Install ffmpeg: brew install ffmpeg
* Install Python: brew install python
* Install Python libs: pip3 install requests moviepy PyQt5 pillow

Also, you will need API access to Unsplash: https://unsplash.com/developers
* Once you have API access, update unsplash_client_id value in user_settings.py file.

