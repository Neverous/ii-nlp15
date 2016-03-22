import grams
import math
import multiprocessing
import os
import pickle
import random
import sys
import tokenizer

ALPHABET = 'abcdefghijklmnopqrstuwvxyz'
ALPHA = 0.1

def save_dictionary(dictionary, filename):
    with open(filename, 'wb') as _file:
        pickle.dump(dictionary, _file)

def load_dictionary(filename):
    with open(filename, 'rb') as _file:
        return pickle.load(_file)

def generate_dictionary(input_filename, output_filename=None):
    if output_filename is None:
        input_file, input_ext = os.path.splitext(input_filename)
        output_filename = input_file + '.dat'

    dictionary = {}
    with open(input_filename, 'r') as _file:
        for word in _file:
            word = word.strip()
            normalized = tokenizer.normalize(word)
            if normalized not in dictionary:
                dictionary[normalized] = []

            dictionary[normalized].append(word)

    #print('Dictionary size: {}'.format(len(dictionary)))
    save_dictionary(dictionary, output_filename)

def unigram_score(word, unigrams):
    c = grams.find_ngram([word], *unigrams[0])
    if not c:
        return -1000000000

    return math.log2(c / unigrams[1])

def bigram_score(w1, w2, unigrams, bigrams):
    c1 = grams.find_ngram([w1], *unigrams[0])
    c2 = grams.find_ngram([w2], *unigrams[0])
    c12 = grams.find_ngram([w1, w2], *bigrams[0])
    if not c12:
        if not c2:
            return -1000000000

        return math.log2(ALPHA * c2 / unigrams[1])

    return math.log2((1 - ALPHA) * c12 / c1)

def fix_typos(sentence, dictionary, unigrams, bigrams):
    result          = []
    possibilities   = []
    for word in sentence.split():
        possibilities.append(possible_replacements(word, dictionary))

    #print(possibilities)
    costs = [{}]
    prev = [{}]
    for word in possibilities[0]:
        costs[0][word] = unigram_score(word, unigrams)

    for i in range(1, len(possibilities)):
        costs.append({})
        prev.append({})
        for w2 in possibilities[i]:
            candidates = [ (costs[i - 1][w1] + bigram_score(w1, w2, unigrams, bigrams), w1) for w1 in possibilities[i - 1]]
            cost, word = max(candidates)
            costs[-1][w2] = cost
            prev[-1][w2] = word

    cost, last = max([(kv[1], kv[0]) for kv in costs[-1].items()])
    result = [last]
    for i in range(len(possibilities) - 1, 0, -1):
        result.append(prev[i][result[-1]])

    return ' '.join(reversed(result))

def possible_replacements(word, dictionary):
    replacements = set([word])
    normalized = tokenizer.normalize(word)
    for (change, dist) in generate_typos(normalized, 1):
        if len(change) <= 2 and dist > 0:
            continue

        if change in dictionary:
            for replacement in dictionary[change]:
                replacements.add(replacement)

    return list(replacements)

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
        for letter in ALPHABET:
            if letter != word[pos]:
                yield from generate_typos(word[:pos] + letter + word[pos + 1:], distance, d + 1)

    # swap letters
    for pos in range(len(word) - 1):
        yield from generate_typos(word[:pos] + word[pos + 1] + word[pos] + word[pos + 2:], distance, d + 1)

def fix_line(line):
    return fix_typos(line.strip(), dictionary, unigrams, bigrams)

if __name__ == '__main__':
    #generate_dictionary('../slownik_do_literowek.txt')
    dictionary = load_dictionary('../slownik_do_literowek.dat')
    unigrams = [grams.load_grams('../1grams_min_cleaned', 1)]
    bigrams = [grams.load_grams('../2grams_min_cleaned', 2)]
    unigrams.append(sum(unigrams[0][3][0]))
    bigrams.append(sum(bigrams[0][3][0]))
    print('Loaded!')

    pool = multiprocessing.Pool()

    print('\n'.join(pool.map(fix_line, sys.stdin)))
