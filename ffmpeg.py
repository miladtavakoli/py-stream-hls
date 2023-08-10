import os
import subprocess

from ffmpeg_lib.ffmpeg import Ffmpeg, OverlayText
from logger import logger
from utils.helper import is_exist_path, mkdir, join_path
from settings import MEDIA_DIRECTORY, MEDIA_DIRECTORY_FULL_PATH


def create_hls_files(input_video_path: str, output_folder: str = MEDIA_DIRECTORY) -> str:
    """
    Create 3 type of resolution : 480X360, 640X480, 1280X720 with m3u8 extensions
    Split to 3 second part.
    :param input_video_path:
    :param output_folder:
    :return: hls file -> `noob_stream.m3u8`
    """
    print("_________________ CREATE START _________________")
    command = f'ffmpeg -i {input_video_path} \
  -map 0:v:0 -map 0:a:0 -map 0:v:0 -map 0:a:0 -map 0:v:0 -map 0:a:0 \
  -c:v libx264 -crf 22 -c:a aac -ar 44100 \
  -filter:v:0 scale=w=480:h=360  -maxrate:v:0 600k -b:a:0 500k \
  -filter:v:1 scale=w=640:h=480  -maxrate:v:1 1500k -b:a:1 1000k \
  -filter:v:2 scale=w=1280:h=720 -maxrate:v:2 3000k -b:a:2 2000k \
  -var_stream_map "v:0,a:0,name:360p v:1,a:1,name:480p v:2,a:2,name:720p" \
  -preset fast -hls_list_size 10 -threads 0 -f hls -hls_playlist_type vod \
  -hls_time 3 -hls_flags independent_segments \
  -master_pl_name "noob_stream.m3u8" \
  -y "{output_folder}/noob_stream-%v.m3u8"'

    print(command)
    logger.debug(f'ffmpeg-command:: {command}')
    subprocess.call(command, shell=True)
    return "noob_stream.m3u8"


def run_ffmpeg(input_video_path: str, output_folder: str = MEDIA_DIRECTORY):
    f = Ffmpeg(input_file=input_video_path)
    f.output_dir = output_folder
    f.output_filename = 'noobstream'
    f.hls_time = 10
    f.overlay_text = OverlayText("noob_streamer.ir")
    f.run()
    return f"{f.output_filename}.m3u8"

