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
        self.__vid_min, self.__vid_sec = self.__checkCorrectDuration(self.__minutes, self.__seconds)
        self.__cover = self.__meta.getTrackCover()

    def __checkCorrectDuration(self, __minutes, __seconds):
        __seconds + 3
        if __seconds == 60:
            __seconds = 0
            return __minutes + 1, __seconds
        else:
            return __minutes, __seconds

    def play(self):
        fps = os.environ.get('fps')
        preset = os.environ.get('preset')
        stream_url = os.environ.get('stream_url')
        stream_key = os.environ.get('stream_key')
        width = os.environ.get('video_width')
        height = os.environ.get('video_height')
        title_pos_x = 85
        title_pos_y = 195
        time_pos_x = title_pos_x + 50
        time_pos_y = title_pos_y - 90

        ffmpeg_command= (f"ffmpeg\x20"
                         f"-stream_loop -1\x20"
                         f"-f image2\x20"
                         f"-i \"{str(self.__cover)}\"\x20"
                         f"-re\x20"
                         f"-i \"{str(self.__audio)}\"\x20"
                         f"-filter_complex "
                            f"\"[0:v]scale='min({width},iw)':"
                            f"'min({height},ih)',"
                            f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2[v1];"
                            f"[v1]drawtext="
                                f"text='{self.__artist} - {self.__title}':"
                                f"x={title_pos_x}:y=h - {title_pos_y}:"
                                f"fontsize=60:"
                                f"fontcolor=white:"
                                f"fontfile=\"resources/fonts/Roboto-Regular.ttf\":"
                                f"box=1:"
                                f"boxcolor=black@0.5:"
                                f"boxborderw=30[v2];"
                                f"[v2]drawtext="
                                f"text='{self.__minutes}\:{self.__seconds} | %{{eif\:mod(t/60\,60)\:d\:2}}\:%{{eif\:mod(t\,60)\:d\:2}}':"
                                f"x={time_pos_x}:y=h - {time_pos_y}:"
                                f"fontsize=40:"
                                f"fontcolor=white:"
                                f"fontfile=\"resources/fonts/Roboto-Light.ttf\":"
                                f"box=1:"
                                f"boxcolor=black@0.5:"
                                f"boxborderw=30[v3];\"\x20"
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
                         f"-t {self.__vid_min}:{self.__vid_sec}\x20"
                         f"-video_size \"{width}x{height}\"\x20"
                         f"-map \"[v3]\"\x20"
                         f"-map 1:a\x20"
                         f"-f flv {stream_url}{stream_key}")

        subprocess.call(ffmpeg_command, shell=True)