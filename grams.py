#!/bin/env python3
from array import array
import codecs
import gc
import marshal
import os
import random
import sys
import time

def less_than(x, y):
    return x < y

def merge_array(arr, s, mid, e, cmp=less_than):
    result = array(arr.typecode)
    l = s
    r = mid
    while l < mid and r < e:
        if cmp(arr[l], arr[r]) < 0:
            result.append(arr[l])
            l += 1

        else:
            result.append(arr[r])
            r += 1

    while l < mid:
        result.append(arr[l])
        l += 1

    while r < e:
        result.append(arr[r])
        r += 1

    return result

def mergesort(arr, s=0, e=None, cmp=less_than):
    if e is None:
        e = len(arr)

    if s + 1 >= e:
        return

    mid = (s + e) // 2
    mergesort(arr, s, mid, cmp)
    mergesort(arr, mid, e, cmp)

    arr[s:e] = merge_array(arr, s, mid, e, cmp)
    return arr

def load_grams(filename, n):
    # read cached values
    if os.path.exists(filename + '.dat'):
        with open(filename + '.dat', 'rb') as _file:
            words, words_index, words_position, connections, connections_index = marshal.load(_file)
            words = tuple(map(lambda x: x.decode('utf-8'), words))
            connections = tuple(map(lambda _repr: array('I', _repr), connections))
            words_index         = array('I', words_index)
            words_position      = array('I', words_position)
            connections_index   = array('I', connections_index)
            return (words, words_index, words_position, connections, connections_index)

    # preprocess data
    seen = {}
    words = []
    connections = [array('I') for _ in range(n + 1)]
    with codecs.open(filename, 'rb') as _file:
        for line in _file:
            weight, partial = line.split(maxsplit=1)
            connections[0].append(int(weight))
            for i, word in enumerate(partial.split()):
                try:
                    connections[i + 1].append(seen[word])
                except KeyError:
                    idx = seen[word] = len(seen)
                    words.append(word)
                    connections[i + 1].append(idx)

            if len(connections[0]) % 10000 == 0:
                print('...', len(connections[0]), len(seen))

    del seen
    gc.collect()
    print(' sorting')
    def words_compare(a, b):
        if words[a] < words[b]:
            return -1

        if words[a] == words[b]:
            return 0

        return 1

    def connections_compare(a, b):
        for i in range(1, n + 1):
            if words_position[connections[i][a]] < words_position[connections[i][b]]:
                return -1

            if words_position[connections[i][a]] > words_position[connections[i][b]]:
                return 1

        return 0

    words_index         = array('I', range(len(words)))
    mergesort(words_index, cmp=words_compare)
    words_position      = array('I', range(len(words)))
    i = 0
    while i < len(words):
        words_position[words_index[i]] = i
        i += 1

    print('  words done')
    connections_index   = array('I', range(len(connections[0])))
    mergesort(connections_index, cmp=connections_compare)
    print('  connections done')
    words               = tuple(words)
    connections         = tuple(connections)
    with open(filename + '.dat', 'wb') as _file:
        marshal.dump((words, words_index, words_position, connections, connections_index), _file)

    return (words, words_index, words_position, connections, connections_index)

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

def find_ngram(ngram, words, words_index, words_position, connections, connections_index):
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

    result = connections[0][connections_index[s]]
    return result

if __name__ == '__main__':
    load_grams('1grams', 1)
    print('1grams')
    load_grams('2grams', 2)
    print('2grams')
    load_grams('3grams', 3)
    print('3grams')
    load_grams('4grams', 4)
    print('4grams')
    load_grams('5grams', 5)
    print('5grams')
