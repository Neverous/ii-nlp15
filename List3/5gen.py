import grams
import sys

WORDS = {}
BASES = {}

grams1 = grams.load_grams('../1grams_cleaned', 1)
for idx in range(len(grams1[3][0])):
    WORDS[grams1[0][grams1[3][1][idx]]] = grams1[3][0][idx]

with open('../morfeuszTagsAndBasesForNKJP.txt') as f:
    for line in f:
        word, base, *_ = line.strip().lower().split(maxsplit=2)
        base = base.split(':')[0]
        if word not in BASES:
            BASES[word] = set()

        BASES[word].add(base)

if __name__ == '__main__':
    print('Loaded!', file=sys.stderr)

    RESULTS = {}
    for word in BASES:
        bases = len(BASES[word])
        for base in BASES[word]:
            if word not in WORDS:
                continue

            weight = WORDS[word]
            preflen = 0
            while preflen < len(word) and preflen < len(base) and word[preflen] == base[preflen]:
                preflen += 1

            preflen = min(preflen, len(base))
            while preflen >= 0 and len(word[preflen:]) <= 4:
                wordsuf = word[preflen:]
                basesuf = base[preflen:]
                #print('-' + wordsuf, '(', '+' + basesuf, weight / bases, ')', word, base)
                if wordsuf not in RESULTS:
                    RESULTS[wordsuf] = {}

                if basesuf not in RESULTS[wordsuf]:
                    RESULTS[wordsuf][basesuf] = weight / bases

                else:
                    RESULTS[wordsuf][basesuf] += weight / bases

                preflen -= 1

    for wordsuf in RESULTS:
        full_sum = 0
        for word, weight in RESULTS[wordsuf].items():
            full_sum += weight

        RESULTS[wordsuf] = tuple(sorted(filter(lambda res: True or res[1] >= 0.00001, map(lambda res: (res[0], res[1] / full_sum), RESULTS[wordsuf].items())), key=lambda x: -x[1]))

    FINAL = {}
    for wordsuf in RESULTS:
        if wordsuf[1:] not in RESULTS or len(RESULTS[wordsuf]) != len(RESULTS[wordsuf[1:]]):
            FINAL[wordsuf] = RESULTS[wordsuf]

    for wordsuf, rules in sorted(FINAL.items()):
        print('-' + wordsuf, ' '.join(('(+{0},{1:.5f})'.format(*rule) for rule in rules)))
