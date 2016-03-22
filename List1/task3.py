import itertools

for perm in itertools.permutations(["judyta", "dała", "wczoraj", "Stefanowi", "czekoladki"]):
    print(' '.join(perm))

print('')
for perm in itertools.permutations(["babuleńka", "miała", "dwa", "rogate", "koziołki"]):
    print(' '.join(perm))
