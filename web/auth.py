from flask import Blueprint, request, render_template, send_file

auth_bp = Blueprint("auth", __name__, url_prefix="/auth/")


@auth_bp.route('/')
def index():
    return render_template('index.html')


@auth_bp.route("/media/videos/<string:file_name>")
def return_manifest(file_name):
    return send_file(f'../media/videos/{file_name}')
