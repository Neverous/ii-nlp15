import itertools

for perm in itertools.permutations(["-yta", "-ała", "-aj", "-owi", "-ki"]):
    print(' '.join(perm))

print('')
for perm in itertools.permutations(["-eńka", "-ała", "-a", "-ate", "-ołki"]):
    print(' '.join(perm))
