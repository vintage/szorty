import string


AVAILABLE_CHARS = string.lowercase + string.digits


def get_words():
    with open('static/words.txt') as words:
        for word in words:
            yield word


def format_word(word):
    return ''.join([
        c for c in word.lower() if c in AVAILABLE_CHARS
    ])


unique_words = set()
for word in get_words():
    word = format_word(word)
    unique_words.add(word)

print(unique_words)