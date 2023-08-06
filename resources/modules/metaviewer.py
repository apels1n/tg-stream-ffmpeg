from mutagen.id3 import ID3, APIC
from mutagen.mp3 import MP3
import io
from PIL import Image


class MetaViewer:
    def __init__(self, audio_file):
        self.__audio_file = audio_file
        self.__audio = ID3(self.__audio_file)
        self.__artist = self.__audio.get('TPE1').text[0] or 'Unknown Artist'
        self.__title = self.__audio.get('TIT2').text[0] or 'Unknown Title'
        self.__cover = self.__get_cover()

    def getArtistAndTitle(self):
        return self.__artist, self.__title

    def getDuration(self):
        duration_seconds = int(MP3(self.__audio_file).info.length)

        minutes = duration_seconds // 60
        seconds = duration_seconds % 60

        return minutes, seconds

    def getTrackCover(self):
        return self.__cover

    def __get_cover(self):
        for tag in self.__audio.getall('APIC'):
            if isinstance(tag, APIC):
                with open("resources/tmp/tmp_cover.jpg", 'wb') as cover:
                    cover.write(tag.data)

                return "resources/tmp/cover.jpg"
        return "resources/unknown_cover.jpg"