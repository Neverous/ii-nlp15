import pickle

ALT = {
    'a': 'ą',
    'c': 'ć',
    'e': 'ę',
    'l': 'ł',
    'n': 'ń',
    'o': 'ó',
    's': 'ś',
    'z': 'ż',
    'x': 'ź',
}

REVALT = {d[1]: d[0] for d in ALT.items()}

if __name__ == '__main__':
    with open('typos.dat', 'rb') as f:
        data = dict(pickle.load(f))

    alt_minus_typos = 0
    alt_plus_typos  = 0
    count_typos     = 0
    del_typos       = 0
    ins_typos       = 0
    rep_typos       = 0
    trans_typos     = 0
    for word, typos in data.items():
        if not typos: continue
        for typo, count in typos:
            if typo == word:
                continue

            count_typos += count
            if len(typo) < len(word):
                del_typos += count

            elif len(typo) > len(word):
                ins_typos += count

            else:
                for i in range(len(word)):
                    a = word[i]
                    b = typo[i]
                    if a == b:
                        continue

                    if a in ALT and ALT[a] == b:
                        alt_plus_typos += count
                        break

                    elif a in REVALT and REVALT[a] == b:
                        alt_minus_typos += count
                        break

                    elif i + 1 < len(word) and (a, word[i+1]) == (typo[i+1], b):
                        trans_typos += count
                        break

                    else:
                        rep_typos += count
                        break

    print(  'ins:',     str(ins_typos/count_typos),
            'del:',     str(del_typos/count_typos),
            'trans:',   str(trans_typos/count_typos),
            'rep:',     str(rep_typos/count_typos),
            'alt+',     str(alt_plus_typos/count_typos),
            'alt-',     str(alt_minus_typos/count_typos))
