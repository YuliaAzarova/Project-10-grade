def bubble_sort_steps(data):
    data = data.copy()
    steps = []
    n = len(data)

    for i in range(n):
        for j in range(n - i - 1):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
                steps.append((j, j + 1))

    return steps


def insert_sort_steps(data):
    data = data.copy()
    steps = []
    n = len(data)
    for i in range(n):
        for j in range(i, 0, -1):
            if data[j] < data[j - 1]:
                data[j], data[j - 1] = data[j - 1], data[j]
                steps.append((j - 1, j))

    return steps
