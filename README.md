# Video Audio Swap 

Swap the audio of a music video with another track using beat detection. Download from youtube urls or local files.


usage: run.py [-h] [--audio-youtube AUDIO_YOUTUBE]
              [--video-youtube VIDEO_YOUTUBE] [--audio-file AUDIO_FILE]
              [--video-file VIDEO_FILE] [--clear] [--output OUTPUT]
              [--video-start VIDEO_START] [--video-end VIDEO_END]
              [--audio-start AUDIO_START] [--audio-end AUDIO_END]
              [--samplerate SAMPLERATE] [--win_s WIN_S] [--hop_s HOP_S]
              [--video-samplerate VIDEO_SAMPLERATE]
              [--video-win_s VIDEO_WIN_S] [--video-hop_s VIDEO_HOP_S]

Swap the video and audio of a music video and music track

optional arguments:
  -h, --help            show this help message and exit
  --audio-youtube AUDIO_YOUTUBE
                        The youtube audio url
  --video-youtube VIDEO_YOUTUBE
                        The youtube video url
  --audio-file AUDIO_FILE
                        The location of the audio file
  --video-file VIDEO_FILE
                        The location of the video file
  --clear               Delete all stored temp files from audio and video
                        folders
  --output OUTPUT       The path and name of the output file
  --video-start VIDEO_START
                        Where the music video's audio track starts playing
  --video-end VIDEO_END
                        Where the music video's audio track ends
  --audio-start AUDIO_START
                        Where the audio in the given audio track starts
  --audio-end AUDIO_END
                        Where the audio in the given audio track stops
  --samplerate SAMPLERATE
                        The sample rate of the audio track
  --win_s WIN_S
  --hop_s HOP_S
  --video-samplerate VIDEO_SAMPLERATE
                        The sample rate of the video track's audio
  --video-win_s VIDEO_WIN_S
  --video-hop_s VIDEO_HOP_S

