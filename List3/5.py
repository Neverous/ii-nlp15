import sys
BASES = {}
RULES = {}
with open('../morfeuszTagsAndBasesForNKJP.txt') as f:
    for line in f:
        word, base, *_ = line.strip().lower().split(maxsplit=2)
        base = base.split(':')[0]
        if word not in BASES:
            BASES[word] = set()

        BASES[word].add(base)

with open('rules.txt') as f:
    for line in f:
        basesuf, *rules = line.strip()[1:].split()
        parsed = []
        for rule in rules:
            subst, weight = rule[2:-1].split(',')
            weight = float(weight)
            parsed.append((subst, weight))

        RULES[basesuf] = tuple(parsed)

if __name__ == '__main__':
    print('Loaded!', file=sys.stderr)
    for line in sys.stdin:
        words = line.strip().split()
        for word in words:
            print(word, '-', end=' ')
            if word in BASES:
                print(' '.join('{0} {1:.5f}'.format(base, 1/len(BASES[word])) for base in BASES[word]))

            else:
                for preflen in range(0, len(word)):
                    if word[preflen:] in RULES:
                        print(' '.join('{0}{1} {2:.5f}'.format(word[:preflen], subst, weight) for subst, weight in RULES[word[preflen:]]))
                        break
