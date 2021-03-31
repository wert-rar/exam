min_ = 0
big_range = 1000000

L_end = 2
M_end = 6
minimum = False


def prog(x):
    a, b = 0, 1
    while x > 0:
        if x % 2 > 0:
            a += 1
        else:
            b += x % 5
        x = x // 5
    return a, b


# Find minimum number that pass condition
for i in range(0, big_range):
    L, M = prog(i)

    if L == L_end and M == M_end:
        min_ = i
        break

if minimum:
    print(min_)
else:
    # Find maximum number that pass condition
    for i in range(min_ + 1, big_range):
        L, M = prog(i)
        if L == L_end and M == M_end:
            min_ = i
            print(min_)
