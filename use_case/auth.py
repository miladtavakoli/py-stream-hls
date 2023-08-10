from repository.user import User
from utils.exceptions import ValidatorInputRequired, ClassInitializingException
from utils.helper import FlaskSession
from utils.use_case_validator import CreateUserUseCaseValidator, LoginUserValidator
from flask_bcrypt import generate_password_hash, check_password_hash


class CreateUser:
    def __init__(self, input_data):
        self.validator = CreateUserUseCaseValidator(input_data)

    def create_user(self) -> tuple[bool, User | dict]:
        has_error = False
        try:
            u = User()
            u.username = self.validator.username.validated_value.lower()
            u.email = self.validator.email.validated_value
            u.password = generate_password_hash(self.validator.password.validated_value, 10).decode('utf-8')
            u.first_name = self.validator.first_name.validated_value
            u.last_name = self.validator.last_name.validated_value
            u.save()
            result = u
        except Exception as e:
            has_error = True
            result = {"msg": str(e)}
        return has_error, result

    def is_existed_username(self) -> bool:
        u = User.query.filter(User.username == self.validator.username.validated_value.lower()).first()
        return u is not None

    def is_existed_email(self) -> bool:
        u = User.query.filter(User.email == self.validator.email.validated_value.lower()).first()
        return u is not None

    def check_unique_fields(self) -> tuple[bool, dict]:
        errors = {}
        has_error = False
        if self.is_existed_username():
            has_error = True
            errors.update({"Username": ["Choose another username. Username has taken."]})
        if self.is_existed_email():
            has_error = True
            errors.update({"Email": ["Choose another email. Email has taken."]})
        return has_error, errors

    def run(self) -> tuple[bool, User | dict | None]:
        if not self.validator.is_valid:
            return True, self.validator.errors
        has_error, errors = self.check_unique_fields()
        if has_error:
            return True, errors
        has_error, result = self.create_user()
        return has_error, result


class LoginUser:
    def __init__(self, input_data):
        self.validator = LoginUserValidator(input_data)

    def get_user(self) -> tuple[bool, User | None]:
        user = User.query.filter(User.username == self.validator.username.validated_value.lower()).first()
        if user is None:
            return True, None
        return False, user

    def is_password_match(self, saved_password: str) -> bool:
        return check_password_hash(saved_password.encode('utf8'), self.validator.password.validated_value)

    def run(self) -> tuple[bool, User | dict]:
        if not self.validator.is_valid:
            return True, self.validator.errors
        has_error, user = self.get_user()
        if has_error or self.is_password_match(user.password):
            return True, {"msg": "Username or password is incorrect!"}

        token = FlaskSession().create_token(user_id=user.id)

        return False, token


class LogoutUser:
    def __init__(self, input_data):
        self.input_data = input_data

    def run(self) -> tuple[bool, User | dict]:
        FlaskSession().revoke_token(self.input_data['token'])
        return False, {"msg": "User logout successfully!"}


class GetUser:
    def __init__(self, user_id: int = None, username: str = None):
        if user_id is None and username is None:
            raise ClassInitializingException("username or user_id is required.")
        self.user_id = user_id
        self.username = username

    def get_user_by_user_id(self) -> tuple[bool, User | dict]:
        user = User.query.filter(User.id == self.user_id).first()
        if user is None:
            return True, {"msg": "User Not Found"}
        return False, user

    def get_user_by_username(self) -> tuple[bool, User | dict]:
        user = User.query.filter(User.username == self.username).first()
        if user is None:
            return True, {"msg": "User Not Found"}
        return False, user

    def run(self) -> tuple[bool, User | dict]:
        if self.user_id is not None:
            return self.get_user_by_user_id()
        return self.get_user_by_user_id()
