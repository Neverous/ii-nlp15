import random

def gen_gender():
    return random.choice(('f', 'm1', 'm2', 'm3', 'n1', 'n2'))

def gen_form():
    return random.choice(('pl', 'sg'))

def gen_subject(gender=None, form=None):
    if gender is None:
        gender = gen_gender()

    if form is None:
        form = gen_form()

    if random.randint(0, 3):
        yield 'adj:' + form + ':nom:' + gender + ':pos'

    yield 'subst:' + form + ':nom:' + gender

def gen_object(gender=None, form=None):
    if gender is None:
        gender = gen_gender()

    if form is None:
        form = gen_form()

    if random.randint(0, 3):
        yield 'adj:' + form + ':nom:' + gender + ':pos'

    yield 'subst:' + form + ':acc:' + gender
    yield 'subst:' + form + ':gen:' + gender

def gen_verb(form=None):
    if form is None:
        form = gen_form()

    perf = random.choice(('perf', 'imperf'))
    yield 'fin:' + form + ':ter:' + perf

if __name__ == '__main__':
    form = gen_form()
    print(' '.join(tuple(gen_subject(form=form)) + tuple(gen_verb(form=form)) + tuple(gen_object())))
