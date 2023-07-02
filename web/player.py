from flask import Blueprint, request, render_template, send_file

movie_bp = Blueprint("movie", __name__, url_prefix="/movie/")


@movie_bp.route('/')
def index():
    return render_template('index.html')


@movie_bp.route("/media/videos/<string:file_name>")
def return_manifest(file_name):
    return send_file(f'../media/videos/hi/{file_name}')
