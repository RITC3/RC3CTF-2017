from random import shuffle, choice

with open("values.txt") as f:
    vals = [int(v, 16) for v in f.readlines()]

lines = []

vz = zip(vals, range(len(vals)))
shuffle(vz)
u = []

acc = 0
for v in vz:
    if v[0] == 0:
        continue
    if len(u)==0:
        lines.append("    ptr[{}] = {};".format(v[1], v[0]))
    else:
        d = 0
        while d == 0:
            c = choice(u)
            d = v[0] ^ c[0]
        lines.append("    ptr[{}] = {} ^ ptr[{}];".format(v[1], d, c[1]))
    u.append(v)

for i in lines:
    print i
