from collections import defaultdict
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

if __name__ == '__main__':
    with open('typos.dat', 'rb') as f:
        data = dict(pickle.load(f))

    rep_typos       = 0
    rep_ab          = defaultdict(lambda: 0)
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
                    break

                else:
                    rep_typos += count
                    rep_ab[(a, b)] += count
                    break

    for (key, value) in sorted(rep_ab.items(), key=lambda x: -x[1]):
        print(''.join(key) + ':', value / rep_typos)

