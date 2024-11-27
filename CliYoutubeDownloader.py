import pytube
import sys
import os
import redis


class YouTubeDownloader:
    def __init__(self):
        self.url = str(input("Enter the URL of the video: "))
        self.youtube = pytube.YouTube(
            self.url, on_progress_callback=YouTubeDownloader.onProgress
        )
        self.redis_client = redis.StrictRedis(host=os.getenv('REDIS_HOST', 'localhost'), port=6379, db=0)
        self.showTitle()

    def showTitle(self):
        print(f"title: {self.youtube.title}\n")
        self.showStreams()

    def showStreams(self):
        self.streamNo = 1
        for stream in self.youtube.streams:
            print(
                f"{self.streamNo} => resolution: {stream.resolution}/fps: {stream.fps}/type: {stream.type}"
            )
            self.streamNo += 1
        self.chooseStream()

    def chooseStream(self):
        self.choose = int(input("Please select one: "))
        self.validateChooseValue()

    def validateChooseValue(self):
        if self.choose in range(1, self.streamNo):
            self.getStream()
        else:
            print("Please enter a correct option from the list.")
            self.chooseStream()

    def getStream(self):
        self.stream = self.youtube.streams[self.choose - 1]
        self.getFileSize()

    def getFileSize(self):
        global file_size
        file_size = self.stream.filesize / 1000000
        self.getPermissionToContinue()

    def getPermissionToContinue(self):
        print(
            f"\n Title: {self.youtube.title} \n Author: {self.youtube.author} \n Size: {file_size:.2f}MB "
            f"\n Resolution: {self.stream.resolution} \n FPS: {self.stream.fps} \n"
        )
        if input("Do you want it? (default = (y)es) or (n)o: ").lower() == "n":
            self.showStreams()
        else:
            self.main()

    def download(self):
        self.stream.download()
        self.redis_client.set(self.youtube.title, f"Downloaded {file_size:.2f}MB")  # Save to Redis

    @staticmethod
    def onProgress(stream=None, chunk=None, remaining=None):
        file_downloaded = file_size - (remaining / 1000000)
        print(
            f"Downloading ... {file_downloaded / file_size * 100:0.2f}% [{file_downloaded:.1f}MB of {file_size:.1f}MB]",
            end="\r",
        )

    def main(self):
        try:
            self.download()
        except KeyboardInterrupt:
            print("Canceled.")
            sys.exit(0)


if __name__ == "__main__":
    try:
        YouTubeDownloader()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)
