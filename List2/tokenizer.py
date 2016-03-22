import re
import unicodedata

TOKEN_WHITESPACES       = 0
TOKEN_WORD              = 1
TOKEN_SPECIAL_CHARS     = 2
TOKEN_END_OF_SENTENCE   = 3

def last_token_is(tokens, TOKEN):
    return tokens and tokens[-1][0] == TOKEN

def merge_same_last_tokens(tokens, TOKEN, value):
    if last_token_is(tokens, TOKEN):
        tokens[-1] = (TOKEN, tokens[-1][1] + value)

    else:
        tokens.append((TOKEN, value))

def normalize(word):
    word = word.lower()
    CHARMAP = ''.maketrans('ąćęłńóśżź', 'acelnoszz')
    word = word.translate(CHARMAP)
    phase1 = unicodedata.normalize('NFKD', word)
    result = phase1.encode('ascii', 'ignore').decode('utf-8')
    return result

def tokenize(line):
    tokens = []
    for letter in line:
        if re.match('\w+', letter, re.UNICODE):
            merge_same_last_tokens(tokens, TOKEN_WORD, letter)

        elif letter in ('\n', '\r', ' ', '\t'):
            merge_same_last_tokens(tokens, TOKEN_WHITESPACES, letter)

        elif letter in ('.', '!', '?'):
            merge_same_last_tokens(tokens, TOKEN_END_OF_SENTENCE, letter)

        else:
            merge_same_last_tokens(tokens, TOKEN_SPECIAL_CHARS, letter)

    return tokens
