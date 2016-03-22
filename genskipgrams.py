import sys
if __name__ == '__main__':
    skip = int(sys.argv[1])
    counter = {}
    for line in sys.stdin:
        count, *words = line.strip().split()
        words = ' '.join(words[::skip+1])
        if words not in counter:
            counter[words] = count

        else:
            counter[words] += count

    for row in sorted(counter.items(), key=lambda x: -x[1]):
        print(row[1], row[0])
