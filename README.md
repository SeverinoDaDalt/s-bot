# S-BOT manual
## How to install

Follow the steps that proceed:
- `git clone` the repository
- Install `ffmpeg` in your device
- Create a python virtual environment and `pip install` the following packages:
  - `discord`
  - `yt_dlp`
- Change the `config.json` parameter called `token` with the desired one (in previous versions this was stored in the `token.txt` file)

## How to run
Simply run `python main.py`.

On Discord you can run the following commands:
- `!join`: the bot will join your voice channel.
- `!leave`: the bot will leave the current voice channel.
- `!play <SONG_NAME> <optional: N_REPETITIONS>`: `<SONG_NAME>.mp3` will be played `<N_REPETITIONS>` (if specified, else, default number of times will be used. See config in order to change this default parameter).
- `!download <YT_URL> <NAME>`: downloads `<YT_URL>` from YouTube and saves it as `<NAME>.mp3` in the default music folder (See config in order to change this default parameter).
- `!pause`: pauses music.
- `!resume`: resume music.
- `!stop`: stops music.

## Config parameters
- `command_prefix`: token used to invoke the bot in discord.
- `token`: token of the bot. 
- `music_directory`: folder where music files are stored.
- `default_repetitions`: how many times a song is played if not specified.
