class Resolutions:
    def __init__(self, width: int, height: int, bitrate: int, buf_size: str):
        self.width = width
        self.height = height
        self.bitrate = bitrate
        self.buf_size = buf_size


d_360p = Resolutions(width=640, height=360, bitrate=800*1000, buf_size='1600k')
d_480p = Resolutions(width=854, height=480, bitrate=1200*1000, buf_size='2400k')
d_720p = Resolutions(width=1280, height=720, bitrate=2000*1000, buf_size='4000k')
d_1080p = Resolutions(width=1920, height=1080, bitrate=5000*1000, buf_size='10000k')
d_2160p = Resolutions(width=3840, height=2160, bitrate=15000*1000, buf_size='300000k')


