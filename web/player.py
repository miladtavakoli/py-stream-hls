from flask import Blueprint, request, render_template, send_file

from settings import PROJECT_DIRECTORY, MEDIA_DIRECTORY_FULL_PATH, MEDIA_VIDEO_DIRECTORY
from use_case.movie import GetMovie
from utils.helper import join_path

movie_bp = Blueprint("movie", __name__, url_prefix="/movie/")


@movie_bp.route('/<int:movie_id>')
def index(movie_id):
    user_id = 1
    has_error, movie_result = GetMovie(movie_id, user_id).run()
    return render_template('movie-detail.html',
                           has_error=has_error,
                           movie_result=movie_result)


@movie_bp.route("/<path:file_name>")
def return_manifest(file_name):
    user_id = 1
    if not file_name.startswith('media/videos'):
        return ""
    return send_file(f"{PROJECT_DIRECTORY}/{file_name}")
