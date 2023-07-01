import os
import subprocess
from logger import logger
from utils.helper import is_exist_path, mkdir
from settings import DEFAULT_RESOLUTION, OUTPUT_DIRECTORY


def create_multiple_resolutions(input_video_path: str, output_folder: str = OUTPUT_DIRECTORY):
    if not is_exist_path(os.path.join(OUTPUT_DIRECTORY, output_folder)):
        mkdir(os.path.join(OUTPUT_DIRECTORY, output_folder))
    output_folder = os.path.join(OUTPUT_DIRECTORY, output_folder)
    command = f'ffmpeg -i {input_video_path} \
  -map 0:v:0 -map 0:a:0 -map 0:v:0 -map 0:a:0 -map 0:v:0 -map 0:a:0 \
  -c:v libx264 -crf 22 -c:a aac -ar 44100 \
  -filter:v:0 scale=w=480:h=360  -maxrate:v:0 600k -b:a:0 500k \
  -filter:v:1 scale=w=640:h=480  -maxrate:v:1 1500k -b:a:1 1000k \
  -filter:v:2 scale=w=1280:h=720 -maxrate:v:2 3000k -b:a:2 2000k \
  -var_stream_map "v:0,a:0,name:360p v:1,a:1,name:480p v:2,a:2,name:720p" \
  -preset fast -hls_list_size 10 -threads 0 -f hls -hls_list_size 11000 \
  -hls_time 3 -hls_flags independent_segments \
  -master_pl_name "livestream.m3u8" \
  -y "{output_folder}/livestream-%v.m3u8"'
    logger.debug(f'ffmpeg-command:: {command}')

    subprocess.call(command, shell=True)


if __name__ == "__main__":
    create_multiple_resolutions(input_video_path="media/videos/00-intro.mp4", output_folder="tmp")
