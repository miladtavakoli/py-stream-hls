from flask import Blueprint, request, render_template, send_file, url_for
from use_case.movie import CreateMovie
from utils.decorator import authentication

panel_bp = Blueprint("panel", __name__, url_prefix="/panel/")


@panel_bp.route('/upload', methods=['GET', 'POST'])
@authentication
def upload_movie():
    if request.method == 'POST':
        input_data = {
            'title': request.form.get('title'),
            'description': request.form.get('description'),
            'movie_file': request.files.get('movieFile'),
            'thumbnail_file': request.files.get('thumbnailFile'),
        }
        use_case = CreateMovie(input_data, user_id=1)
        has_error, result = use_case.run()
        print(has_error, result)

    return render_template('upload_movie.html', form_action=url_for('panel.upload_movie'))
