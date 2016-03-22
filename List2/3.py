import grams
import multiprocessing
import pickle

ALPHABET = 'aąbcćdeęfghijklłmnńoópqrsśtuwvxyzźż'
KEYBOARD = (
    'qwertyuiop',
    'asdfghjkl',
    'zxcvbnm',
)
ALT = {
    'a': 'ą',
    'c': 'ć',
    'e': 'ę',
    'l': 'ł',
    'n': 'ń',
    'o': 'ó',
    's': 'ś',
    'z': 'ż',
    'x': 'ź',
}

REVALT = {d[1]: d[0] for d in ALT.items()}

DICTIONARY = set()
with open('../slownik_do_literowek.txt', 'r') as f:
    for word in f:
        DICTIONARY.add(word.strip())

DIST = 1

def possible_typos(word):
    if word not in DICTIONARY:
        return ('', [])

    result = (word, [])
    for typo, _ in generate_typos(word, 1):
        if typo not in DICTIONARY: continue
        cnt1 = grams.find_ngram([word], *grams1)
        cnt2 = grams.find_ngram([typo], *grams1)
        if cnt2 <= cnt1:
            result[1].append((typo, cnt2))

    result = (result[0], tuple(sorted(set(result[1]), key=lambda x: -x[1])))
    if len(result[1]) < 2:
        return ('', [])

    return result

def generate_letter_typos(letter):
    if letter in ALT:
        yield ALT[letter]

    if letter in REVALT:
        yield REVALT[letter]

    H = -1
    W = -1
    while W < 0 and H < 2:
        H += 1
        W = KEYBOARD[H].find(letter)

    if W < 0:
        return

    assert H >= 0 and W >= 0

    for h in range(max(0, H - DIST), min(len(KEYBOARD), H + DIST + 1)):
        for w in range(max(0, W - DIST), min(len(KEYBOARD), W + DIST + 1)):
            letter = KEYBOARD[h][w]
            yield letter
            if letter in ALT:
                yield ALT[letter]

            if letter in REVALT:
                yield REVALT[letter]

def generate_typos(word, distance, d=0):
    yield (word, d)
    if d == distance:
        return

    # add letter
    for pos in range(len(word)):
        for letter in ALPHABET:
            yield from generate_typos(word[:pos] + letter + word[pos:], distance, d + 1)

    # remove letter
    for pos in range(len(word)):
        yield from generate_typos(word[:pos] + word[pos + 1:], distance, d + 1)

    # change letter
    for pos in range(len(word)):
        for letter in generate_letter_typos(word[pos]):
            yield from generate_typos(word[:pos] + letter + word[pos + 1:], distance, d + 1)

    # swap letters
    for pos in range(len(word) - 1):
        yield from generate_typos(word[:pos] + word[pos + 1] + word[pos] + word[pos + 2:], distance, d + 1)

if __name__ == '__main__':
    grams1 = grams.load_grams('../1grams_cleaned', 1)
    pool = multiprocessing.Pool()
    data = pool.map(possible_typos, grams1[0])
    with open('typos.dat', 'wb') as f:
        pickle.dump(data, f)
