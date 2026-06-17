import re


def read_text(file_path):
    """
    Reads a file and returns its content as a string.

    Args:
        file_path (str): The path to the file to read.

    Returns:
        str: The content of the file as a string.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        # raise ValueError if file contains no text after stripping
        if not content.strip():
            raise ValueError(f"File contains no text: {file_path}")
        return content
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")


def clean_text(text):
    """
    Converts raw text into a list of tokens, with each poem ending in '<END>'.

    Args:
        text (str): The raw text content of the file.

    Returns:
        list: A list of tokens extracted from the text.
    """
    # convert to lowercase for uniform processing
    text = text.lower()
    # split into individual lines for poem boundary detection
    lines = text.split("\n")
    poems = []
    current_poem = []

    for line in lines:
        if line.strip().isdigit():
            # numeric line indicates start of a new poem
            if current_poem:
                # save completed poem before starting a new one
                poems.append(current_poem)
            current_poem = []
        else:
            if line.strip():
                # only add non-empty lines to current poem
                current_poem.append(line.strip())

    # ensure the last poem is included after loop ends
    if current_poem:
        poems.append(current_poem)

    tokens = []
    for poem in poems:
        # merge all lines of a poem into one string
        poem_text = " ".join(poem)
        # make commas and periods into separate tokens
        poem_text = poem_text.replace(",", " , ")
        poem_text = poem_text.replace(".", " . ")
        # split into individual words
        raw_words = poem_text.split()
        processed_words = []

        for word in raw_words:
            if word in [",", "."]:
                # keep commas and periods as standalone tokens
                processed_words.append(word)
            else:
                # remove all punctuation except letters and digits
                # use [a-z0-9] to avoid keeping underscores from \w
                cleaned_word = re.sub(r'[^a-z0-9]', '', word)
                if cleaned_word:
                    # only add non-empty words after cleaning
                    processed_words.append(cleaned_word)

        # mark end of each poem
        processed_words.append("<END>")
        tokens.extend(processed_words)

    # raise ValueError if no valid tokens were produced
    if not tokens:
        raise ValueError("The text cannot produce any valid k-grams.")

    return tokens


def build_kgram_model(text, k):
    """
    Builds a k-gram model from the given text.

    Args:
        text (str): The raw text content to build the model from.
        k (int): The size of the k-gram.

    Returns:
        dict: A dictionary mapping k-gram tuples to dictionaries of next token counts.
    """
    # validate input types, bool is a subclass of int so must be checked separately
    if not isinstance(k, int) or isinstance(k, bool):
        raise TypeError("k must be an integer")
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    # validate k value, k must be greater than 0
    if k <= 0:
        raise ValueError("k must be greater than 0")

    # get token list from clean_text
    tokens = clean_text(text)

    # raise ValueError if text cannot produce any valid k-grams
    if len(tokens) <= k:
        raise ValueError("The text cannot produce any valid k-grams.")

    model = {}

    # slide window of size k across tokens
    for i in range(len(tokens) - k):
        # extract k tokens as the key
        kgram = tuple(tokens[i:i + k])
        # the next token after the k-gram
        next_token = tokens[i + k]

        if kgram not in model:
            # initialise new k-gram entry
            model[kgram] = {}

        if next_token not in model[kgram]:
            # initialise new next token count
            model[kgram][next_token] = 0

        # increment count for this next token
        model[kgram][next_token] += 1

    return model


def get_next_token_options(kgram, model):
    """
    Returns the dictionary of next token options for a given k-gram.

    Args:
        kgram (tuple): A tuple of k tokens to look up in the model.
        model (dict): The k-gram model dictionary.

    Returns:
        dict: A dictionary of next tokens and their counts, or empty dict if not found.
    """
    # return next token options, or empty dict if kgram not in model
    return model.get(kgram, {})