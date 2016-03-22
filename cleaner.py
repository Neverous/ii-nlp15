import re
import sys

regex = re.compile(r'[^\w ]', re.UNICODE | re.IGNORECASE)
counter = {}
with open(sys.argv[1], 'r') as _file:
    for line in _file:
        count, ngram = line.split(maxsplit=1)
        processed = regex.sub('', ngram).strip()
        if not processed or len(ngram.split()) != len(processed.split()):
            continue

        if processed not in counter:
            counter[processed] = int(count)
        else:
            counter[processed] += int(count)

with open(sys.argv[1] + '_cleaned', 'w') as _file:
    for ngram in sorted(counter.items(), key=lambda x: -x[1]):
        print(ngram[1], ngram[0], file=_file)
