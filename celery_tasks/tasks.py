from __future__ import absolute_import, unicode_literals

from logger import logger
from celery import shared_task

from ffmpeg import create_hls_files
from repository.file import Movie
from settings import MEDIA_DIRECTORY, MEDIA_DIRECTORY_FULL_PATH, PROJECT_DIRECTORY
from utils.helper import join_path


@shared_task(name='celery_tasks.task_create_hls_files')
def task_create_hls_files(movie_id: int):
    try:
        movie = Movie.query.filter(Movie.id == movie_id).first()
        if movie is None:
            print("__" * 50)
            return True, {"TASK_CREATE_HLS_FILES": "Movie not found."}
        hls_file_name = create_hls_files(input_video_path=join_path(PROJECT_DIRECTORY, movie.original_filename),
                                         output_folder=join_path(MEDIA_DIRECTORY_FULL_PATH, str(movie_id)))
        movie.hls_path = join_path(join_path(MEDIA_DIRECTORY, str(movie_id)), hls_file_name)
        movie.save()
        logger.debug(f"celery hls file created :: {movie.hls_path}")
        return True
    except Exception as e:
        has_error = True
        result = {"TASK_CREATE_HLS_FILES": str(e)}
        print("*" * 10, e)
    return has_error
