import re


def clean_text(text):
    # Remove HTML tags
    text = re.sub(r"<[^>]*?>", "", text)
    # Remove URLs
    text = re.sub(
        r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\)]|(?:%[0-9a-fA-F]{2}))+",
        "",
        text,
    )
    # Remove non-alphanumeric characters except spaces
    text = re.sub(r"[^a-zA-Z0-9 ]", "", text)
    # Collapse whitespace
    text = re.sub(r"\s{2,}", " ", text)
    # Bug fix: text.split() was called on a list (text was already split on line above)
    # Correct: split once, then join
    text = " ".join(text.split())
    return text