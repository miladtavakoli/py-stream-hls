from test import BaseStreamTestCase, app
from utils.validators import ValidatorUsername, ValidatorEmail, ValidateFirstName, ValidateLastName, ValidatorPassword


class ValidatorUsernameTestCase(BaseStreamTestCase):
    def test_rejects_required(self):
        invalid_input = None
        validation = ValidatorUsername(invalid_input)
        self.assertFalse(validation.is_valid)
        self.assertIn("Its required.", validation.errors)

    def test_rejects_min_length(self):
        invalid_input = "er"
        validation = ValidatorUsername(invalid_input)
        self.assertFalse(validation.is_valid)
        self.assertIn("Must be more than 3 characters.", validation.errors)

    def test_rejects_max_length(self):
        invalid_input = "error" * 10
        validation = ValidatorUsername(invalid_input)
        self.assertFalse(validation.is_valid)
        self.assertIn("Must be less than 30 characters.", validation.errors)

    def test_rejects_regex(self):
        invalid_input = "M!L@D"
        validation = ValidatorUsername(invalid_input)
        self.assertFalse(validation.is_valid)
        self.assertIn("Does not have a valid pattern.", validation.errors)

    def test_valid(self):
        valid_input = "Milad"
        validation = ValidatorUsername(valid_input)
        self.assertTrue(validation.is_valid)
        self.assertFalse(validation.errors)


class ValidatorEmailTestCase(BaseStreamTestCase):
    def test_rejects_required(self):
        invalid_input = None
        validation = ValidatorEmail(invalid_input)
        self.assertFalse(validation.is_valid)
        self.assertIn("Its required.", validation.errors)

    def test_rejects_min_length(self):
        invalid_input = "er"
        validation = ValidatorEmail(invalid_input)
        self.assertFalse(validation.is_valid)
        self.assertIn("Must be more than 3 characters.", validation.errors)

    def test_rejects_max_length(self):
        invalid_input = "error" * 100
        validation = ValidatorEmail(invalid_input)
        self.assertFalse(validation.is_valid)
        self.assertIn("Must be less than 100 characters.", validation.errors)

    def test_rejects_regex(self):
        invalid_input = "Milad"
        validation = ValidatorEmail(invalid_input)
        self.assertFalse(validation.is_valid)
        self.assertIn("Does not have a valid pattern.", validation.errors)

    def test_valid(self):
        valid_input = "8590410@gmail.com"
        validation = ValidatorEmail(valid_input)
        self.assertTrue(validation.is_valid)
        self.assertFalse(validation.errors)


class ValidatorPasswordTestCase(BaseStreamTestCase):
    def test_rejects_required(self):
        invalid_input = None
        validation = ValidatorPassword(invalid_input)
        self.assertFalse(validation.is_valid)
        self.assertIn("Its required.", validation.errors)

    def test_rejects_min_length(self):
        invalid_input = "er0r"
        validation = ValidatorPassword(invalid_input)
        self.assertFalse(validation.is_valid)
        self.assertIn("Must be more than 6 characters.", validation.errors)

    def test_rejects_max_length(self):
        invalid_input = "error" * 100
        validation = ValidatorPassword(invalid_input)
        self.assertFalse(validation.is_valid)
        self.assertIn("Must be less than 50 characters.", validation.errors)

    def test_valid(self):
        valid_input = "S@MpL3Pa$$w0rd"
        validation = ValidatorPassword(valid_input)
        self.assertTrue(validation.is_valid)
        self.assertFalse(validation.errors)


class ValidateFirstNameTestCase(BaseStreamTestCase):
    def test_rejects_required(self):
        invalid_input = None
        validation = ValidateFirstName(invalid_input)
        self.assertTrue(validation.is_valid)
        self.assertFalse(validation.errors)

    def test_rejects_min_length(self):
        invalid_input = "er"
        validation = ValidateFirstName(invalid_input)
        self.assertFalse(validation.is_valid)
        self.assertIn("Must be more than 3 characters.", validation.errors)

    def test_rejects_max_length(self):
        invalid_input = "error" * 100
        validation = ValidateFirstName(invalid_input)
        self.assertFalse(validation.is_valid)
        self.assertIn("Must be less than 200 characters.", validation.errors)

    def test_valid(self):
        valid_input = "Milad"
        validation = ValidateFirstName(valid_input)
        self.assertTrue(validation.is_valid)
        self.assertFalse(validation.errors)


class ValidateLastNameTestCase(BaseStreamTestCase):
    def test_rejects_required(self):
        invalid_input = None
        validation = ValidateLastName(invalid_input)
        self.assertTrue(validation.is_valid)
        self.assertFalse(validation.errors)

    def test_rejects_min_length(self):
        invalid_input = "er"
        validation = ValidateLastName(invalid_input)
        self.assertFalse(validation.is_valid)
        self.assertIn("Must be more than 3 characters.", validation.errors)

    def test_rejects_max_length(self):
        invalid_input = "error" * 100
        validation = ValidateLastName(invalid_input)
        self.assertFalse(validation.is_valid)
        self.assertIn("Must be less than 200 characters.", validation.errors)

    def test_valid(self):
        valid_input = "Tavakoli"
        validation = ValidateLastName(valid_input)
        self.assertTrue(validation.is_valid)
        self.assertFalse(validation.errors)

