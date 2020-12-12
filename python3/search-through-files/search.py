import os

folder='./'
needles=[
'needle',
'folder',
]

needles = [x.upper() for x in needles]

for filename in os.listdir('./'):
    print("--- File '{}' ---".format(filename))
    with open(filename, 'r') as f:
        i=0
        for line in f.readlines():
            for needle in needles:
                if needle in line.upper():
                    print("    L{}: '{}'".format(i,line.strip()))
            i+=1