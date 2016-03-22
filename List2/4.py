import math
import os
import pickle
import random
import sys
import tokenizer

EPS = 0.000000001
DATA_DIR='../dane_pozytywistyczne'

WORDGRAMS_SIZE          = 2
NORMALIZEDGRAMS_SIZE    = 2

WORD_SHARE          = 0.2
NORMALIZED_SHARE    = 0.8

ALFA    = 1
BETA    = 3
GAMMA   = 0
DELTA   = 10000

def main():
    orzeszkowa  = load_model(DATA_DIR + '/korpus_orzeszkowej.dat')
    prus        = load_model(DATA_DIR + '/korpus_prusa.dat')
    sienkiewicz = load_model(DATA_DIR + '/korpus_sienkiewicza.dat')

    #debug_model(orzeszkowa)
    #debug_model(prus)
    #debug_model(sienkiewicz)
    #return

    text = sys.stdin.read()
    results = process_text(text, ((orzeszkowa, 'Orzeszkowa'), (prus, 'Prus'), (sienkiewicz, 'Sienkiewicz')))

    print(' vs. '.join(['{:s} {:.4f}'.format(res[1], res[0]) for res in results]))

def debug_model(model):
    from pprint import pprint
    pprint(tuple(map(lambda kv: (tuple(map(lambda i: model['id2word'][i], kv[0])), kv[1]), tuple(sorted(model['wordgrams'][WORDGRAMS_SIZE-1].items(), key=lambda kv: -kv[1]))[:20])))

def save_model(model, filename):
    with open(filename, 'wb') as _file:
        pickle.dump(model, _file)

def load_model(filename):
    with open(filename, 'rb') as _file:
        return pickle.load(_file)

def generate_model(input_filename, output_filename=None):
    if output_filename is None:
        input_file, input_ext = os.path.splitext(input_filename)
        output_filename = input_file + '.dat'

    model = {
        'id2word':          [],
        'word2id':          {},
        'wordgrams':        [],
        'normalizedgrams':  [],
        'words_count':      0,
        'normalized_count': 0,
        'words_sum':        0,

        'coefficients':     {
            'wordgrams':        [1] * WORDGRAMS_SIZE,
            'normalizedgrams':  [1] * NORMALIZEDGRAMS_SIZE,
        },

        'unknown':          0.0,
    }

    # READ TOKENS
    with open(input_filename, 'r') as _file:
        tokens = tokenizer.tokenize(_file.read())

    print('##', input_filename)
    make_dictionary(tokens, model)
    gather_wordgrams(tokens, model)
    gather_normalizedgrams(tokens, model)
    calculate_unknown(tokens, model)
    calculate_coefficients(model)

    save_model(model, output_filename)

def make_dictionary(tokens, model):
    word2id = model['word2id']
    id2word = model['id2word']
    for (kind, word) in tokens:
        if kind == tokenizer.TOKEN_WORD:
            normalized = tokenizer.normalize(word)
            if word not in word2id:
                word2id[word] = len(id2word)
                id2word.append(word)

            if normalized not in word2id:
                word2id[normalized] = len(id2word)
                id2word.append(normalized)

            model['words_sum'] += 1

    print('# Words: {:d}'.format(len(id2word)))

def gather_grams(source, output):
    for n in range(1, len(source) + 1):
        while len(output) < n:
            output.append({})

        ngram = tuple(source[-n:])
        if ngram not in output[n-1]:
            output[n-1][ngram] = 1

        else:
            output[n-1][ngram] += 1

def gather_wordgrams(tokens, model):
    word2id     = model['word2id']
    wordgrams   = model['wordgrams']
    lastwords   = []
    for (kind, word) in tokens:
        if kind == tokenizer.TOKEN_WORD:
            lastwords.append(word2id[word])
            lastwords = lastwords[-WORDGRAMS_SIZE:]
            gather_grams(lastwords, wordgrams)

    model['words_count'] = len(wordgrams[0])
    print('# Wordgrams: {}'.format(
        tuple(map(lambda dct: len(dct), wordgrams))))

def gather_normalizedgrams(tokens, model):
    word2id         = model['word2id']
    normalizedgrams = model['normalizedgrams']
    lastnormalized  = []
    for (kind, word) in tokens:
        if kind == tokenizer.TOKEN_WORD:
            normalized = tokenizer.normalize(word)
            lastnormalized.append(word2id[normalized])
            lastnormalized = lastnormalized[-NORMALIZEDGRAMS_SIZE:]
            gather_grams(lastnormalized, normalizedgrams)

    model['normalized_count'] = len(normalizedgrams[0])
    print('# Normalizedgrams: {}'.format(
        tuple(map(lambda dct: len(dct), normalizedgrams))))

def calculate_unknown(tokens, model):
    word2id         = model['word2id']
    known_words     = set()
    unknown_words   = []
    unknown_count   = 0
    lastwords       = []
    for (kind, word) in tokens:
        if kind == tokenizer.TOKEN_WORD:
            normalized = tokenizer.normalize(word)
            lastwords.append(word2id[normalized])

        elif kind == tokenizer.TOKEN_END_OF_SENTENCE:
            if random.randint(1, BETA) == 1:
                unknown_words.extend(lastwords)

            else:
                for word in lastwords:
                    known_words.add(word)

            lastwords = []

    for word in unknown_words:
        if word not in known_words:
            unknown_count += 1

    model['unknown'] = unknown_count / len(unknown_words) / DELTA
    print('# Unknown: {:.9f}'.format(model['unknown']))

def calculate_coefficients(model):
    calculate_wordgrams_coefficients(model)
    calculate_normalizedgrams_coefficients(model)

def calculate_wordgrams_coefficients(model):
    word2id         = model['word2id']
    wordgrams       = model['wordgrams']
    coefficients    = model['coefficients']['wordgrams']
    for (ngram, value) in wordgrams[WORDGRAMS_SIZE-1].items():
        winner = choose_best_gram(ngram, wordgrams, model['words_count'])
        coefficients[winner] += value

    coefficients_sum = sum(coefficients)
    for (i, value) in enumerate(coefficients):
        coefficients[i] = value / coefficients_sum

    print('# Wordgrams coefficients: {}'.format(coefficients))

def calculate_normalizedgrams_coefficients(model):
    word2id         = model['word2id']
    normalizedgrams = model['normalizedgrams']
    coefficients    = model['coefficients']['normalizedgrams']
    for (ngram, value) in normalizedgrams[NORMALIZEDGRAMS_SIZE-1].items():
        winner = choose_best_gram(ngram, normalizedgrams, model['normalized_count'])
        coefficients[winner] += value

    coefficients_sum = sum(coefficients)
    for (i, value) in enumerate(coefficients):
        coefficients[i] = value / coefficients_sum

    print('# Normalizedgrams coefficients: {}'.format(coefficients))

def choose_best_gram(source, ngrams, full_count):
    best = [0]
    best_ppb = (ngrams[0].get(tuple(source[-1:]), ALFA) - ALFA) / (full_count - ALFA)
    for n in range(1, len(source)):
        ngram_prev  = tuple(source[-n-1:-1])
        ngram_cur   = tuple(source[-n-1:])
        top     = ngrams[n].get(ngram_cur, ALFA) - ALFA
        bottom  = ngrams[n-1].get(ngram_prev, 0) - ALFA
        if bottom <= 0:
            cur_ppb = 0.0

        else:
            assert top <= bottom
            cur_ppb = top / bottom

        if cur_ppb - best_ppb > EPS:
            best_ppb = cur_ppb
            best = [n]

        elif abs(cur_ppb - best_ppb) < EPS:
            best.append(n)

    return random.choice(best)

def process_text(text, models):
    results = [0] * len(models)
    tokens = tokenizer.tokenize(text)
    lastwords       = []
    lastnormalized  = []
    for (kind, data) in tokens:
        if kind == tokenizer.TOKEN_WORD:
            lastwords.append(data)
            lastnormalized.append(tokenizer.normalize(data))
            lastwords = lastwords[-WORDGRAMS_SIZE:]
            lastnormalized = lastnormalized[-NORMALIZEDGRAMS_SIZE:]
            for score in enumerate(map(lambda mod: count_probabilities(lastwords[-WORDGRAMS_SIZE:], lastnormalized[-NORMALIZEDGRAMS_SIZE:], mod[0]), models)):
                results[score[0]] += WORD_SHARE * score[1][0] + NORMALIZED_SHARE * score[1][1]

        #if kind == tokenizer.TOKEN_END_OF_SENTENCE:
        #    print('Results: {}'.format(results))

    return tuple(reversed(sorted(map(lambda res: (res[1], models[res[0]][1]), enumerate(results)))))

def count_probabilities(words, normalized, model):
    result = [0.0, 0.0]
    if words:
        words = tuple(map(lambda word: model['word2id'].get(word), words))
        result[0] = count_gram_probability(words, model['wordgrams'], model['words_sum'], model['words_count'], model['coefficients']['wordgrams'], model['unknown'])

    if normalized:
        normalized = tuple(map(lambda word: model['word2id'].get(word), normalized))
        result[1] = count_gram_probability(normalized, model['normalizedgrams'], model['words_sum'], model['normalized_count'], model['coefficients']['normalizedgrams'], model['unknown'])

    return result

def count_gram_probability(source, ngrams, grams_sum, words_count, coefficients, unknown):
    ngram = tuple(source[:1])
    ppb = [(ngrams[0][ngram] + GAMMA) / (grams_sum + GAMMA * words_count) if ngram in ngrams[0] else unknown]
    for n in range(1, len(source)):
        ngram_prev = tuple(source[-n-1:-1])
        ngram_cur = tuple(source[-n-1:])
        top = ngrams[n].get(ngram_cur, 0) + GAMMA
        bottom = ngrams[n-1].get(ngram_prev, 0) + GAMMA * words_count
        assert top <= bottom
        if bottom <= 0:
            ppb.append(0.0)
        else:
            ppb.append(top / bottom)

    result = 0.0
    normalize = sum(coefficients[:len(source)])

    for (i, value) in enumerate(ppb):
        result += value * coefficients[i] / normalize

    return math.log2(result)

if __name__ == '__main__':
    #generate_model(DATA_DIR + '/korpus_orzeszkowej.txt')
    #generate_model(DATA_DIR + '/korpus_prusa.txt')
    #generate_model(DATA_DIR + '/korpus_sienkiewicza.txt')
    main()
