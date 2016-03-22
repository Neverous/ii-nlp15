import pickle

if __name__ == '__main__':
    with open('typos.dat', 'rb') as f:
        data = dict(pickle.load(f))

    for word, typos in data.items():
        print(word+':', end=' ')
        for typo, count in typos:
            print(typo+':'+str(count), end=' ')

        print('')
