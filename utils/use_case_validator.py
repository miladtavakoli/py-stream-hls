from utils.validators import ValidatorUsername, ValidatorEmail, ValidatorPassword, ValidateFirstName, ValidateLastName


class BaseUseCaseValidator:
    def __init__(self):
        self.errors = self.__all_errors()
        self.is_valid = True if self.errors is None else False

    def __all_errors(self) -> dict | None:
        errors = {}
        for field, field_validator in vars(self).items():
            if not field_validator.is_valid:
                errors.update({field: field_validator.errors})
        return errors if len(errors) > 0 else None


class CreateUserUseCaseValidator(BaseUseCaseValidator):
    def __init__(self, input_data):
        self.username = ValidatorUsername(input_data=input_data.get('username', None))
        self.email = ValidatorEmail(input_data=input_data.get('email', None))
        self.password = ValidatorPassword(input_data=input_data.get('password', None))
        self.first_name = ValidateFirstName(input_data=input_data.get('first_name', None))
        self.last_name = ValidateLastName(input_data=input_data.get('last_name', None))
        super(CreateUserUseCaseValidator, self).__init__()
