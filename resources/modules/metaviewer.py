from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3

class MetaViewer:
    def __init__(self, audio_file):
        self.__audio_file = audio_file
        self.__audio = EasyID3(self.__audio_file)
        self.__artist = self.__audio['artist'][0] or 'Unknown Artist'
        self.__title = self.__audio['title'][0] or 'Unknown Title'

    def getArtistAndTitle(self):
        return self.__artist, self.__title

    def getDuration(self):
        duration_seconds = int(MP3(self.__audio_file).info.length)

        minutes = duration_seconds // 60
        seconds = duration_seconds % 60

        return minutes, seconds