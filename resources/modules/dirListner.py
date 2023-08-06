import os
import glob

class DirListner:
    def __init__(self, dir, type = 'mp3'):
        self.__dir = dir
        self.__mp3_files = glob.glob(os.path.join(self.__dir, f"*.{type}"))

    def getFiles(self):
        self.__mp3_files.sort()
        return self.__mp3_files
