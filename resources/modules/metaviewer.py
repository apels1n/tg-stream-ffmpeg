from mutagen.id3 import ID3, APIC
from mutagen.mp3 import MP3

class MetaViewer:
    def __init__(self, audio_file):
        self.__audio_file = audio_file
        self.__audio = ID3(self.__audio_file)
        self.__artist = self.__audio.get('TPE1').text[0] or 'Unknown Artist'
        self.__title = self.__audio.get('TIT2').text[0] or 'Unknown Title'
        self.__cover = self.__audio.getall('APIC')[0].data

    def getArtistAndTitle(self):
        return self.__artist, self.__title

    def getDuration(self):
        duration_seconds = int(MP3(self.__audio_file).info.length)

        minutes = duration_seconds // 60
        seconds = duration_seconds % 60

        return minutes, seconds

    def getTrackCover(self):
        return self.__cover