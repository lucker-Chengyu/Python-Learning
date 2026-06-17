import random
from abc import ABC, abstractmethod
from kgram import build_kgram_model, get_next_token_options


class TextGenerator(ABC):
    """Abstract base class for text generators."""

    def __init__(self, text, k):
        """
        Initialises the TextGenerator with raw text and k-gram size.

        Args:
            text (str): The raw text to build the model from.
            k (int): The size of the k-gram.
        """
        # store raw text and k for rebuilding model later
        self.text = text
        self.k = k
        # build the k-gram model from the text
        self.model = build_kgram_model(text, k)

    def get_next_options(self, kgram):
        """
        Returns the next token options for a given k-gram.

        Args:
            kgram (tuple): A tuple of k tokens.

        Returns:
            dict: A dictionary of next tokens and their counts.
        """
        # look up the k-gram in the model
        return get_next_token_options(kgram, self.model)

    @abstractmethod
    def choose_next_token(self, options):
        """
        Chooses the next token from the given options.

        Args:
            options (dict): A dictionary of next tokens and their counts.

        Returns:
            str: The chosen next token.
        """
        pass

    def _generate_recursive(self, kgram, max_tokens, current_tokens):
        """
        Recursively generates a list of tokens.

        Args:
            kgram (tuple): The current k-gram to look up.
            max_tokens (int): The maximum number of tokens to generate.
            current_tokens (list): The tokens generated so far.

        Returns:
            list: The list of generated tokens.
        """
        # stop if max tokens reached
        if len(current_tokens) >= max_tokens:
            return current_tokens

        # get next token options
        options = self.get_next_options(kgram)

        # stop if no options available
        if not options:
            return current_tokens

        # choose next token
        next_token = self.choose_next_token(options)

        # stop if <END> is chosen
        if next_token == "<END>":
            return current_tokens

        # add chosen token to list
        current_tokens.append(next_token)

        # create new k-gram by sliding window forward
        new_kgram = tuple(list(kgram[1:]) + [next_token])

        # recursively generate next token
        return self._generate_recursive(new_kgram, max_tokens, current_tokens)

    def generate(self, start_kgram, max_tokens):
        """
        Generates text starting from the given k-gram.

        Args:
            start_kgram (tuple): The starting k-gram.
            max_tokens (int): The maximum number of tokens to generate.

        Returns:
            str: The generated text.
        """
        # validate start_kgram is a tuple first before checking length
        if not isinstance(start_kgram, tuple):
            raise ValueError("start_kgram must be a tuple")
        # validate start_kgram length matches k
        if len(start_kgram) != self.k:
            raise ValueError("start_kgram must be a tuple of length k")
        # validate max_tokens is at least k
        if max_tokens < self.k:
            raise ValueError("max_tokens must be at least k")
        # validate start_kgram exists in model
        if start_kgram not in self.model:
            raise ValueError("start_kgram not found in model")

        # start with the tokens from start_kgram
        tokens = list(start_kgram)

        # recursively generate remaining tokens
        tokens = self._generate_recursive(start_kgram, max_tokens, tokens)

        # format and return the generated text
        return self._format_output(tokens)

    def _format_output(self, tokens):
        """
        Formats a list of tokens into a readable string.

        Args:
            tokens (list): The list of tokens to format.

        Returns:
            str: The formatted text.
        """
        if not tokens:
            return ""

        # capitalise the first word
        result = [tokens[0].capitalize()]

        for i in range(1, len(tokens)):
            token = tokens[i]
            if token in [",", "."]:
                # remove space before punctuation
                result.append(token)
            elif tokens[i - 1] == ".":
                # capitalise word after period
                result.append(token.capitalize())
            else:
                result.append(token)

        # join tokens with spaces then fix punctuation spacing
        text = " ".join(result)
        text = text.replace(" ,", ",")
        text = text.replace(" .", ".")

        # remove any trailing <END> token
        text = text.replace("<END>", "").strip()

        return text

    def rebuild_model(self, text):
        """
        Rebuilds the k-gram model using new text.

        Args:
            text (str): The new text to build the model from.
        """
        # update stored text and rebuild model
        self.text = text
        self.model = build_kgram_model(text, self.k)

    def update_k(self, k):
        """
        Updates the k value and rebuilds the model.

        Args:
            k (int): The new k value.
        """
        # update k and rebuild model with existing text
        self.k = k
        self.model = build_kgram_model(self.text, self.k)

    def add_poem(self, poem):
        """
        Adds a new poem to the text and rebuilds the model.

        Args:
            poem (str): The new poem to add.
        """
        # append poem with newline separator and rebuild
        self.text = self.text + "\n" + poem
        self.model = build_kgram_model(self.text, self.k)


class DeterministicGenerator(TextGenerator):
    """Generates text by always choosing the most frequent next token."""

    def choose_next_token(self, options):
        """
        Chooses the next token with the highest frequency.
        Ties are broken alphabetically.

        Args:
            options (dict): A dictionary of next tokens and their counts.

        Returns:
            str: The token with the highest count.
        """
        # sort by count descending, then alphabetically for tie-breaking
        return min(options.keys(), key=lambda t: (-options[t], t))


class RandomGenerator(TextGenerator):
    """Generates text by randomly choosing the next token weighted by frequency."""

    def choose_next_token(self, options):
        """
        Chooses the next token randomly, weighted by frequency.

        Args:
            options (dict): A dictionary of next tokens and their counts.

        Returns:
            str: A randomly chosen token.
        """
        # get tokens and their counts as weights
        tokens = list(options.keys())
        weights = list(options.values())

        # use random.choices for weighted random selection
        return random.choices(tokens, weights=weights, k=1)[0]


class HaikuGenerator(RandomGenerator):
    """Generates haiku poems with a 5-7-5 token structure."""

    def _generate_line(self, start_kgram, target_tokens):
        """
        Generates a single line with the target number of tokens.

        Args:
            start_kgram (tuple): The starting k-gram for this line.
            target_tokens (int): The target token count for the line.

        Returns:
            str: The generated line as a string.
        """
        # account for start_kgram tokens already in the list
        total_tokens = target_tokens + len(start_kgram)

        # generate tokens for this line using recursion
        tokens = list(start_kgram)
        tokens = self._generate_recursive(start_kgram, total_tokens, tokens)

        # clean up tokens by removing punctuation and <END>
        line_tokens = [
            t for t in tokens
            if t not in [",", ".", "<END>"]
        ]

        # capitalise first word
        if line_tokens:
            line_tokens[0] = line_tokens[0].capitalize()

        # strip extra spaces from start and end
        return " ".join(line_tokens).strip()

    def generate_poem(self):
        """
        Generates a haiku poem with 5-7-5 token structure.

        Returns:
            str: A haiku poem as a single string with newlines between lines.
        """
        # pick a new random starting k-gram for each line to ensure variety
        start_kgram1 = random.choice(list(self.model.keys()))
        start_kgram2 = random.choice(list(self.model.keys()))
        start_kgram3 = random.choice(list(self.model.keys()))

        # generate three lines with 5, 7, 5 tokens
        line1 = self._generate_line(start_kgram1, 5)
        line2 = self._generate_line(start_kgram2, 7)
        line3 = self._generate_line(start_kgram3, 5)

        return "\n".join([line1, line2, line3])


class AcrosticPoemGenerator(RandomGenerator):
    """Generates acrostic poems where the first letter of each line spells a keyword."""

    def __init__(self, text, k, keyword):
        """
        Initialises the AcrosticPoemGenerator with a keyword.

        Args:
            text (str): The raw text to build the model from.
            k (int): The size of the k-gram.
            keyword (str): The keyword to spell out in the acrostic.
        """
        # initialise parent class
        super().__init__(text, k)
        # store keyword in lowercase
        self.keyword = keyword.lower()

    def generate_poem(self):
        """
        Generates an acrostic poem where each line starts with a keyword letter.

        Returns:
            str: The acrostic poem as a string with newlines between lines.
        """
        lines = []

        for letter in self.keyword:
            # find k-grams that start with this letter
            matching_kgrams = [
                kgram for kgram in self.model
                if kgram[0].startswith(letter)
            ]

            if matching_kgrams:
                # randomly pick one matching k-gram
                start_kgram = random.choice(matching_kgrams)
            else:
                # fallback message if no match found
                lines.append(f"No match found for '{letter}'")
                continue

            # generate approximately 6 tokens per line
            # account for start_kgram tokens already in the list
            total_tokens = 6 + len(start_kgram)
            tokens = list(start_kgram)
            tokens = self._generate_recursive(start_kgram, total_tokens, tokens)

            # strip leading and trailing punctuation
            line_tokens = [
                t for t in tokens
                if t not in [",", ".", "<END>"]
            ]

            # capitalise first word
            if line_tokens:
                line_tokens[0] = line_tokens[0].capitalize()

            lines.append(" ".join(line_tokens).strip())

        return "\n".join(lines)