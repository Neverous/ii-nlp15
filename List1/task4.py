#!/bin/env python3
import grams
import itertools
import random

WINDOW = 2
words, words_index, words_position, connections, connections_index = grams.load_grams('../{}grams'.format(WINDOW), WINDOW)

def upper_bound(val, arr, s=0, e=None, key=lambda x: x):
    if e is None:
        e = len(arr)

    while s < e:
        mid = (s + e) // 2
        if val >= key(arr[mid]):
            s = mid + 1

        else:
            e = mid

    return s

def find_ngram(ngram):
    s = 0
    e = len(connections_index)
    for i, word in enumerate(ngram):
        word_id = words_index[upper_bound(word, words_index, key=lambda idx: words[idx]) - 1]
        if words[word_id] != word:
            return 0

        word_position = words_position[word_id]
        s = upper_bound(word_position - 1, connections_index, s, e, key=lambda idx: words_position[connections[i+1][idx]])
        if connections[i+1][connections_index[s]] != word_id:
            return 0

        e = upper_bound(word_position, connections_index, s, e, key=lambda idx: words_position[connections[i+1][idx]])

    return connections[0][s]

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
    for word in words:
        if word.endswith(match):
            yield from process_sentence(sentence, done + [word])

if __name__ == '__main__':
    while True:
        sentence = input('').lower().split()
        print(' '.join(sentence), end=' ')
        result = [0 for _ in range(len(sentence) - WINDOW + 1)]
        for pos in range(len(sentence) - WINDOW + 1):
            for perm in process_sentence(sentence[pos:pos + WINDOW]):
                result[pos] += find_ngram(perm)

        print(' '.join(map(str, result)))
