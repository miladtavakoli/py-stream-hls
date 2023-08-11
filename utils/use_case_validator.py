from utils.validators import ValidatorUsername, ValidatorEmail, ValidatorPassword, ValidateFirstName, ValidateLastName, \
    ValidateMovieFile, ValidateMovieThumbnailFile, ValidateMovieTitle, ValidateMovieDescription, ValidateMovieImdbTag, \
    ValidatePaginationPage, ValidatePaginationPerPage, ValidateHomeSearch


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


class CreateFileMovieValidator(BaseUseCaseValidator):
    def __init__(self, input_data):
        self.movie_file = ValidateMovieFile(input_data=input_data.get('movie_file', None))
        self.thumbnail_file = ValidateMovieThumbnailFile(input_data=input_data.get('thumbnail_file', None))
        self.title = ValidateMovieTitle(input_data=input_data.get('title', None))
        self.description = ValidateMovieDescription(input_data=input_data.get('description', None))
        self.imdb_tag = ValidateMovieImdbTag(input_data=input_data.get('imdb_tag', None))
        super(CreateFileMovieValidator, self).__init__()


class LoginUserValidator(BaseUseCaseValidator):
    def __init__(self, input_data):
        self.username = ValidatorUsername(input_data=input_data.get('username', None))
        self.password = ValidatorPassword(input_data=input_data.get('password', None))
        super(LoginUserValidator, self).__init__()


class HomePageVideosValidator(BaseUseCaseValidator):
    def __init__(self, input_data):
        self.search = ValidateHomeSearch(input_data=input_data.get('search', None))
        self.page = ValidatePaginationPage(input_data=input_data.get('page', None))
        self.per_page = ValidatePaginationPerPage(input_data=input_data.get('per_page', None))
        super(HomePageVideosValidator, self).__init__()


class UpdateUserUseCaseValidator(BaseUseCaseValidator):
    def __init__(self, input_data):
        self.username = ValidatorUsername(input_data=input_data.get('username', None))
        self.email = ValidatorEmail(input_data=input_data.get('email', None))
        self.first_name = ValidateFirstName(input_data=input_data.get('first_name', None))
        self.last_name = ValidateLastName(input_data=input_data.get('last_name', None))
        super(UpdateUserUseCaseValidator, self).__init__()


class UpdateUserPasswordUseCaseValidator(BaseUseCaseValidator):
    def __init__(self, input_data):
        self.old_password = ValidatorPassword(input_data=input_data.get('old_password', None))
        self.new_password = ValidatorPassword(input_data=input_data.get('new_password', None))
        super(UpdateUserPasswordUseCaseValidator, self).__init__()

