import multiprocessing
import nltk
import phrases
import bad_phrases3 as bad_phrases
import skladnicaTagsBases

WORDS_GRAMMAR = skladnicaTagsBases.gen_grammar()
with open('rules') as f:
    NP_GRAMMAR = f.read()

FULL_GRAMMAR = NP_GRAMMAR + WORDS_GRAMMAR
nltk_grammar = nltk.grammar.FeatureGrammar.fromstring(FULL_GRAMMAR)
nltk_parser = nltk.FeatureChartParser(nltk_grammar)

def is_np(phrase):
    try:
        if len(phrase) < 7:
            trees = list(nltk_parser.parse(phrase))
            if len(trees):
                return (True, ' '.join(phrase))

    except ValueError:
        pass

    return (False, ' '.join(phrase))

def valid(phrase):
    result, phrase = is_np(phrase)
    if not result:
        return 'PHRASE: ' + phrase + '\n'

    return ''

def invalid(phrase):
    result, phrase = is_np(phrase)
    if result:
        return 'BAD_PHRASE: ' + phrase + '\n'

    return ''

pool = multiprocessing.Pool()

invalid_phrases = ''.join(pool.map(valid, phrases.PHRASES))
invalid_bad_phrases = ''.join(pool.map(invalid, bad_phrases.PHRASES))
print(invalid_phrases)
print(invalid_bad_phrases)
