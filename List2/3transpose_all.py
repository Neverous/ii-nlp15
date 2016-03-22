from collections import defaultdict
import grams
import pickle

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

if __name__ == '__main__':
    with open('typos.dat', 'rb') as f:
        data = dict(pickle.load(f))

    trans_ab        = defaultdict(lambda: 0)
    for word, typos in data.items():
        if not typos: continue
        for typo, count in typos:
            if typo == word:
                continue

            if len(typo) != len(word):
                continue

            for i in range(len(word)):
                a = word[i]
                b = typo[i]
                if a == b:
                    continue

                if a in ALT and ALT[a] == b:
                    break

                elif a in REVALT and REVALT[a] == b:
                    break

                elif i + 1 < len(word) and (a, word[i+1]) == (typo[i+1], b):
                    trans_ab[(a, b)] += count
                    break

                else:
                    break

    grams1 = grams.load_grams('../1grams_cleaned', 1)
    paired = defaultdict(lambda: 0)
    for word in grams1[0]:
        if word not in DICTIONARY:
            continue

        count = grams.find_ngram([word], *grams1)
        for i in range(len(word)):
            if i + 1 < len(word):
                paired[(word[i], word[i+1])] += count

    for (key, value) in trans_ab.items():
        trans_ab[key] = value / (value + paired[key])

    for (key, value) in sorted(trans_ab.items(), key=lambda x: -x[1]):
        print(''.join(key) + ':', value)
