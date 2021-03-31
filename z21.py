a_n = 8
big_range = 100000
minimum = False
min_ = 0


def prog(x):
    a = 0
    b = 10
    while x > 5:
        a -= 1
        x -= 1
    return a + b


# Find minimum number that pass condition
for i in range(0, big_range):
    a = prog(i)

    if a == a_n:
        min_ = i
        break

if minimum:
    print(min_)
else:
    # Find maximum number that pass condition
    for i in range(min_ + 1, big_range):
        a = prog(i)
        if a == a_n:
            min_ = i
            print(min_)
