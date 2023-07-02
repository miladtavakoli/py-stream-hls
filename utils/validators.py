from utils.base_validators import StringFieldValidator, FileFieldValidator


class ValidatorUsername(StringFieldValidator):
    def __init__(self, input_data, ):
        super(ValidatorUsername, self).__init__(input_data=input_data, is_required=True,
                                                regex=r'^[a-zA-Z0-9_-]{3,20}$',
                                                min_length=3, max_length=30)


class ValidatorEmail(StringFieldValidator):
    def __init__(self, input_data):
        super(ValidatorEmail, self).__init__(input_data=input_data, is_required=True,
                                             regex=r'^[\w\.-]+@[\w\.-]+\.\w+$',
                                             min_length=3, max_length=100)


class ValidatorPassword(StringFieldValidator):
    def __init__(self, input_data):
        super(ValidatorPassword, self).__init__(input_data=input_data, is_required=True,
                                                min_length=6, max_length=50)


class ValidateFirstName(StringFieldValidator):
    def __init__(self, input_data):
        super(ValidateFirstName, self).__init__(input_data=input_data, is_required=False,
                                                min_length=3, max_length=200)


class ValidateLastName(StringFieldValidator):
    def __init__(self, input_data):
        super(ValidateLastName, self).__init__(input_data=input_data, is_required=False,
                                               min_length=3, max_length=200)


class ValidateMovieTitle(StringFieldValidator):
    def __init__(self, input_data):
        super(ValidateMovieTitle, self).__init__(input_data=input_data, is_required=True,
                                                 min_length=5, max_length=400)


class ValidateMovieFile(FileFieldValidator):
    def __init__(self, input_data):
        super(ValidateMovieFile, self).__init__(input_data=input_data, is_required=True,
                                                allowed_mime_types=['video/mp4', 'video/webm',
                                                                    'video/x-msvideo', "video/x-matroska"])


class ValidateMovieThumbnailFile(FileFieldValidator):
    def __init__(self, input_data):
        super(ValidateMovieThumbnailFile, self).__init__(input_data=input_data, is_required=True,
                                                         allowed_mime_types=['image/jpeg', 'image/png',
                                                                             'image/bmp''image/gif',
                                                                             "image/tiff", 'image/webp'])


class ValidateMovieDescription(StringFieldValidator):
    def __init__(self, input_data):
        super(ValidateMovieDescription, self).__init__(input_data=input_data, is_required=False,
                                                       min_length=10, max_length=600)


class ValidateMovieImdbTag(StringFieldValidator):
    def __init__(self, input_data):
        super(ValidateMovieImdbTag, self).__init__(input_data=input_data, is_required=False,
                                                   min_length=10, max_length=600)
