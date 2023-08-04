import os
import subprocess
from resources.modules import metaviewer as MetaViewer


class Player():
    def __init__(self, audio, image):
        self.__audio = audio
        self.__image = image
        self.__meta = MetaViewer.MetaViewer(self.__audio)
        self.__artist, self.__title = self.__meta.getArtistAndTitle()
        self.__minutes, self.__seconds = self.__meta.getDuration()

    def play(self):
        fps = os.environ.get('fps')
        preset = os.environ.get('preset')
        stream_url = os.environ.get('stream_url')
        stream_key = os.environ.get('stream_key')
        width = os.environ.get('video_width')
        height = os.environ.get('video_height')

        ffmpeg_command= (f"ffmpeg\x20"
                         f"-stream_loop -1\x20"
                         f"-f image2\x20"
                         f"-i \"{str(self.__image)}\"\x20"
                         f"-re\x20"
                         f"-i \"{str(self.__audio)}\"\x20"
                         f"-filter_complex \"[0:v]scale='min({width},iw)':'min({height},ih)',pad={width}:{height}:(ow-iw)/2:(oh-ih)/2[v1];[v1]drawtext=text='{self.__artist} - {self.__title}':x=85:y=h - 145:fontsize=60:fontcolor=white:fontfile=\"resources/fonts/Roboto-Regular.ttf\":box=1:boxcolor=black@0.5:boxborderw=30[v2]\" "
                         f"-c:v libx264\x20"
                         f"-preset {preset}\x20"
                         f"-b:v 3500k\x20"
                         f"-maxrate 7000k\x20"
                         f"-bufsize 200k\x20"
                         f"-pix_fmt yuv420p\x20"
                         f"-g {fps}\x20"
                         f"-bf 2\x20"
                         f"-c:a aac\x20"
                         f"-b:a 320k\x20"
                         f"-ac 2\x20"
                         f"-ar 44100\x20"
                         f"-t {self.__minutes}:{self.__seconds + 3}\x20"
                         f"-video_size \"{width}x{height}\"\x20"
                         f"-map \"[v2]\"\x20"
                         f"-map 1:a\x20"
                         f"-f flv {stream_url}{stream_key}")

        subprocess.call(ffmpeg_command, shell=True)