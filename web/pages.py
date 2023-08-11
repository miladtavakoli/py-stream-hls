from flask import Blueprint, request, render_template, send_file, make_response, g, jsonify
from settings import PROJECT_DIRECTORY, PAGINATION_PER_PAGE
from use_case.auth import GetUser
from use_case.movie import GetMovie, HomeListMovie

pages_bp = Blueprint("pages", __name__, url_prefix="/")


@pages_bp.route('/')
def home():
    input_data = {
        'per_page': PAGINATION_PER_PAGE,
        'page': int(request.args.get('page', 1))
    }
    has_error, user_result = GetUser(user_id=g.user_id).run() if g.user_id else (True, None)
    user = user_result if not has_error else None
    has_error, result = HomeListMovie(input_data).run()
    render = render_template('home.html', has_error=has_error, result=result, user=user)
    response = make_response(render)
    return response


@pages_bp.route('/home/load-movie')
def load_items():
    input_data = {
        'per_page': PAGINATION_PER_PAGE,
        'page': int(request.args.get('page', 1))
    }
    has_error, items_result = HomeListMovie(input_data).run()
    html = render_template('items.html', result=items_result)
    return jsonify({'html': html, 'len_items': len(items_result)})


@pages_bp.route('movie/<int:movie_id>')
def movie_detail(movie_id):
    user_id = g.user_id
    has_error, movie_result = GetMovie(movie_id, user_id).run()
    return render_template('movie-detail.html',
                           has_error=has_error,
                           movie_result=movie_result)


@pages_bp.route("movie/<path:file_name>")
def return_manifest(file_name):
    # TODO: Authorize owner file if movie is private
    if not file_name.startswith('media/videos'):
        return ""
    return send_file(f"{PROJECT_DIRECTORY}/{file_name}")
