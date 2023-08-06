import os
import asyncio
from resources.modules import dirListner as dlist
from resources.modules import player as pl


async def updateFileList():
    global flist
    flist = dlist.DirListner("music").getFiles()
    await asyncio.sleep(3)


async def playStream():
    while True:
        try:
            for file in flist:
                player = pl.Player(file, os.environ.get('overlay_image'))
                player.play()
                await updateFileList()
        except Exception as e:
            print(e)


async def main():
    await asyncio.gather(updateFileList())
    await asyncio.gather(playStream())

if __name__ == "__main__":
    asyncio.run(main())
