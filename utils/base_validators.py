import re
import os
import mimetypes
from abc import ABC, abstractmethod
from werkzeug.datastructures import FileStorage
from utils.helper import splitext


class BaseFieldValidator(ABC):
    """
    Class Variable:
        field_name (str) : Required, Used for user messages.  Example: "first_name"
        is_required (bool) :  Optional. Checks field input is not None. Example: True
    """

    field_name: str = None
    is_required: bool = None

    def __init__(self, input_data, is_required=False):
        self._is_valid: bool = True
        self._errors: list = []
        self.input_data = input_data
        self.is_required = is_required
        self.validate()

    def required_validate(self):
        if self.is_required and self.input_data is None:
            self._is_valid = False
            self._errors.append("Its required.")

    @abstractmethod
    def validate(self):
        pass

    @property
    def is_valid(self) -> bool:
        """
        :return:
            True if the validated was successful, False otherwise.
        """
        return self._is_valid

    @property
    def errors(self) -> list | None:
        """
        :return:
            List of all errors
        """
        return self._errors if self._is_valid is False else None

    @property
    def validated_value(self):
        if self.is_valid:
            return self.input_data
        return None


class StringFieldValidator(BaseFieldValidator):
    """
    Class Variable:
        regex_pattern (str) : Optional. Checks pattern of field input. Example:  r'^[\w\.-]+@[\w\.-]+\.\w+$'
        min_length (int) : Optional. Checks minimum length of field input. Example: 3
        maximum_length (str) : Optional. Checks maximum_length of field input. Example: 25
    """

    def __init__(self, input_data,
                 is_required=False,
                 min_length: int = None,
                 max_length: int = None,
                 regex: str = None):
        self.min_length = min_length
        self.max_length = max_length
        self.regex = regex
        super().__init__(input_data=input_data, is_required=is_required)

    def regex_validate(self):
        if isinstance(self.input_data, str) and self.regex is not None:
            if re.match(self.regex, self.input_data) is None:
                self._is_valid = False
                self._errors.append("Does not have a valid pattern.")

    def length_validate(self):
        if isinstance(self.input_data, str):
            if self.min_length is not None and len(self.input_data) < self.min_length:
                self._is_valid = False
                self._errors.append(f"Must be more than {self.min_length} characters.")

            if self.max_length is not None and len(self.input_data) > self.max_length:
                self._is_valid = False
                self._errors.append(f"Must be less than {self.max_length} characters.")

    def validate(self):
        if not isinstance(self.input_data, str) and (not self.is_required and self.input_data is not None):
            self._is_valid = False
            self._errors.append("Is not String.")

        for method in dir(self):
            if callable(getattr(self, method)) and method.endswith('_validate'):
                getattr(self, method)()
        return self.input_data


class IntegerFieldValidator(BaseFieldValidator):
    """
    Class Variable:
            min_value (int) : Optional. Checks input number has been greater than min_value. Example: 1
            max_value (int) : Optional. Checks input Number has been lower than max_value. Example: 10

    """

    def __init__(self, input_data,
                 is_required=False,
                 min_value: int = None,
                 max_value: int = None):
        self.min_value = min_value
        self.max_value = max_value
        super().__init__(input_data=input_data, is_required=is_required)

    def length_validate(self):
        if isinstance(self.input_data, int):
            if self.min_value is not None and self.input_data < self.min_value:
                self._is_valid = False
                self._errors.append(f"Must be greater than {self.min_value} .")

            if self.max_value is not None and self.input_data > self.max_value:
                self._is_valid = False
                self._errors.append(f"Must be lower than {self.max_value} .")

    def validate(self):
        if not isinstance(self.input_data, int) and (not self.is_required and self.input_data is not None):
            self._is_valid = False
            self._errors.append("Is not Integer.")

        for method in dir(self):
            if callable(getattr(self, method)) and method.endswith('_validate'):
                getattr(self, method)()
        return self.input_data


class FileFieldValidator(BaseFieldValidator):
    """
    Class Variable:
        allowed_mime_types (list[str]) : Optional. Checks Input File has valid mime type: Example: `['video/mp4']`
    """

    def __init__(self, input_data,
                 is_required=False,
                 allowed_mime_types: list[str] = None):
        self.allowed_mime_types = allowed_mime_types
        super().__init__(input_data=input_data, is_required=is_required)

    def mime_types_validate(self):
        if isinstance(self.input_data, FileStorage):
            file_type = mimetypes.guess_type(self.input_data.filename)[0]
            if self.allowed_mime_types is not None and file_type not in self.allowed_mime_types:
                self._is_valid = False
                self._errors.append(f"This file type {file_type} is not valid.")

    def validate(self):
        if not isinstance(self.input_data, FileStorage) and (not self.is_required and self.input_data is not None):
            self._is_valid = False
            self._errors.append("This is not valid file.")

        for method in dir(self):
            if callable(getattr(self, method)) and method.endswith('_validate'):
                getattr(self, method)()
        return self.input_data

    @property
    def file_extension(self):
        if self.is_valid:
            _, file_extension = splitext(self.input_data.filename)
            return file_extension
        return None
