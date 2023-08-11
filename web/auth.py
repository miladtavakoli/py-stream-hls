from flask import Blueprint, request, render_template, redirect, make_response, url_for

import settings
from use_case.auth import LoginUser, CreateUser, LogoutUser
from datetime import datetime, timedelta

auth_bp = Blueprint("auth", __name__, url_prefix="/auth/")


@auth_bp.route('/', methods=['GET', 'POST'])
def auth_index():
    form_display = {
        "login": "block",
        "sign-up": None,
    }
    if request.method == 'POST':
        input_data = {
            "username": request.form.get("username"),
            "password": request.form.get("password"),
        }
        use_case = LoginUser(input_data)
        has_error, result = use_case.run()

        if has_error:
            return make_response(render_template('login.html', form_display=form_display,
                                                 has_error=has_error,
                                                 errors=result))
        response = make_response(redirect(url_for("pages.home")))
        expire_time = datetime.now() + timedelta(seconds=settings.AUTHORIZATION_EXPIRE_TIME)
        response.set_cookie('authentication', result, expires=expire_time)
        return response
    if request.method == 'GET':
        return render_template('login.html', form_display=form_display, )


@auth_bp.route('/sign-up', methods=["POST", "GET"])
def sign_up():
    form_display = {
        "login": None,
        "sign-up": "block",
    }
    if request.method == 'POST':
        input_data = {
            "username": request.form.get("username"),
            "email": request.form.get("email"),
            "password": request.form.get("password"),
        }
        use_case = CreateUser(input_data)
        has_error, result = use_case.run()

        if has_error:
            return make_response(render_template('login.html', form_display=form_display,
                                                 has_error=has_error,
                                                 errors=result))
        response = make_response(redirect(url_for("pages.home")))
        expire_time = datetime.now() + timedelta(seconds=settings.AUTHORIZATION_EXPIRE_TIME)
        response.set_cookie('authentication', result, expires=expire_time)
        return response
    if request.method == 'GET':
        return render_template('login.html', form_display=form_display )


@auth_bp.route('/logout', methods=["GET"])
def logout():
    input_data = {
        "token": request.cookies.get('authentication')
    }
    use_case = LogoutUser(input_data)
    use_case.run()
    response = make_response(redirect(url_for("pages.home")))
    response.delete_cookie('authentication')
    return response
