from collections import defaultdict
import grams
import random
import re
import sys

WORD    = 1
TAG     = 2

WORDS = {}
WORDS2 = defaultdict(lambda: dict())
TAGS = defaultdict(lambda: list())

grams1 = grams.load_grams('../1grams_min_cleaned', 1)
grams2 = grams.load_grams('../2grams_min_cleaned', 2)
for idx in range(len(grams1[3][0])):
    WORDS[grams1[0][grams1[3][1][idx]]] = grams1[3][0][idx]

for idx in range(len(grams2[3][0])):
    WORDS2[grams2[0][grams2[3][1][idx]]][grams2[0][grams2[3][2][idx]]] = grams2[3][0][idx]

regex = re.compile(r'[^\w ]', re.UNICODE | re.IGNORECASE)
with open('../morfeuszTagsAndBasesForNKJP.txt', 'r') as f:
    for line in f:
        word, base, *tags = line.strip().split()
        word = regex.sub('', word).strip()
        if word not in WORDS:
            continue

        for tag in tags:
            TAGS[tag].append(word)

def parse_structure(structure):
    for description in structure.split():
        if description.startswith('"'):
            yield (WORD, description[1:-1])

        else:
            yield (TAG, description)

def simple_generator(structure):
    for kind, word in parse_structure(structure):
        if kind == WORD:
            yield word

        else:
            yield choose_by_tag(word)

def choose_by_tag(tag):
    full_sum = 0
    for word in TAGS[tag]:
        full_sum += WORDS[word]

    val = random.randint(0, full_sum-1)
    for word in TAGS[tag]:
        if val < WORDS[word]:
            return word

        val -= WORDS[word]

def bigram_generator(structure):
    prev = None
    for kind, word in parse_structure(structure):
        if kind == WORD:
            prev = word
            yield prev

        else:
            next_ = choose_bigram_by_tag(prev, word)
            yield next_
            prev = next_

def choose_bigram_by_tag(prev, tag):
    full_sum = 0
    possible = []
    WORDS = WORDS2[prev]
    for word in TAGS[tag]:
        if word in WORDS:
            full_sum += WORDS[word]
            possible.append(word)

    if not possible:
        return choose_by_tag(tag)

    val = random.randint(0, full_sum-1)
    for word in possible:
        if val < WORDS[word]:
            return word

        val -= WORDS[word]

if __name__ == '__main__':
    print('Loaded!')
    for line in sys.stdin:
        print('S:', ' '.join(simple_generator(line.strip())))
        print('B:', ' '.join(bigram_generator(line.strip())))
