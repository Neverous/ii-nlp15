#!/bin/env python3
import grams
import random
import sys

words, words_index, words_position, connections, connections_index = grams.load_grams('../2grams', 2)

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

def choose_simple(i, s, e):
    if s == e:
        return None

    cid = connections_index[random.randint(s, e - 1)]
    wid = connections[i+1][cid]
    return wid

def choose_ranked(i, s, e):
    if s == e:
        return None

    full = 0
    for c in range(s, e):
        full += connections[0][connections_index[c]]

    val = random.randint(0, full - 1)
    for c in range(s, e):
        cid = connections_index[c]
        if val < connections[0][cid]:
            return connections[i+1][cid]

        val -= connections[0][cid]

    return None

def generate_next_word(history, choice_fn):
    s = 0
    e = len(connections_index)
    for i, word_id in enumerate(history):
        word_position = words_position[word_id]
        s = upper_bound(word_position - 1, connections_index, s, e, key=lambda idx: words_position[connections[i+1][idx]])
        if connections[i+1][connections_index[s]] != word_id:
            return None

        e = upper_bound(word_position, connections_index, s, e, key=lambda idx: words_position[connections[i+1][idx]])

    return choice_fn(len(history), s, e)

def generate_sentence(history_size=0, choice_fn=choose_simple):
    history_size = min(history_size, len(connections) - 1)
    history = []
    next_word_id = generate_next_word(history, choice_fn)
    while next_word_id is not None:
        print(words[next_word_id], end=' ')
        history.append(next_word_id)
        if len(history) >= history_size:
            history = history[1:]

        sys.stdout.flush()
        next_word_id = generate_next_word(history, choice_fn)

    print('')

if __name__ == '__main__':
    while True:
        generate_sentence(5, choose_simple)
        while True:
            opt = input('Next sentence? [y/n] ').lower()
            if opt == 'y':
                break

            elif opt == 'n':
                sys.exit(0)

