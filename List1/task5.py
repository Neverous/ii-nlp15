#!/bin/env python3
import grams
import itertools
import math
import random

WINDOW = 2
words, words_index, words_position, connections, connections_index = grams.load_grams('../{}grams'.format(WINDOW), WINDOW)

cache = {}
def process_sentence(sentence, done=None):
    if done is None:
        done = []

    if not sentence:
        yield done
        return

    for i in range(len(sentence)):
        if sentence[i].startswith('-'):
            break

        done.append(sentence[i])

    else:
        yield done
        return

    match = sentence[i][1:]
    sentence = sentence[i + 1:]
    if not match in cache:
        cache[match] = []
        for word in words:
            if word.endswith(match):
                cache[match].append(word)

    for word in cache[match]:
        yield from process_sentence(sentence, done + [word])

if __name__ == '__main__':
    while True:
        sentence = input('').lower().split()
        result = 0
        for pos in range(len(sentence) - WINDOW + 1):
            res = 0
            count = 0
            for perm in process_sentence(sentence[pos:pos + WINDOW]):
                count += 1
                res -= math.log(grams.find_ngram(perm, words_index, words, words_position, connections_index, connections) + 1) - math.log(grams.find_ngram(perm[:1], words_index, words, words_position, connections_index, connections) + len(words))

            result += res / count

        print(int(result * 1000000), ' '.join(sentence))
