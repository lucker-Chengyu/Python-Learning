

import unittest
from .generator import (DeterministicGenerator, RandomGenerator,
                       HaikuGenerator, AcrosticPoemGenerator)


class TestGeneratorLogic(unittest.TestCase):
    """Tests for basic generator functionality."""

    def setUp(self):
        """Set up a simple text for testing."""
        self.text = "1\nthe bird sings.\n\n2\nthe bird flies.\n\n3\nthe moon shines.\n"
        self.generator = DeterministicGenerator(self.text, 2)

    def test_generator_produces_text(self):
        """Verify that generator produces a non-empty string."""
        result = self.generator.generate(("the", "bird"), 20)
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

    def test_output_starts_with_capital(self):
        """Verify that output starts with a capital letter."""
        result = self.generator.generate(("the", "bird"), 20)
        self.assertTrue(result[0].isupper())

    def test_no_end_token_in_output(self):
        """Verify that <END> token does not appear in output."""
        result = self.generator.generate(("the", "bird"), 20)
        self.assertNotIn("<END>", result)

    def test_invalid_start_kgram(self):
        """Verify that invalid start_kgram raises ValueError."""
        with self.assertRaises(ValueError):
            self.generator.generate(("hello", "world"), 20)

    def test_invalid_max_tokens(self):
        """Verify that max_tokens less than k raises ValueError."""
        with self.assertRaises(ValueError):
            self.generator.generate(("the", "bird"), 1)


class TestSubclassBehaviour(unittest.TestCase):
    """Tests for deterministic and random generator behaviour."""

    def setUp(self):
        """Set up text and generators for testing."""
        self.text = "1\nthe bird sings.\n\n2\nthe bird flies.\n\n3\nthe moon shines.\n"
        self.det_gen = DeterministicGenerator(self.text, 2)
        self.rand_gen = RandomGenerator(self.text, 2)

    def test_deterministic_same_output(self):
        """Verify that deterministic generator produces same output each time."""
        result1 = self.det_gen.generate(("the", "bird"), 20)
        result2 = self.det_gen.generate(("the", "bird"), 20)
        self.assertEqual(result1, result2)

    def test_random_is_string(self):
        """Verify that random generator produces a string."""
        result = self.rand_gen.generate(("the", "bird"), 20)
        self.assertIsInstance(result, str)

    def test_deterministic_tie_breaking(self):
        """Verify that deterministic generator breaks ties alphabetically."""
        # "moon" comes before "stars" alphabetically
        options = {"stars": 2, "moon": 2}
        chosen = self.det_gen.choose_next_token(options)
        self.assertEqual(chosen, "moon")

    def test_random_generator_is_random(self):
        """Verify that random generator can produce different outputs."""
        results = set()
        for _ in range(20):
            result = self.rand_gen.generate(("the", "bird"), 20)
            results.add(result)
        # should produce at least 2 different results over 20 tries
        self.assertGreater(len(results), 1)


class TestSpecialisedPoems(unittest.TestCase):
    """Tests for haiku and acrostic poem generators."""

    def setUp(self):
        """Set up text for testing."""
        self.text = "1\nthe bird sings.\n\n2\nthe bird flies.\n\n3\nthe moon shines.\n"

    def test_haiku_produces_three_lines(self):
        """Verify that haiku generator produces three lines."""
        gen = HaikuGenerator(self.text, 2)
        poem = gen.generate_poem()
        lines = poem.split("\n")
        self.assertEqual(len(lines), 3)

    def test_haiku_is_string(self):
        """Verify that haiku generator produces a string."""
        gen = HaikuGenerator(self.text, 2)
        poem = gen.generate_poem()
        self.assertIsInstance(poem, str)

    def test_acrostic_correct_line_count(self):
        """Verify that acrostic poem has correct number of lines."""
        keyword = "the"
        gen = AcrosticPoemGenerator(self.text, 2, keyword)
        poem = gen.generate_poem()
        lines = poem.split("\n")
        # number of lines should match keyword length
        self.assertEqual(len(lines), len(keyword))

    def test_acrostic_is_string(self):
        """Verify that acrostic generator produces a string."""
        gen = AcrosticPoemGenerator(self.text, 2, "the")
        poem = gen.generate_poem()
        self.assertIsInstance(poem, str)


class TestFormattingAndCleanup(unittest.TestCase):
    """Tests for text formatting and cleanup."""

    def setUp(self):
        """Set up generator for testing."""
        self.text = "1\nthe bird sings.\n\n2\nthe bird flies.\n\n3\nthe moon shines.\n"
        self.gen = DeterministicGenerator(self.text, 2)

    def test_no_end_token_in_output(self):
        """Verify that <END> token is not in the output."""
        result = self.gen.generate(("the", "bird"), 20)
        self.assertNotIn("<END>", result)

    def test_no_space_before_punctuation(self):
        """Verify that there is no space before punctuation."""
        result = self.gen.generate(("the", "bird"), 20)
        self.assertNotIn(" ,", result)
        self.assertNotIn(" .", result)

    def test_first_word_capitalised(self):
        """Verify that the first word is capitalised."""
        result = self.gen.generate(("the", "bird"), 20)
        self.assertTrue(result[0].isupper())


class TestDynamicUpdates(unittest.TestCase):
    """Tests for rebuild_model, update_k and add_poem functionality."""

    def setUp(self):
        """Set up generator for testing."""
        self.text = "1\nthe bird sings.\n\n2\nthe bird flies.\n"
        self.gen = DeterministicGenerator(self.text, 2)

    def test_rebuild_model(self):
        """Verify that rebuild_model updates the model."""
        new_text = "1\nthe moon shines.\n"
        self.gen.rebuild_model(new_text)
        # old k-gram should no longer be in model
        options = self.gen.get_next_options(("the", "bird"))
        self.assertEqual(options, {})

    def test_add_poem_updates_model(self):
        """Verify that add_poem adds new tokens to the model."""
        self.gen.add_poem("14\nthe stars shine bright.\n")
        # new k-gram should now be in model
        options = self.gen.get_next_options(("stars", "shine"))
        self.assertNotEqual(options, {})

    def test_update_k(self):
        """Verify that update_k changes k and rebuilds the model."""
        self.gen.update_k(1)
        # k should be updated
        self.assertEqual(self.gen.k, 1)
        # model should now contain 1-grams
        options = self.gen.get_next_options(("the",))
        self.assertNotEqual(options, {})


class TestInvalidInputs(unittest.TestCase):
    """Tests for invalid input handling."""

    def setUp(self):
        """Set up text for testing."""
        self.text = "1\nthe bird sings.\n\n2\nthe bird flies.\n"

    def test_invalid_k_type(self):
        """Verify that non-integer k raises TypeError."""
        with self.assertRaises(TypeError):
            DeterministicGenerator(self.text, "2")

    def test_invalid_k_zero(self):
        """Verify that k=0 raises ValueError."""
        with self.assertRaises(ValueError):
            DeterministicGenerator(self.text, 0)

    def test_invalid_k_negative(self):
        """Verify that negative k raises ValueError."""
        with self.assertRaises(ValueError):
            DeterministicGenerator(self.text, -1)

    def test_invalid_text_type(self):
        """Verify that non-string text raises TypeError."""
        with self.assertRaises(TypeError):
            DeterministicGenerator(123, 2)

    def test_invalid_start_kgram_type(self):
        """Verify that non-tuple start_kgram raises ValueError."""
        gen = DeterministicGenerator(self.text, 2)
        with self.assertRaises(ValueError):
            gen.generate(["the", "bird"], 20)

    def test_invalid_start_kgram_not_in_model(self):
        """Verify that start_kgram not in model raises ValueError."""
        gen = DeterministicGenerator(self.text, 2)
        with self.assertRaises(ValueError):
            gen.generate(("hello", "world"), 20)


if __name__ == "__main__":
    unittest.main()