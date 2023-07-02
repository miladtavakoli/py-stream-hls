import hashlib

from celery_tasks.tasks import task_create_hls_files
from repository.file import Movie
from settings import MEDIA_DIRECTORY, MEDIA_DIRECTORY_FULL_PATH, PROJECT_DIRECTORY
# from tasks import task_create_hls_files
from utils.use_case_validator import CreateFileMovieValidator
from utils.helper import mkdir, is_exist_path, join_path, generate_random_characters
from slugify import slugify


class CreateMovie:
    def __init__(self, input_data, user_id):
        self.validator = CreateFileMovieValidator(input_data)
        self.user_id = user_id

    def _save_movie(self, movie_id: int):
        save_path = join_path(MEDIA_DIRECTORY_FULL_PATH, str(movie_id))
        if not is_exist_path(save_path):
            mkdir(save_path)
        new_file_name = f"{generate_random_characters()}{self.validator.movie_file.file_extension}"
        saved_file = join_path(save_path, new_file_name)
        # self.validator.movie_file.validated_value.filename = new_file_name
        self.validator.movie_file.validated_value.save(saved_file)
        # TODO: Send to celery for ffmpeg
        return join_path(MEDIA_DIRECTORY, f"{movie_id}/{new_file_name}")

    def _save_movie_thumbnail(self, movie_id: int):
        save_path = join_path(MEDIA_DIRECTORY_FULL_PATH, str(movie_id))
        if not is_exist_path(save_path):
            mkdir(save_path)
        new_file_name = f"thumbnail_{generate_random_characters()}{self.validator.thumbnail_file.file_extension}"
        saved_file = join_path(save_path, new_file_name)
        # self.validator.thumbnail_file.validated_value.filename = new_file_name
        self.validator.thumbnail_file.validated_value.save(saved_file)
        # TODO: Send to celery for ffmpeg for screen shot
        return join_path(MEDIA_DIRECTORY, f"{movie_id}/{new_file_name}")

    def make_hash_value(self):
        hasher = hashlib.sha256(self.validator.movie_file.validated_value.read()).hexdigest()
        self.validator.movie_file.validated_value.seek(0)
        return hasher

    def create_movie(self, hash_value: str, existed_movie: Movie = None) -> tuple[bool, Movie | dict]:
        has_error = False
        try:
            m = Movie()
            m.user_id = self.user_id
            m.title = self.validator.title.validated_value
            m.description = self.validator.description.validated_value
            m.imdb_tag = self.validator.imdb_tag.validated_value
            m.slug = slugify(self.validator.title.validated_value)
            m.is_private = False
            m.hash_value = hash_value
            m.save()
            m = Movie.query.filter(Movie.id == m.id).first()

            if existed_movie is None:
                saved_movie = self._save_movie(movie_id=m.id)
            else:
                saved_movie = existed_movie.original_filename
            if existed_movie is None:
                saved_thumbnail = self._save_movie_thumbnail(movie_id=m.id)
            else:
                saved_thumbnail = self._save_movie_thumbnail(movie_id=existed_movie.id)
            m.original_filename = saved_movie
            m.thumbnail = saved_thumbnail
            m.save()
            result = m
        except Exception as e:
            has_error = True
            result = {"CREATE_MOVIE_ERROR": str(e)}
        return has_error, result

    @staticmethod
    def checks_availability_movie_by(hash_value):
        movie = Movie.query.filter(Movie.hash_value == hash_value).order_by(Movie.id.desc())
        return movie.first() if movie.count() > 0 else None

    def run(self) -> tuple[bool, Movie | dict]:
        if not self.validator.is_valid:
            has_error = True
            errors = self.validator.errors
            return has_error, errors

        hash_value = self.make_hash_value()
        existed_movie = self.checks_availability_movie_by(hash_value)
        has_error, result_movie = self.create_movie(hash_value, existed_movie)
        if has_error:
            return has_error, result_movie
        if not existed_movie:
            task_create_hls_files.delay(result_movie.id)
        return False, {"CREATE_MOVIE": "Successful..."}
