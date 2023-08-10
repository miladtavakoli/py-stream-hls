import os.path
import subprocess
import json
from ffmpeg_lib import config
from ffmpeg_lib.exceptions import InputFileDoesNotExists, OutputDirectoryDoesNotExists
from ffmpeg_lib.resolutions import Resolutions

from logger import logger


class OverlayText:
    def __init__(self, text: str, font_size: int = 15, font_color: str = 'white', position: list[int, int] = (20, 20)):
        self.text = text
        self.font_size = font_size
        self.font_color = font_color
        self.position = position

    def create_command(self):
        command = f"-vf drawtext=text='{self.text}':" \
                  f"fontsize={self.font_size}:" \
                  f"fontcolor={self.font_color}" \
                  f":x={self.position[0]}:y={self.position[1]}"
        return command


class FfprobeResolution:
    def __init__(self, input_file: str):
        self.input_file = input_file

    def create_command(self):
        command = [
            'ffprobe',
            '-v', 'error',
            '-select_streams', 'v:0',
            '-show_entries', 'stream=width,height,bit_rate',
            '-of', 'json',
            self.input_file
        ]
        return command

    def run(self) -> (int, int, int):
        command = self.create_command()
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            output_json = json.loads(result.stdout)
            video_info = output_json['streams'][0]
            width = video_info['width']
            height = video_info['height']
            bit_rate = int(video_info['bit_rate']) if 'bit_rate' in video_info else None
            return int(width), int(height), int(bit_rate)
        except subprocess.CalledProcessError as e:
            logger.warning(f"Error running Ffprobe: {e}")
            return None, None, None


class Ffmpeg:
    def __init__(self, input_file=None):
        self._input_file: str = input_file
        self._output_dir: str = config.output_path
        self._output_filename: str = config.output_filename
        self._hls_time: int | str = config.hls_time
        self._resolutions: list[Resolutions] = config.default_resolution
        self._overlay_text: OverlayText | None = None

    @property
    def input_file(self) -> str:
        return self._input_file

    @input_file.setter
    def input_file(self, i_path: str):
        if i_path is None or not os.path.exists(i_path):
            raise InputFileDoesNotExists
        self._input_file = i_path

    @property
    def output_dir(self) -> str:
        return self._output_dir

    @output_dir.setter
    def output_dir(self, o_path):
        if not os.path.exists(o_path):
            raise OutputDirectoryDoesNotExists
        self._output_dir = o_path

    @property
    def output_filename(self) -> str:
        return self._output_filename

    @output_filename.setter
    def output_filename(self, o_filename: str):
        o_filename = o_filename.rstrip('.m3u8')
        self._output_filename = o_filename

    @property
    def hls_time(self) -> str:
        return str(self._hls_time)

    @hls_time.setter
    def hls_time(self, time: int):
        self._hls_time = time

    @property
    def resolutions(self) -> list[Resolutions]:
        return self._resolutions

    @resolutions.setter
    def resolutions(self, i_resolution: list[Resolutions]):
        self._resolutions = i_resolution

    @property
    def overlay_text(self) -> str:
        return self._overlay_text.create_command() if self._overlay_text is not None else None

    @overlay_text.setter
    def overlay_text(self, i_overlay_text: OverlayText):
        self._overlay_text = i_overlay_text

    @property
    def input_filename(self):
        return self.input_file.split('/')[-1].split('.')[0]

    def _create_resolution_command(self):
        org_w, org_h, org_bit = FfprobeResolution(input_file=self.input_file).run()
        resolutions = []
        for i in self.resolutions:
            if org_h >= i.height:
                resolutions.append(Resolutions(i.width, i.height, min(i.bitrate, org_bit), i.buf_size))
        resolution_command = []
        map_ = ""
        for i, r in enumerate(resolutions):
            tmp = [f'-filter:v:{i}', f"scale=w={r.width}:h={r.height}:force_original_aspect_ratio=decrease,setsar=1"]
            tmp.extend([f'-b:v:{i}', f"{r.bitrate}", f'-maxrate:v:{i}', f"{r.bitrate}"])
            tmp.extend(['-ar', '44100', f'-b:a:{i}', '100k'])
            map_ += f"v:{i},a:{i},name:{r.height}p "
            resolution_command.append(tmp)
        return resolution_command, map_, resolutions

    def command_creator(self):
        resolution_command, resolution_map, resolutions = self._create_resolution_command()
        command = ['ffmpeg', '-i', self.input_file, '-c:v', 'libx264', '-c:a', 'aac']
        if self.overlay_text is not None:
            command.append(self.overlay_text)
        command.extend(['-map', '0:v:0', '-map', '0:a:0'] * len(resolutions))
        for res in resolution_command:
            command.extend(res)
        command.extend(['-f', 'hls'])
        command.extend(['-var_stream_map', f'"{resolution_map}"'])
        command.extend(['-hls_time', self.hls_time])
        command.extend(['-preset', 'fast', '-hls_flags', 'independent_segments'])
        command.extend(['-hls_playlist_type', 'vod'])
        command.extend(['-master_pl_name', f"{self.output_filename}.m3u8"])
        command.extend(['-y', f"{self.output_dir}/{self.output_filename}-%v.m3u8"])
        return command

    def run(self):
        try:
            if not os.path.exists(self.input_file):
                return InputFileDoesNotExists
            command = self.command_creator()
            c = ' '.join(command)
            subprocess.run(c, check=True, shell=True)
        except InputFileDoesNotExists:
            logger.error("Input file does not exists.")
            return None
        except subprocess.CalledProcessError as e:
            logger.error(f"Error executing FFmpeg command: {e}")
            return None
        except Exception as e:
            logger.error(f"ERROR :: {e}")
