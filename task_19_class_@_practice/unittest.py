import unittest
def validate_email_format(email):
    if not isinstance(email, str):
        raise TypeError("Email must be a string")
    if email.count('@') == 1:
        return "Valid"
    return "Invalid"
class TestEmailValidator(unittest.TestCase):
    def test_valid_email(self):
        self.assertEqual(validate_email_format("student@university.edu"), "Valid")
    def test_missing_at_symbol(self):
        self.assertEqual(validate_email_format("studentuniversity.edu"), "Invalid")
    def test_multiple_at_symbols(self):
        self.assertEqual(validate_email_format("student@@university.edu"), "Invalid")
    def test_integer_input_raises_type_error(self):
        with self.assertRaises(TypeError):
            validate_email_format(1)
    def test_none_input_raises_type_error(self):
        with self.assertRaises(TypeError):
            validate_email_format(None)

    def test_type_error_message(self):
        with self.assertRaises(TypeError) as context:
            validate_email_format(1)
        self.assertEqual(str(context.exception), "Email must be a string")
