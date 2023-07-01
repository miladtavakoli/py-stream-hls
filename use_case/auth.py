from repository.user import User
from utils.use_case_validator import CreateUserUseCaseValidator


class CreateUser:
    def __init__(self, input_data):
        self.validator = CreateUserUseCaseValidator(input_data)

    def create_user(self) -> tuple[bool, User | dict]:
        has_error = False
        try:
            u = User()
            u.username = self.validator.username.validated_value
            u.email = self.validator.email.validated_value
            u.password = self.validator.password.validated_value
            u.first_name = self.validator.first_name.validated_value
            u.last_name = self.validator.last_name.validated_value
            u.save()
            result = u
        except Exception as e:
            has_error = True
            result = User
        return has_error, result

    def run(self) -> tuple[bool, User | dict | None]:
        if not self.validator.is_valid:
            has_error = True
            result = self.validator.errors
        else:
            has_error, result = self.create_user()
        return has_error, result

