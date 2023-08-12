from flask import Blueprint, request, render_template, send_file, url_for, g, jsonify

from settings import PAGINATION_PER_PAGE
from use_case.auth import UpdateUserProfile, UpdateUserPassword
from use_case.movie import CreateMovie, MyListMovie
from utils.decorator import authentication

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard/")


@dashboard_bp.route('/upload', methods=['GET', 'POST'])
@authentication
def upload_movie():
    if request.method == 'POST':
        input_data = {
            'title': request.form.get('title'),
            'description': request.form.get('description'),
            'movie_file': request.files.get('movieFile'),
            'thumbnail_file': request.files.get('thumbnailFile'),
        }
        use_case = CreateMovie(input_data, user_id=g.current_user.id)
        has_error, result = use_case.run()
        print(has_error, result)

    return render_template('upload_movie.html', form_action=url_for('dashboard.upload_movie'), user=g.current_user)


@dashboard_bp.route('/', methods=['GET', 'POST'])
@authentication
def profile():
    if request.method == 'POST':
        input_data = {
            'first_name': request.form.get('firstName'),
            'last_name': request.form.get('lastName'),
            'username': request.form.get('userName'),
            'email': request.form.get('email'),
        }
        input_data = {key: value for key, value in input_data.items() if value not in ('', None, " ")}
        has_error, result = UpdateUserProfile(input_data, g.current_user).run()
        return render_template('dashboard.html',
                               tab="profile",
                               has_error=has_error,
                               errors=result,
                               user=g.current_user)
    if request.method == 'GET':
        return render_template('dashboard.html', tab="profile", user=g.current_user)


@dashboard_bp.route('/update-password', methods=['GET', 'POST'])
@authentication
def change_password():
    if request.method == 'POST':
        input_data = {
            'old_password': request.form.get('oldPassword'),
            'new_password': request.form.get('newPassword'),
        }
        has_error, result = UpdateUserPassword(input_data, g.current_user).run()
        return render_template('dashboard.html',
                               tab="Password",
                               has_error=has_error,
                               errors=result,
                               user=g.current_user)
    if request.method == 'GET':
        return render_template('dashboard.html', user=g.current_user)


@dashboard_bp.route('/my-movies', methods=['GET'])
@authentication
def my_movies():
    input_data = {
        'per_page': PAGINATION_PER_PAGE,
        'page': int(request.args.get('page', 1))
    }

    has_error, result = MyListMovie(input_data=input_data, user=g.current_user).run()
    return render_template('my-movies.html',
                           has_error=has_error,
                           result=result,
                           user=g.current_user)


@dashboard_bp.route('/my-videos-load')
def load_my_videos():
    input_data = {
        'per_page': PAGINATION_PER_PAGE,
        'page': int(request.args.get('page', 1))
    }
    has_error, result = MyListMovie(input_data=input_data, user=g.current_user).run()
    html = render_template('my-movie-items.html', result=result)
    return jsonify({'html': html, 'len_items': len(result)})
