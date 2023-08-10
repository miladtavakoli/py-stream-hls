class ValidatorInputRequired(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class ValidationException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class ClassInitializingException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class AuthenticationRequired(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)
