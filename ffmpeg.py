import os
import subprocess
from logger import logger
from utils import is_exist_path, mkdir
from settings import OUTPUT_DIRECTORY, DEFAULT_RESOLUTION, PROJECT_DIRECTORY


def create_multiple_resolutions(input_video_path: str,
                                output_folder: str = OUTPUT_DIRECTORY,
                                resolutions: list[str] = DEFAULT_RESOLUTION):
    if not is_exist_path(output_folder):
        mkdir(f"{output_folder}/")
    output_folder = f"{PROJECT_DIRECTORY}/{output_folder}"

    for resolution in resolutions:
        output_path = os.path.join(output_folder, f"__{resolution}.mp4")
        command = f"ffmpeg -i {input_video_path} -vf scale={resolution} -c:a copy {output_path}"
        subprocess.call(command, shell=True)
        logger.debug('')


if __name__ == "__main__":
    create_multiple_resolutions(input_video_path="media/videos/00-intro.mp4")
