# vuploader
this python script uploads voice messages to a discord channel
requires the requests library and python version 3.10
```
usage: voiceUpload.py [-h] [--duration DURATION] [--noisetype NOISETYPE] [--nspec NSPEC] filename channel_id

Python script for uploading a voice message from a file to a Discord channel

positional arguments:
  filename              Filename
  channel_id            The Channel ID

options:
  -h, --help            show this help message and exit
  --duration DURATION   The shown voice message duration. Can be any float between 0 and 2147483647. Defaults to 0
  --noisetype NOISETYPE
                        Determines the waveform displayed in the message. Can be 'random', 'reversecone', 'cone',
                        'silence', 'wall', 'specified'. Defaults to 'cone'.
  --nspec NSPEC         A 256 element long byte array encoded in base64. This will be sent to Discord as waveform data
                        if you specify 'specified' in noisetype, otherwise this is ignored.

Discord Token is taken from USER_TOKEN.txt in pwd
```
