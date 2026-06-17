import unittest

from kgram import read_text, clean_text, build_kgram_model, get_next_token_options


class TestCleanTextLogic(unittest.TestCase):
    """Tests for the clean_text function."""

    def test_lowercase(self):
        """Verify that text is converted to lowercase."""
        tokens = clean_text('1\nHELLO! "World": sings\n')
        self.assertIn("hello", tokens)
        self.assertIn("world", tokens)
        self.assertIn("sings", tokens)
        self.assertNotIn("HELLO", tokens)

    def test_end_token(self):
        """Verify that each poem ends with <END>."""
        tokens = clean_text("1\nthe bird sings.\n")
        self.assertIn("<END>", tokens)

    def test_comma_as_token(self):
        """Verify that commas are treated as separate tokens."""
        tokens = clean_text("1\nthe bird sings, and flies.\n")
        self.assertIn(",", tokens)

    def test_period_as_token(self):
        """Verify that periods are treated as separate tokens."""
        tokens = clean_text("1\nthe bird sings.\n")
        self.assertIn(".", tokens)

    def test_multiple_poems(self):
        """Verify that multiple poems are all tokenized correctly."""
        text = "1\nthe bird sings.\n\n2\nthe moon shines.\n"
        tokens = clean_text(text)
        # two poems means two <END> tokens
        self.assertEqual(tokens.count("<END>"), 2)

    def test_empty_lines_ignored(self):
        """Verify that empty lines are not added as tokens."""
        tokens = clean_text("1\nthe bird sings.\n\n\n")
        self.assertNotIn("", tokens)

    def test_other_punctuation_removed(self):
        """Verify that punctuation other than comma and period is removed."""
        tokens = clean_text('1\n"what language is thine, o sea?"\n')
        # quotes and question marks should be removed
        self.assertIn("what", tokens)
        self.assertIn("sea", tokens)
        self.assertNotIn('"what', tokens)
        self.assertNotIn('sea?"', tokens)


class TestBuildModelBasic(unittest.TestCase):
    """Tests for the build_kgram_model function."""

    def setUp(self):
        """Set up a simple text for testing."""
        self.text = "1\nthe bird sings.\n\n2\nthe bird flies.\n"

    def test_basic_model(self):
        """Verify that the model contains expected k-grams."""
        model = build_kgram_model(self.text, 2)
        self.assertIn(("the", "bird"), model)

    def test_phrase_appearing_twice_updates_count(self):
        """Verify that a phrase appearing twice updates the count correctly."""
        model = build_kgram_model(self.text, 2)
        # "the bird" appears twice, once before sings and once before flies
        self.assertEqual(model[("the", "bird")]["sings"], 1)
        self.assertEqual(model[("the", "bird")]["flies"], 1)

    def test_invalid_k_type(self):
        """Verify that non-integer k raises TypeError."""
        with self.assertRaises(TypeError):
            build_kgram_model(self.text, "2")

    def test_invalid_k_bool(self):
        """Verify that bool k raises TypeError."""
        with self.assertRaises(TypeError):
            build_kgram_model(self.text, True)

    def test_invalid_k_zero(self):
        """Verify that k=0 raises ValueError."""
        with self.assertRaises(ValueError):
            build_kgram_model(self.text, 0)

    def test_invalid_k_negative(self):
        """Verify that negative k raises ValueError."""
        with self.assertRaises(ValueError):
            build_kgram_model(self.text, -1)

    def test_invalid_text_type(self):
        """Verify that non-string text raises TypeError."""
        with self.assertRaises(TypeError):
            build_kgram_model(123, 2)

    def test_k_too_large(self):
        """Verify that k larger than token count raises ValueError."""
        with self.assertRaises(ValueError):
            build_kgram_model(self.text, 1000)


class TestGetNextTokenOptions(unittest.TestCase):
    """Tests for the get_next_token_options function."""

    def setUp(self):
        """Set up a simple model for testing."""
        self.model = {
            ("the", "bird"): {"sings": 1, "flies": 2},
            ("bird", "sings"): {"<END>": 1}
        }

    def test_existing_kgram(self):
        """Verify that existing k-gram returns correct options."""
        result = get_next_token_options(("the", "bird"), self.model)
        self.assertEqual(result, {"sings": 1, "flies": 2})

    def test_missing_kgram(self):
        """Verify that missing k-gram returns empty dict."""
        result = get_next_token_options(("hello", "world"), self.model)
        self.assertEqual(result, {})


class TestFileErrors(unittest.TestCase):
    """Tests for the read_text function."""

    def test_file_not_found(self):
        """Verify that missing file raises FileNotFoundError."""
        with self.assertRaises(FileNotFoundError):
            read_text("nonexistent_file.txt")

    def test_valid_file(self):
        """Verify that valid file returns string content."""
        result = read_text("sample_text.txt")
        self.assertIsInstance(result, str)


class TestInvalidInputs(unittest.TestCase):
    """Tests for invalid inputs across all functions."""

    def setUp(self):
        """Set up a simple text for testing."""
        self.text = "1\nthe bird sings.\n\n2\nthe bird flies.\n"

    def test_invalid_k_zero(self):
        """Verify that k=0 raises ValueError."""
        with self.assertRaises(ValueError):
            build_kgram_model(self.text, 0)

    def test_invalid_k_negative(self):
        """Verify that negative k raises ValueError."""
        with self.assertRaises(ValueError):
            build_kgram_model(self.text, -1)

    def test_invalid_k_type(self):
        """Verify that non-integer k raises TypeError."""
        with self.assertRaises(TypeError):
            build_kgram_model(self.text, 2.5)

    def test_invalid_k_bool(self):
        """Verify that bool k raises TypeError."""
        with self.assertRaises(TypeError):
            build_kgram_model(self.text, False)

    def test_invalid_text_type(self):
        """Verify that non-string text raises TypeError."""
        with self.assertRaises(TypeError):
            build_kgram_model([], 2)

    def test_text_too_short_raises_value_error(self):
        """Verify that text too short to produce k-grams raises ValueError."""
        with self.assertRaises(ValueError):
            build_kgram_model(self.text, 1000)


if __name__ == "__main__":
    unittest.main()